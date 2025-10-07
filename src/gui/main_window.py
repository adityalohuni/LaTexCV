"""Main window for the CV generator GUI application."""

import os
import tkinter as tk
import tkinter.simpledialog as simpledialog
from pathlib import Path

try:
    from tkfontawesome import icon_to_image
except ImportError:
    icon_to_image = None

try:
    from pdf2image import convert_from_path
    from PIL import Image, ImageTk
except ImportError:
    ImageTk = None
    convert_from_path = None

import ttkbootstrap as ttk
from ttkbootstrap.constants import DANGER, LINK, SUCCESS
from ttkbootstrap.scrolled import ScrolledFrame

from controllers.resume_controller import ResumeController
from gui.fonts import FONTS
from models.resume_model import ResumeModel
from gui.views.contact_section import ContactSection
from gui.views.education_section import EducationSection
from gui.views.interests_section import InterestsSection
from gui.views.item_section import ItemSection
from gui.views.name_section import NameSection
from gui.views.skills_section import SkillsSection
from gui.views.summary_section import SummarySection
from gui.views.experience_section import ExperienceSection

RESUME_YAML = "resume.yaml"
BUILD_DIR = "build"
PDF_PATH = f"{BUILD_DIR}/resume.pdf"


class MainWindow(ttk.Window):
    """Main application window for CV generation."""

    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.title("CV Generator")
        self.geometry("1400x800")  # Increased size for better proportions
        self.resizable(True, True)
        # model + controller
        self.model = ResumeModel(RESUME_YAML)
        self.controller = ResumeController(self.model, BUILD_DIR, PDF_PATH)
        # assets
        self.cls_files = self.get_cls_files()
        self.dynamic_sections = []
        # include default sections in order
        self.section_names = ['name', 'contact', 'summary', 'experience', 'education', 'skills', 'interests']
        self.all_section_names = self.section_names[:]
        # UI state
        self.current_section = 0
        self.sections = {}
        # build UI
        self.create_widgets()
        self.create_sections()
        self.show_current_section()
        # self.update_pdf_preview()

    def create_widgets(self):
        """Create and layout the main window widgets."""
        # Top Navigation Bar
        nav_frame = ttk.Frame(self, padding=10)
        nav_frame.pack(fill="x", side="top")
        nav_frame.grid_columnconfigure(0, weight=1)
        nav_frame.grid_columnconfigure(1, weight=0)

        # Left: Brand
        brand_frame = ttk.Frame(nav_frame)
        brand_frame.grid(row=0, column=0, sticky="w")
        icon_label = ttk.Label(
            brand_frame, text="📄", font=("Helvetica", 18), bootstyle="primary"
        )
        icon_label.pack(side="left", padx=(0, 5))
        title_label = ttk.Label(
            brand_frame,
            text="CV Generator",
            font=("Helvetica", 18, "bold"),
            bootstyle="primary",
        )
        title_label.pack(side="left")

        # Right: Buttons
        button_frame = ttk.Frame(nav_frame)
        button_frame.grid(row=0, column=1, sticky="e")
        add_section_btn = ttk.Button(
            button_frame,
            text="Add Section",
            command=self.add_new_section,
            bootstyle="secondary",
        )
        add_section_btn.pack(side="left", padx=(0, 10))
        download_btn = ttk.Button(
            button_frame,
            text="Download PDF",
            command=self.save_and_compile,
            bootstyle="primary",
        )
        download_btn.pack(side="left")

        # Main Content Area (Split Layout)
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Left Panel - CV Editor (50% width)
        editor_frame = ttk.Frame(self.main_frame, padding=20)
        editor_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        editor_frame.grid_columnconfigure(0, weight=1)
        editor_frame.grid_rowconfigure(0, weight=0)
        editor_frame.grid_rowconfigure(1, weight=0)
        editor_frame.grid_rowconfigure(2, weight=1)
        editor_frame.grid_rowconfigure(3, weight=0)

        # CLS Template Selection
        cls_frame = ttk.Frame(editor_frame)
        cls_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        cls_label = ttk.Label(cls_frame, text="CV Template (.cls):", font=FONTS["text"])
        cls_label.pack(side="left")
        self.cls_menu = ttk.Combobox(
            cls_frame,
            values=self.cls_files if self.cls_files else ["No .cls found"],
            font=FONTS["text"],
        )
        self.cls_menu.set(self.cls_files[0] if self.cls_files else "")
        self.cls_menu.pack(side="left", padx=(10, 0))

        # Section Management
        sections_label = ttk.Label(
            editor_frame, text="Sections", font=("Helvetica", 16, "bold")
        )
        sections_label.grid(row=1, column=0, sticky="w", pady=(0, 10))
        # Keep scrollbar visible so users can scroll through all sections on one page
        self.scrolled_frame = ScrolledFrame(editor_frame, autohide=False)
        self.scrolled_frame.grid(row=2, column=0, sticky="nsew")

        # No previous/next navigation — user scrolls through all sections
        preview_frame = ttk.Frame(self.main_frame, padding=20)
        preview_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        preview_frame.grid_columnconfigure(0, weight=1)
        preview_frame.grid_rowconfigure(0, weight=0)
        preview_frame.grid_rowconfigure(1, weight=1)

        preview_header = ttk.Label(
            preview_frame,
            text="CV Preview",
            font=("Helvetica", 16, "bold"),
            bootstyle="secondary",
        )
        preview_header.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        preview_container = ttk.Frame(
            preview_frame, borderwidth=1, relief="solid", padding=10
        )
        preview_container.grid(row=1, column=0, sticky="nsew")
        self.preview_label = ttk.Label(
            preview_container, text="PDF Preview will appear here"
        )
        self.preview_label.pack(expand=True)
        # Drag visual indicator state
        self._drag_indicator = None
        self._drag_state = {'name': None}

    def create_sections(self):
        data = self.model.get_data()
        # If YAML contained an explicit order, respect it
        saved_order = self.model.get_order()
        if saved_order and isinstance(saved_order, list):
            # use saved order
            self.all_section_names = saved_order[:]
        else:
            self.all_section_names = self.section_names[:]

        # Pass drag and move callbacks to SectionView-derived sections
        cb_kwargs = dict(
            drag_callback=self.handle_drag_event,
            move_up_callback=self.move_section_up,
            move_down_callback=self.move_section_down,
        )

        # Factory mapping
        factory = {
            'name': lambda d: NameSection(self.scrolled_frame, d, **cb_kwargs),
            'contact': lambda d: ContactSection(self.scrolled_frame, d, **cb_kwargs),
            'summary': lambda d: SummarySection(self.scrolled_frame, d, **cb_kwargs),
            'experience': lambda d: ExperienceSection(self.scrolled_frame, d, **cb_kwargs),
            'education': lambda d: EducationSection(self.scrolled_frame, d, **cb_kwargs),
            'skills': lambda d: SkillsSection(self.scrolled_frame, d, **cb_kwargs),
            'interests': lambda d: InterestsSection(self.scrolled_frame, d, **cb_kwargs),
        }

        # Instantiate sections in the chosen order
        for name in self.all_section_names:
            section_data = data.get(name) if isinstance(data, dict) else None
            if name in factory:
                self.sections[name] = factory[name](section_data)
            else:
                # unknown/dynamic sections use ItemSection with default fields
                self.sections[name] = ItemSection(self.scrolled_frame, name, ["title", "description"], section_data, **cb_kwargs)

    # Drag/reorder support -------------------------------------------------
    def handle_drag_event(self, action, section_name, event):
        """Live drag preview and reorder.
        action: 'start', 'motion', 'end'
        """
        container = self.scrolled_frame.container
        if action == 'start':
            # remember which section is being dragged
            self._drag_state['name'] = section_name
            # ensure indicator exists
            if self._drag_indicator is None:
                self._drag_indicator = ttk.Frame(container, height=4)
            # raise drag indicator and hide the dragged widget temporarily
            dragged = self.sections.get(section_name).frame
            dragged.lift()
            # Create a lightweight ghost window showing the section title
            try:
                self._ghost = tk.Toplevel(self)
                self._ghost.overrideredirect(True)
                lbl = ttk.Label(self._ghost, text=section_name.replace('_', ' ').title(), bootstyle='secondary')
                lbl.pack()
                self._ghost.attributes('-alpha', 0.85)
            except Exception:
                self._ghost = None
        elif action == 'motion':
            if not self._drag_state.get('name'):
                return
            y = event.y_root - container.winfo_rooty()
            # find insertion index by midpoint
            insert_index = 0
            for i, name in enumerate(self.all_section_names):
                if name not in self.sections:
                    continue
                w = self.sections[name].frame
                top = w.winfo_y()
                height = w.winfo_height()
                if y > top + height / 2:
                    insert_index = i + 1
            # determine target widget at insertion index
            target_widget = None
            for name in self.all_section_names[insert_index:]:
                if name in self.sections and name != self._drag_state['name']:
                    target_widget = self.sections[name].frame
                    break
            # place indicator
            self._drag_indicator.place_forget()
            if target_widget:
                self._drag_indicator.place(in_=container, x=0, y=target_widget.winfo_y(), relwidth=1)
            else:
                # end of list
                self._drag_indicator.place(in_=container, x=0, y=container.winfo_height(), relwidth=1)
            # move ghost with cursor
            try:
                if getattr(self, '_ghost', None):
                    gx = event.x_root + 10
                    gy = event.y_root + 10
                    self._ghost.geometry(f'+{gx}+{gy}')
            except Exception:
                pass
        elif action == 'end':
            if not self._drag_state.get('name'):
                return
            y = event.y_root - container.winfo_rooty()
            insert_index = 0
            for i, name in enumerate(self.all_section_names):
                if name not in self.sections:
                    continue
                w = self.sections[name].frame
                top = w.winfo_y()
                height = w.winfo_height()
                if y > top + height / 2:
                    insert_index = i + 1
            # clear indicator and reorder
            self._drag_indicator.place_forget()
            self.reorder_section(self._drag_state['name'], insert_index)
            # destroy ghost
            try:
                if getattr(self, '_ghost', None):
                    self._ghost.destroy()
            except Exception:
                pass
            self._drag_state['name'] = None

    def reorder_section(self, section_name, new_index):
        if section_name not in self.all_section_names:
            return
        old_index = self.all_section_names.index(section_name)
        if old_index == new_index:
            return
        # remove and insert
        self.all_section_names.pop(old_index)
        self.all_section_names.insert(new_index, section_name)
        # refresh UI order in scrolled_frame.container
        # pack_forget all then repack in new order
        for name in self.all_section_names:
            if name in self.sections:
                self.sections[name].frame.pack_forget()
        for name in self.all_section_names:
            if name in self.sections:
                self.sections[name].frame.pack(fill="x", pady=10, padx=5)
        # autosave the order to resume.yaml
        try:
            self._autosave_order()
        except Exception:
            pass

    def _autosave_order(self):
        # collect visible section data
        data = {}
        for section_name, section in self.sections.items():
            # Always include section data in the saved YAML regardless of UI mute state
            data[section_name] = section.get_data()
        ordered_data = {k: data.get(k) for k in self.all_section_names if k in data}
        for k, v in data.items():
            if k not in ordered_data:
                ordered_data[k] = v
        yaml_payload = {"_order": self.all_section_names, **ordered_data}
        # write YAML without triggering compile
        self.model.save(yaml_payload)

    def move_section_up(self, section_name):
        if section_name in self.all_section_names:
            idx = self.all_section_names.index(section_name)
            if idx > 0:
                self.reorder_section(section_name, idx - 1)

    def move_section_down(self, section_name):
        if section_name in self.all_section_names:
            idx = self.all_section_names.index(section_name)
            if idx < len(self.all_section_names) - 1:
                self.reorder_section(section_name, idx + 1)

    def show_current_section(self):
        # Ensure all sections are shown in the editor; visibility toggles only mute inputs
        for name in self.all_section_names:
            if name in self.sections:
                section = self.sections[name]
                section.frame.pack(fill="x", pady=10, padx=5)
                try:
                    # apply muted/enabled appearance per section
                    section.set_enabled(section.visible)
                except Exception:
                    pass

    # removed prev/next/dots navigation — scrolling replaces it

    def load_yaml(self):
        self.model.load()
        data = self.model.get_data()
        for section_name, section in self.sections.items():
            section.load_data(data.get(section_name))

    def save_and_compile(self):
        """Save the data and compile the PDF."""
        data = {}
        for section_name, section in self.sections.items():
            # visibility is a UI-only state and does not affect what is written to YAML
            data[section_name] = section.get_data()
        # Preserve order in the YAML by storing an explicit order list
        ordered_data = {k: data.get(k) for k in self.all_section_names if k in data}
        # also include any additional entries that were not UI sections
        for k, v in data.items():
            if k not in ordered_data:
                ordered_data[k] = v

        # attach a special key for order so loader can respect it (non-destructive)
        yaml_payload = {"_order": self.all_section_names, **ordered_data}
        # save via controller (which writes yaml and compiles)
        self.controller.save_and_compile(yaml_payload, self.cls_menu.get(), self.update_pdf_preview)

    def update_pdf_preview(self):
        if convert_from_path is None or ImageTk is None:
            self.preview_label.config(
                text="Install pdf2image and Pillow for PDF preview."
            )
            return
        if not self.controller.pdf_exists():
            self.preview_label.config(text="PDF not found. Compile first.")
            return
        try:
            images = convert_from_path(
                PDF_PATH, first_page=1, last_page=1, size=(600, 800)
            )
            img = images[0]
            img_tk = ImageTk.PhotoImage(img)
            self.preview_label.config(image=img_tk, text="")
            self.preview_label.image = img_tk
        except Exception as e:
            self.preview_label.config(text=f"Error loading PDF: {e}")

    def get_cls_files(self):
        cls_dir = "cls"
        if not os.path.isdir(cls_dir):
            return []
        return [
            os.path.join(cls_dir, f) for f in os.listdir(cls_dir) if f.endswith(".cls")
        ]

    def add_new_section(self):
        """Add a new custom section."""
        name = simpledialog.askstring("New Section", "Enter section name:", parent=self)
        if name and name not in self.sections:
            cb_kwargs = dict(
                drag_callback=self.handle_drag_event,
                move_up_callback=self.move_section_up,
                move_down_callback=self.move_section_down,
            )
            self.sections[name] = ItemSection(
                self.scrolled_frame,
                name,
                ["title", "description"],
                None,
                **cb_kwargs,
            )
            self.dynamic_sections.append(name)
            self.all_section_names.append(name)
            self.current_section = len(self.all_section_names) - 1
            self.update_dots()
            self.show_current_section()


if __name__ == "__main__":
    MainWindow().mainloop()
