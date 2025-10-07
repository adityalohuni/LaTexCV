"""Main window for the CV generator GUI application."""

import os
import tkinter as tk
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox

try:
    from pdf2image import convert_from_path
    from PIL import Image, ImageTk
except Exception:
    convert_from_path = None
    ImageTk = None

import ttkbootstrap as ttk
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
from gui.section_manager import SectionManager

RESUME_YAML = "resume.yaml"
BUILD_DIR = "build"
PDF_PATH = f"{BUILD_DIR}/resume.pdf"


class MainWindow(ttk.Window):
    """Main application window for CV generation."""

    def __init__(self):
        super().__init__()
        self.title("CV Generator")
        self.geometry("1400x800")
        self.resizable(True, True)

        # model + controller
        self.model = ResumeModel(RESUME_YAML)
        self.controller = ResumeController(self.model, BUILD_DIR, PDF_PATH)

        # assets and section lists
        self.cls_files = self.get_cls_files()
        self.dynamic_sections = []
        self.section_names = [
            'name', 'contact', 'summary', 'experience', 'education', 'skills', 'interests'
        ]
        self.all_section_names = self.section_names[:]

        # UI state
        self.current_section = 0
        self.sections = {}

        # Section manager centralizes order/save/remove behaviors
        self.section_manager = SectionManager(self.model, self.sections, self.all_section_names, self.dynamic_sections)

        # build UI
        self.create_widgets()
        self.create_sections()
        self.show_current_section()

    def create_widgets(self):
        # Top Navigation Bar
        nav_frame = ttk.Frame(self, padding=10)
        nav_frame.pack(fill="x", side="top")
        nav_frame.grid_columnconfigure(0, weight=1)
        nav_frame.grid_columnconfigure(1, weight=0)

        # Left: Brand
        brand_frame = ttk.Frame(nav_frame)
        brand_frame.grid(row=0, column=0, sticky="w")
        icon_label = ttk.Label(brand_frame, text="📄", font=("Helvetica", 18), bootstyle="primary")
        icon_label.pack(side="left", padx=(0, 5))
        title_label = ttk.Label(brand_frame, text="CV Generator", font=("Helvetica", 18, "bold"), bootstyle="primary")
        title_label.pack(side="left")

        # Right: Buttons
        button_frame = ttk.Frame(nav_frame)
        button_frame.grid(row=0, column=1, sticky="e")
        add_section_btn = ttk.Button(button_frame, text="Add Section", command=self.add_new_section, bootstyle="secondary")
        add_section_btn.pack(side="left", padx=(0, 10))
        download_btn = ttk.Button(button_frame, text="Download PDF", command=self.save_and_compile, bootstyle="primary")
        download_btn.pack(side="left")

        # Main Content Area
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Left Panel - CV Editor
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
        cls_label = ttk.Label(cls_frame, text="CV Template (.cls):", font=FONTS.get("text"))
        cls_label.pack(side="left")
        self.cls_menu = ttk.Combobox(cls_frame, values=self.cls_files if self.cls_files else ["No .cls found"], font=FONTS.get("text"))
        self.cls_menu.set(self.cls_files[0] if self.cls_files else "")
        self.cls_menu.pack(side="left", padx=(10, 0))

        sections_label = ttk.Label(editor_frame, text="Sections", font=("Helvetica", 16, "bold"))
        sections_label.grid(row=1, column=0, sticky="w", pady=(0, 10))

        self.scrolled_frame = ScrolledFrame(editor_frame, autohide=False)
        self.scrolled_frame.grid(row=2, column=0, sticky="nsew")

        # Preview panel
        preview_frame = ttk.Frame(self.main_frame, padding=20)
        preview_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        preview_frame.grid_columnconfigure(0, weight=1)
        preview_frame.grid_rowconfigure(0, weight=0)
        preview_frame.grid_rowconfigure(1, weight=1)

        preview_header = ttk.Label(preview_frame, text="CV Preview", font=("Helvetica", 16, "bold"), bootstyle="secondary")
        preview_header.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        preview_container = ttk.Frame(preview_frame, borderwidth=1, relief="solid", padding=10)
        preview_container.grid(row=1, column=0, sticky="nsew")
        self.preview_label = ttk.Label(preview_container, text="PDF Preview will appear here")
        self.preview_label.pack(expand=True)

        # Drag visual state
        self._drag_indicator = None
        self._drag_state = {'name': None}

    def create_sections(self):
        data = self.model.get_data()
        saved_order = self.model.get_order()
        if saved_order and isinstance(saved_order, list):
            self.all_section_names = saved_order[:]
        else:
            self.all_section_names = self.section_names[:]

        cb_kwargs = dict(
            drag_callback=self.handle_drag_event,
            move_up_callback=self.move_section_up,
            move_down_callback=self.move_section_down,
            remove_callback=self.remove_section,
            visibility_callback=self.section_manager.autosave_order,
        )

        factory = {
            'name': lambda d: NameSection(self.scrolled_frame, d, **cb_kwargs),
            'contact': lambda d: ContactSection(self.scrolled_frame, d, **cb_kwargs),
            'summary': lambda d: SummarySection(self.scrolled_frame, d, **cb_kwargs),
            'experience': lambda d: ExperienceSection(self.scrolled_frame, d, **cb_kwargs),
            'education': lambda d: EducationSection(self.scrolled_frame, d, **cb_kwargs),
            'skills': lambda d: SkillsSection(self.scrolled_frame, d, **cb_kwargs),
            'interests': lambda d: InterestsSection(self.scrolled_frame, d, **cb_kwargs),
        }

        for name in self.all_section_names:
            section_data = data.get(name) if isinstance(data, dict) else None
            if name in factory:
                self.sections[name] = factory[name](section_data)
            else:
                self.sections[name] = ItemSection(self.scrolled_frame, name, ["title", "description"], section_data, **cb_kwargs)

    # Drag/reorder support -------------------------------------------------
    def handle_drag_event(self, action, section_name, event):
        container = getattr(self.scrolled_frame, 'container', None)
        if container is None:
            return
        if action == 'start':
            self._drag_state['name'] = section_name
            if self._drag_indicator is None:
                self._drag_indicator = ttk.Frame(container, height=4)
            dragged = self.sections.get(section_name).frame
            dragged.lift()
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
            insert_index = 0
            for i, name in enumerate(self.all_section_names):
                if name not in self.sections:
                    continue
                w = self.sections[name].frame
                top = w.winfo_y()
                height = w.winfo_height()
                if y > top + height / 2:
                    insert_index = i + 1
            target_widget = None
            for name in self.all_section_names[insert_index:]:
                if name in self.sections and name != self._drag_state['name']:
                    target_widget = self.sections[name].frame
                    break
            self._drag_indicator.place_forget()
            if target_widget:
                self._drag_indicator.place(in_=container, x=0, y=target_widget.winfo_y(), relwidth=1)
            else:
                self._drag_indicator.place(in_=container, x=0, y=container.winfo_height(), relwidth=1)
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
            self._drag_indicator.place_forget()
            self.reorder_section(self._drag_state['name'], insert_index)
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
        self.all_section_names.pop(old_index)
        self.all_section_names.insert(new_index, section_name)
        for name in self.all_section_names:
            if name in self.sections:
                self.sections[name].frame.pack_forget()
        for name in self.all_section_names:
            if name in self.sections:
                self.sections[name].frame.pack(fill="x", pady=10, padx=5)
        try:
            self.section_manager.autosave_order()
        except Exception:
            pass

    def _autosave_order(self):
        try:
            self.section_manager.autosave_order()
        except Exception:
            pass

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
        for name in self.all_section_names:
            if name in self.sections:
                section = self.sections[name]
                section.frame.pack(fill="x", pady=10, padx=5)
                try:
                    section.set_enabled(section.visible)
                except Exception:
                    pass

    def load_yaml(self):
        self.model.load()
        data = self.model.get_data()
        for section_name, section in self.sections.items():
            section.load_data(data.get(section_name))

    def save_and_compile(self):
        data = {}
        for section_name, section in self.sections.items():
            data[section_name] = section.get_data()
        ordered_data = {k: data.get(k) for k in self.all_section_names if k in data}
        for k, v in data.items():
            if k not in ordered_data:
                ordered_data[k] = v
        yaml_payload = {"_order": self.all_section_names, **ordered_data}
        self.controller.save_and_compile(yaml_payload, self.cls_menu.get(), self.update_pdf_preview)

    def update_pdf_preview(self):
        if convert_from_path is None or ImageTk is None:
            self.preview_label.config(text="Install pdf2image and Pillow for PDF preview.")
            return
        if not self.controller.pdf_exists():
            self.preview_label.config(text="PDF not found. Compile first.")
            return
        try:
            images = convert_from_path(PDF_PATH, first_page=1, last_page=1, size=(600, 800))
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
        return [os.path.join(cls_dir, f) for f in os.listdir(cls_dir) if f.endswith(".cls")]

    def add_new_section(self):
        name = simpledialog.askstring("New Section", "Enter section name:", parent=self)
        if name and name not in self.sections:
            cb_kwargs = dict(
                drag_callback=self.handle_drag_event,
                move_up_callback=self.move_section_up,
                move_down_callback=self.move_section_down,
                remove_callback=self.remove_section,
                visibility_callback=self.section_manager.autosave_order,
            )
            self.sections[name] = ItemSection(self.scrolled_frame, name, ["title", "description"], None, **cb_kwargs)
            self.dynamic_sections.append(name)
            self.all_section_names.append(name)
            self.current_section = len(self.all_section_names) - 1
            try:
                self.section_manager.autosave_order()
            except Exception:
                pass
            self.show_current_section()

    def remove_section(self, section_name_or_obj):
        if isinstance(section_name_or_obj, str):
            name = section_name_or_obj
        else:
            name = getattr(section_name_or_obj, 'section_name', None)
        if not name or name not in self.sections:
            return False
        if name not in self.section_names:
            ok = messagebox.askyesno("Remove section", f"Remove section '{name}'? This will delete any data for it.", parent=self)
            if not ok:
                return False
        try:
            sec = self.sections.pop(name)
            try:
                if getattr(sec, 'frame', None):
                    sec.frame.destroy()
            except Exception:
                pass
        except KeyError:
            return False
        if name in self.all_section_names:
            try:
                self.all_section_names.remove(name)
            except ValueError:
                pass
        if name in self.dynamic_sections:
            try:
                self.dynamic_sections.remove(name)
            except ValueError:
                pass
        try:
            self.section_manager.autosave_order()
        except Exception:
            pass
        return True


if __name__ == "__main__":
    MainWindow().mainloop()
