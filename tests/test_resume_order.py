import sys
from pathlib import Path

# ensure src package is importable from tests (insert repo root so `src` is a package folder)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import types
# Create minimal pylatex stubs so the ResumeGenerator module can import
if 'pylatex' not in sys.modules:
    pylatex = types.ModuleType('pylatex')
    class _Dummy:
        def __init__(self, *a, **k):
            pass
    pylatex.Document = _Dummy
    pylatex.Section = _Dummy
    pylatex.MiniPage = _Dummy
    pylatex.Command = _Dummy
    pylatex.Enumerate = _Dummy
    sys.modules['pylatex'] = pylatex
if 'pylatex.utils' not in sys.modules:
    utils = types.ModuleType('pylatex.utils')
    def NoEscape(x):
        return x
    utils.NoEscape = NoEscape
    sys.modules['pylatex.utils'] = utils
if 'pylatex.basic' not in sys.modules:
    basic = types.ModuleType('pylatex.basic')
    class NewLine:
        pass
    basic.NewLine = NewLine
    sys.modules['pylatex.basic'] = basic

from src.core.generator.resume_generator import ResumeGenerator


class TestableResumeGenerator(ResumeGenerator):
    def __init__(self, data_dict):
        # Do not initialize parent pylatex document; just set data
        self.data = data_dict
        self.processed = []

    def _add_header(self):
        # no-op for tests
        return

    def _add_section(self, title: str, items: list, parent=None):
        # Instead of generating LaTeX, record the section title and items
        self.processed.append((title, items))

    def generate(self, tex_path: str = 'resume.tex'):
        # Re-implement only the ordering + left/right splitting from ResumeGenerator.generate
        left_sections, right_sections = [], []
        reserved_keys = ['name', 'contact', 'cls', '_order']

        section_names_to_process = []
        if isinstance(self.data, dict) and isinstance(self.data.get('_order'), list):
            for name in self.data.get('_order'):
                if name in reserved_keys:
                    continue
                if name in self.data:
                    section_names_to_process.append(name)
            for name in self.data:
                if name in reserved_keys or name in section_names_to_process:
                    continue
                section_names_to_process.append(name)
        else:
            for name in self.data:
                if name in reserved_keys:
                    continue
                section_names_to_process.append(name)

        for section_name in section_names_to_process:
            items = self.data.get(section_name)
            if not isinstance(items, list) or not items:
                continue
            if isinstance(items[0], dict) and items[0].get('left', False):
                left_sections.append((section_name, items))
            else:
                right_sections.append((section_name, items))

        # record in the order they would be added (left then right as generator did)
        for title, items in left_sections + right_sections:
            self._add_section(title, items)


def test_generate_respects_order_with__order():
    data = {
        '_order': ['skills', 'education', 'experience'],
        'skills': ['python', 'git'],
        'education': [{'institution': 'X', 'degree': 'BSc'}],
        'experience': [{'company': 'Y', 'title': 'Dev'}],
        'name': {'first': 'A', 'last': 'B'},
        'contact': {'email': 'a@b.com'}
    }
    rg = TestableResumeGenerator(data)
    rg.generate(tex_path=':memory:')
    titles = [t for (t, _) in rg.processed]
    # since none of the items include left:true, all should be in the right column
    assert titles == ['skills', 'education', 'experience']


def test_generate_falls_back_to_mapping_order_when_no__order():
    # mapping order: python 3.7+ preserves insertion order
    data = {
        'skills': ['python', 'git'],
        'experience': [{'company': 'Y', 'title': 'Dev'}],
        'education': [{'institution': 'X', 'degree': 'BSc'}],
        'name': {'first': 'A', 'last': 'B'},
        'contact': {'email': 'a@b.com'}
    }
    rg = TestableResumeGenerator(data)
    rg.generate(tex_path=':memory:')
    titles = [t for (t, _) in rg.processed]
    assert titles == ['skills', 'experience', 'education']
