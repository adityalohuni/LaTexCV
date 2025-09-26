import threading
import tkinter.messagebox as messagebox
from pathlib import Path

from core.cv_compiler import CVCompiler


class ResumeController:
    def __init__(self, model, build_dir="build", pdf_path="build/resume.pdf"):
        self.model = model
        self.cv_compiler = CVCompiler(build_dir)
        self.pdf_path = pdf_path

    def save_and_compile(self, data, cls_file, callback=None):
        try:
            self.model.save(data)
            threading.Thread(
                target=self.compile_resume, args=(cls_file, callback)
            ).start()
        except Exception as e:
            messagebox.showerror("YAML Error", f"Invalid YAML: {e}")

    def compile_resume(self, cls_file, callback=None):
        success, msg = self.cv_compiler.build_pipeline(
            "resume.yaml", "resume.tex", cls_file
        )
        if not success:
            messagebox.showerror("Compile Error", msg)
        if callback:
            callback()

    def pdf_exists(self):
        return Path(self.pdf_path).exists()
