"""Main window for the CV generator GUI application."""

import os
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
from views.contact_section import ContactSection
from views.education_section import EducationSection
from views.interests_section import InterestsSection
from views.item_section import ItemSection
from views.name_section import NameSection
from views.skills_section import SkillsSection
from views.summary_section import SummarySection

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
        self.model = ResumeModel(RESUME_YAML)
        self.controller = ResumeController(self.model, BUILD_DIR, PDF_PATH)
        self.cls_files = self.get_cls_files()
        self.dynamic_sections = []
        self.section_names = ['name', 'contact', 'summary', 'education', 'skills', 'interests']
        self.all_section_names = self.section_names[:]
        self.current_section = 0
        self.sections = {}
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

        self.scrolled_frame = ScrolledFrame(editor_frame, autohide=True)
        self.scrolled_frame.grid(row=2, column=0, sticky="nsew")

        # Navigation Controls
        nav_controls = ttk.Frame(editor_frame)
        nav_controls.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        self.prev_btn = ttk.Button(
            nav_controls, text="Previous", command=self.prev_section, bootstyle="secondary"
        )
        self.prev_btn.pack(side="left")
        self.dots_frame = ttk.Frame(nav_controls)
        self.dots_frame.pack(side="left", expand=True)
        self.next_btn = ttk.Button(
            nav_controls, text="Next", command=self.next_section, bootstyle="secondary"
        )
        self.next_btn.pack(side="right")

        self.update_dots()
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

    def create_sections(self):
        data = self.model.get_data()
        self.sections["name"] = NameSection(
            self.scrolled_frame.container,
            data.get("name"),
        )
        self.sections["contact"] = ContactSection(
            self.scrolled_frame.container,
            data.get("contact"),
        )
        self.sections["summary"] = SummarySection(
            self.scrolled_frame.container,
            data.get("summary"),
        )
        self.sections["education"] = EducationSection(
            self.scrolled_frame.container,
            data.get("education"),
        )
        self.sections["skills"] = SkillsSection(
            self.scrolled_frame.container,
            data.get("skills"),
        )
        self.sections["interests"] = InterestsSection(
            self.scrolled_frame.container,
            data.get("interests"),
        )
        # Add more sections as needed

    def show_current_section(self):
        for name in self.all_section_names:
            if name in self.sections:
                section = self.sections[name]
                if name == self.all_section_names[self.current_section] and section.visible:
                    section.frame.pack(fill="x", pady=10, padx=5)
                else:
                    section.frame.pack_forget()

    def prev_section(self):
        if self.current_section > 0:
            self.current_section -= 1
            self.show_current_section()
            self.update_dots()

    def next_section(self):
        if self.current_section < len(self.all_section_names) - 1:
            self.current_section += 1
            self.show_current_section()
            self.update_dots()

    def update_dots(self):
        for widget in self.dots_frame.winfo_children():
            widget.destroy()
        for i, name in enumerate(self.all_section_names):
            dot = ttk.Label(
                self.dots_frame,
                text=str(i + 1),
                bootstyle="primary" if i == self.current_section else "secondary",
            )
            dot.pack(side="left", padx=5)

    def load_yaml(self):
        self.model.load()
        data = self.model.get_data()
        for section_name, section in self.sections.items():
            section.load_data(data.get(section_name))

    def save_and_compile(self):
        """Save the data and compile the PDF."""
        data = {}
        for section_name, section in self.sections.items():
            if section.visible:
                data[section_name] = section.get_data()
        self.controller.save_and_compile(
            data, self.cls_menu.get(), self.update_pdf_preview
        )

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
            self.sections[name] = ItemSection(
                self.scrolled_frame.container,
                name,
                ["title", "description"],
            )
            self.dynamic_sections.append(name)
            self.all_section_names.append(name)
            self.current_section = len(self.all_section_names) - 1
            self.update_dots()
            self.show_current_section()


if __name__ == "__main__":
    MainWindow().mainloop()
