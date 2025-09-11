import tkinter as tk
from tkinter import messagebox, scrolledtext
import tkinter.font as tkfont
from pathlib import Path
from PIL import Image, ImageTk
import threading
import os
try:
    from pdf2image import convert_from_path
except ImportError:
    convert_from_path = None

from core.yaml_handler import YAMLHandler
from core.cv_compiler import CVCompiler

RESUME_YAML = 'resume.yaml'
BUILD_DIR = 'build'
PDF_PATH = f'{BUILD_DIR}/resume.pdf'

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('YAML Resume Editor & PDF Preview')
        self.geometry('1200x700')
        self.configure(bg='#F5F5F7')
        self.yaml_handler = YAMLHandler(RESUME_YAML)
        self.cv_compiler = CVCompiler(BUILD_DIR)
        self.cls_files = self.get_cls_files()
        self.selected_cls = tk.StringVar(value=self.cls_files[0] if self.cls_files else '')
        self.create_widgets()
        self.load_yaml()
        self.update_pdf_preview()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        available_fonts = tkfont.families()
        font_family = 'SF Pro Display' if 'SF Pro Display' in available_fonts else 'Helvetica'
        text_font = (font_family, 14)
        header_font = (font_family, 18, 'bold')
        button_font = (font_family, 13)

        editor_frame = tk.Frame(self, bg='#F5F5F7', bd=0)
        editor_frame.grid(row=0, column=0, sticky='nsew', padx=(40, 20), pady=(30, 20))
        editor_frame.grid_columnconfigure(0, weight=1)
        editor_frame.grid_columnconfigure(1, weight=2)
        editor_frame.grid_rowconfigure(2, weight=1)
        header_font2 = ("Arial", 16, "bold")
        text_font2 = ("Courier New", 12)
        editor_label = tk.Label(editor_frame, text='YAML Editor', font=header_font2, bg='#F5F5F7', fg='#1D1D1F', pady=0)
        editor_label.grid(row=0, column=0, sticky='ns')
        cls_label = tk.Label(editor_frame, text='CV Template (.cls):', font=("Arial", 12), bg='#F5F5F7', fg='#1D1D1F')
        cls_label.grid(row=1, column=0, sticky='w', pady=(5,0))
        self.cls_menu = tk.OptionMenu(editor_frame, self.selected_cls, *(self.cls_files if self.cls_files else ['No .cls found']))
        self.cls_menu.config(font=("Arial", 12), bg='#FFFFFF', fg='#1D1D1F', relief='flat', highlightthickness=1, highlightbackground='#D1D1D6')
        self.cls_menu.grid(row=1, column=1, sticky='w', pady=(5,0))
        self.yaml_text = scrolledtext.ScrolledText(editor_frame, wrap=tk.WORD, font=text_font2, bg='#FFFFFF', fg='#1D1D1F', relief='flat', highlightthickness=1, highlightbackground='#D1D1D6')
        self.yaml_text.grid(row=2, column=0, columnspan=2, sticky='ns', pady=(10, 0))
        self.yaml_text.config(borderwidth=0, padx=16, pady=16)

        self.preview_frame = tk.Frame(self, bg='#F5F5F7', bd=0)
        self.preview_frame.grid(row=0, column=1, sticky='nsew', padx=(20,40), pady=(30,20))
        self.preview_frame.grid_rowconfigure(1, weight=1)
        self.preview_frame.grid_columnconfigure(0, weight=1)
        preview_label = tk.Label(self.preview_frame, text='PDF Preview', font=header_font, bg='#F5F5F7', fg='#1D1D1F', pady=10)
        preview_label.grid(row=0, column=0, sticky='nsew')
        self.preview_label = tk.Label(self.preview_frame, text='PDF Preview will appear here', bg='#FFFFFF', fg='#1D1D1F', bd=0, relief='flat', highlightthickness=1, highlightbackground='#D1D1D6')
        self.preview_label.grid(row=1, column=0, sticky='nsew')

        self.button_frame = tk.Frame(self, bg='#F5F5F7', bd=0)
        self.button_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=40, pady=(0,20))
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.save_btn = tk.Button(self.button_frame, text='Save YAML & Compile', command=self.save_and_compile, font=button_font, bg='#007AFF', fg='#FFFFFF', activebackground='#0051A8', activeforeground='#FFFFFF', bd=0, padx=20, pady=10, relief='flat', highlightthickness=0)
        self.save_btn.pack(side='left', padx=10, pady=10)
        self.reload_btn = tk.Button(self.button_frame, text='Reload YAML', command=self.load_yaml, font=button_font, bg='#E5E5EA', fg='#1D1D1F', activebackground='#D1D1D6', activeforeground='#1D1D1F', bd=0, padx=20, pady=10, relief='flat', highlightthickness=0)
        self.reload_btn.pack(side='left', padx=10)
        self.refresh_btn = tk.Button(self.button_frame, text='Refresh PDF Preview', command=self.update_pdf_preview, font=button_font, bg='#E5E5EA', fg='#1D1D1F', activebackground='#D1D1D6', activeforeground='#1D1D1F', bd=0, padx=20, pady=10, relief='flat', highlightthickness=0)
        self.refresh_btn.pack(side='left', padx=10)

    def load_yaml(self):
        content = self.yaml_handler.load()
        self.yaml_text.delete('1.0', tk.END)
        self.yaml_text.insert(tk.END, content if content else '# resume.yaml not found. Fill in your details.')

    def save_and_compile(self):
        yaml_content = self.yaml_text.get('1.0', tk.END)
        try:
            self.yaml_handler.save(yaml_content)
        except Exception as e:
            messagebox.showerror('YAML Error', f'Invalid YAML: {e}')
            return
        threading.Thread(target=self.compile_resume).start()

    def compile_resume(self):
        self.save_btn.config(state='disabled')
        def run_pipeline():
            success, msg = self.cv_compiler.build_pipeline(RESUME_YAML, 'resume.tex', self.selected_cls.get())
            if not success:
                self.after(0, lambda: messagebox.showerror('Compile Error', msg))
            else:
                self.after(1000, self.update_pdf_preview)
            self.after(0, lambda: self.save_btn.config(state='normal'))
        threading.Thread(target=run_pipeline).start()

    def update_pdf_preview(self):
        if convert_from_path is None:
            self.preview_label.config(text='Install pdf2image and Pillow for PDF preview.')
            return
        if not Path(PDF_PATH).exists():
            self.preview_label.config(text='PDF not found. Compile first.')
            return
        try:
            images = convert_from_path(PDF_PATH, first_page=1, last_page=1, size=(600, 800))
            img = images[0]
            img_tk = ImageTk.PhotoImage(img)
            self.preview_label.config(image=img_tk, text='')
            self.preview_label.image = img_tk
        except Exception as e:
            self.preview_label.config(text=f'Error loading PDF: {e}')

    def get_cls_files(self):
        cls_dir = 'cls'
        if not os.path.isdir(cls_dir):
            return []
        return [os.path.join(cls_dir, f) for f in os.listdir(cls_dir) if f.endswith('.cls')]

if __name__ == '__main__':
    MainWindow().mainloop()
