import yaml
import re
from pathlib import Path
from pylatex import Document, Section, MiniPage, Command, Enumerate
from pylatex.utils import NoEscape
from pylatex.basic import NewLine


class ResumeGenerator:
    """
    A class to generate a LaTeX resume from a YAML data file.
    This version uses an attribute-driven architecture, formatting entries
    based on the keys they contain, not the section they are in.
    It supports nested items, bullet points, hyperlinks, and snake_case titles.
    """
    def __init__(self, yaml_path: str, cls_file: str = 'template.cls'):
        self.yaml_path = Path(yaml_path)
        self.cls_file = cls_file
        self.data = self._load_data()
        self.doc = self._setup_document()

    def _load_data(self) -> dict:
        """Loads and returns data from the YAML file."""
        if not self.yaml_path.exists():
            raise FileNotFoundError(f'{self.yaml_path} not found. Please provide a data file.')
        with self.yaml_path.open() as f:
            return yaml.safe_load(f)

    def _setup_document(self) -> Document:
        """Sets up the pylatex document with packages and preamble."""
        cls_path = Path(self.data.get('cls', self.cls_file))
        doc = Document(documentclass=cls_path.stem)
        doc.packages.append(Command('usepackage', 'enumitem'))
        doc.packages.append(Command('usepackage', 'fancyhdr'))
        doc.packages.append(Command('usepackage', 'hyperref'))
        doc.packages.append(Command('usepackage', 'fontawesome'))
        doc.preamble.append(NoEscape(r'\pagestyle{fancy}'))
        doc.preamble.append(NoEscape(r'\fancyhf{}'))
        return doc

    def _add_header(self):
        """Adds the name and dynamic contact information section."""
        name = self.data.get('name', {})
        contact = self.data.get('contact', {})
        self.doc.append(NoEscape(rf"\namesection{{{name.get('first','John')}}}{{{name.get('last','Doe')}}}{{"))
        contact_parts = []
        # Icon mapping for contact details
        icon_map = {
            'email': r'\faEnvelope', 'linkedin': r'\faLinkedin', 'github': r'\faGithub',
            'portfolio': r'\faGlobe', 'url': r'\faGlobe', 'website': r'\faGlobe'
        }
        for key, value in contact.items():
            if not value: continue
            icon = icon_map.get(key.lower())
            if key.lower() == 'email':
                contact_parts.append(NoEscape(rf"\href{{mailto:{value}}}{{{icon}\ {value}}}"))
            elif icon:
                # Remove protocol for display, but keep for link
                display_val = re.sub(r'https?://(www\.)?', '', value)
                contact_parts.append(NoEscape(rf"\href{{{value}}}{{{icon}\ {display_val}}}"))
            else:
                contact_parts.append(NoEscape(value))
        self.doc.append(NoEscape(" | ".join(contact_parts)))
        self.doc.append(NoEscape(r'}'))

    def _process_text_for_latex(self, text: str) -> NoEscape:
        """Processes a simple text string for hyperlinks and escapes special characters."""
        if not text: return NoEscape("")
        # Basic escaping for LaTeX special characters
        text = text.replace('&', r'\&').replace('%', r'\%').replace('$', r'\$')
        text = text.replace('#', r'\#').replace('_', r'\_').replace('{', r'\{').replace('}', r'\}')
        # Markdown-style hyperlinks: [text](url) -> \href{url}{text}
        text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\\href{\2}{\1}', text)
        return NoEscape(text)

    def _process_content_field(self, content, target, is_nested=False):
        """
        Recursively processes a content field, which can be a string (with bullets)
        or a list of nested dictionary items.
        """
        if isinstance(content, str):
            lines = content.strip().split('\n')
            # Check if the string contains bullet points
            if any(line.strip().startswith('- ') for line in lines):
                # replaced this {'label': '$\bullet$', 'leftmargin': '*'}
                with target.create(Enumerate(options=NoEscape(r'label=\textbullet,leftmargin=*'))) as enum:
                    # Group non-bullet lines with the previous bullet item
                    current_item_lines = []
                    for line in lines:
                        stripped_line = line.strip()
                        if stripped_line.startswith('- '):
                            if current_item_lines:
                                enum.add_item(self._process_text_for_latex(" ".join(current_item_lines)))
                            current_item_lines = [stripped_line[2:].strip()]
                        elif current_item_lines: # Append to existing item
                            current_item_lines.append(stripped_line)
                    if current_item_lines: # Add the last item
                        enum.add_item(self._process_text_for_latex(" ".join(current_item_lines)))
            else: # It's just a paragraph
                target.append(self._process_text_for_latex(content))

        elif isinstance(content, list): # Recursive case for nested items
             with target.create(Enumerate(options={'label': r'-', 'leftmargin': '*'})) as enum:
                for sub_item in content:
                    if isinstance(sub_item, dict):
                        # Create a MiniPage for the sub-item to contain its formatting
                        with enum.create(MiniPage(width=r"\linewidth")) as sub_item_mp:
                            self._format_section_item(sub_item, sub_item_mp, is_nested=True)

    def _format_section_item(self, item: dict, target, is_nested=False):
        """
        Formats a single dictionary item based on the attributes it contains.
        This is the core of the attribute-driven architecture.
        """
        # --- 1. Define Attribute Priority ---
        primary_title_keys = ['position', 'degree', 'title', 'project', 'name']
        secondary_title_keys = ['company', 'institution', 'issuer']
        meta_keys = {'dates': '', 'location': '', 'url': '', 'pull_request': 'PR: '}
        content_keys = ['description', 'contribution', 'details']
        list_keys = ['technologies', 'skills_used', 'tools']

        # --- 2. Extract and Format Titles ---
        primary_title = next((item[key] for key in primary_title_keys if key in item), None)
        secondary_title = next((item[key] for key in secondary_title_keys if key in item), None)

        if primary_title:
            target.append(Command('runsubsection', self._process_text_for_latex(primary_title)))
        if secondary_title:

            if(primary_title):
                target.append(NewLine())

            target.append(Command('descript', self._process_text_for_latex(secondary_title)))

        if(not secondary_title):
            target.append(NewLine())

        # --- 3. Extract and Format Metadata Line ---
        meta_parts = []
        for key, prefix in meta_keys.items():
            if key in item:
                value = item[key]
                if key == 'url':
                    # NEW: Check for 'url_href' to use as custom link text
                    display_text = self._process_text_for_latex(item.get('url_href', 'Link'))
                    meta_parts.append(NoEscape(rf"\href{{{value}}}{{{display_text}}}"))
                else:
                    meta_parts.append(prefix + str(value))
        if meta_parts:
            target.append(Command('location', NoEscape(" ~|~ ".join(meta_parts))))



        # --- 4. Process Main Content (potentially recursive) ---
        for key in content_keys:
            if key in item:
                self._process_content_field(item[key], target, is_nested=is_nested)

        # --- 5. Process Single-Line Lists (e.g., Technologies) ---
        for key in list_keys:
            if key in item and isinstance(item[key], list):
                label = key.replace('_', ' ').title()
                values = ", ".join(item[key])
                target.append(NoEscape(r"\\" if any(k in item for k in content_keys) else "")) # Add space if content exists
                target.append(NoEscape(r"\textbf{" + label + r":} " + self._process_text_for_latex(values)))
        
        
        if not is_nested:
            target.append(NewLine())

    def _add_section(self, title: str, items: list, parent):
        """Adds a section, processing each item based on its attributes."""
        if not items:
            return

        formatted_title = title.replace('_', ' ').title()
        with parent.create(Section(formatted_title)) as section:
            try:
                for i, item in enumerate(items):
                    if(isinstance(item, dict) and 'left' in item and len(item.keys()) <=1):
                        items.pop(i)
                       # Handle simple list of strings
                if all(isinstance(item, str) for item in items):
                    processed_items = [self._process_text_for_latex(i) for i in items]
                    section.append(NoEscape(" ".join(processed_items)))
                    return

                for item in items:
                   if isinstance(item, dict):
                        self._format_section_item(item, section)


            except Exception as e:
                           print(e)
                           raise ValueError(e)


    def generate(self, tex_path: str = 'resume.tex'):
        """Orchestrates the resume generation process."""
        self._add_header()
        
        left_sections, right_sections = [], []
        reserved_keys = ['name', 'contact', 'cls']
        for section_name, items in self.data.items():
            if section_name in reserved_keys or not isinstance(items, list) or not items:
                continue
            # Default to right column unless 'left: true' is specified in the first item
            if isinstance(items[0], dict) and items[0].get('left', False):
                left_sections.append((section_name, items))
            else:
                right_sections.append((section_name, items))
        
        with self.doc.create(MiniPage(width=r'0.33\textwidth', pos='t')) as left:
            for title, items in left_sections:
                self._add_section(title, items, parent=left)

        # self.doc.append(NoEscape('%'))
        self.doc.append(NoEscape(r'\hfill'))


        with self.doc.create(MiniPage(width=r'0.66\textwidth', pos='t', align='t')) as right:
            for title, items in right_sections:
                self._add_section(title, items, parent=right)
        
        try:
            self.doc.generate_tex(str(Path(tex_path).stem))
        except Exception as e:
            raise ValueError(e)
