import os
import shutil
import subprocess
from pathlib import Path
from latex import build_pdf

class CVCompiler:
    def __init__(self, build_dir='build'):
        self.build_dir = build_dir
        os.makedirs(self.build_dir, exist_ok=True)

    def run_command(self, cmd, cwd=None):
        try:
            result = subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr

    def generate_tex_from_yaml(self, yaml_file, cls_file):
        # Step 1: Generate resume.tex from YAML using module, passing cls_file
        try:
            from core.generator.generic import generate_resume
            generate_resume(yaml_file, 'resume.tex', cls_file=cls_file)
            return True, "resume.tex generated"
        except Exception as e:
            return False, f"YAML to TEX failed: {e}"

    def copy_files(self, tex_file, cls_file):
        # Step 2: Copy files to build dir, rename cls file to match template name
        try:
            shutil.copy(tex_file, self.build_dir)
            # Copy cls file with its basename into build dir
            import os
            cls_basename = os.path.basename(cls_file)
            shutil.copy(cls_file, os.path.join(self.build_dir, cls_basename))
            return True, "Files copied"
        except Exception as e:
            return False, f"File copy failed: {e}"

    def compile_pdf(self, tex_file):
        # Step 3: Ensure .cls file exists in build dir before compiling
        tex_path = Path(self.build_dir) / tex_file
        # Extract documentclass name from .tex file
        import re
        with tex_path.open() as f:
            tex_content = f.read()
        match = re.search(r'\\documentclass\[.*\]\{(.*?)\}', tex_content)
        cls_name = match.group(1) if match else None
        cls_file_path = Path(self.build_dir) / f"{cls_name}.cls"
        if not cls_file_path.exists():
            return False, f"Required .cls file '{cls_file_path.name}' is missing in build directory."
        # NOTE: Ensure your .cls files use fonts compatible with pdflatex (not xelatex-only fonts)
        try:
            pdf = build_pdf(tex_path.read_text(), texinputs=[str(Path(self.build_dir))])
            pdf.save_to(str(Path(self.build_dir) / tex_path.with_suffix('.pdf').name))
            return True, "PDF compiled"
        except Exception as e:
            return False, f"LaTeX compilation failed: {e}"

    def build_pipeline(self, yaml_file, tex_file, cls_file):
        steps = [
            (self.generate_tex_from_yaml, [yaml_file, cls_file]),
            (self.copy_files, [tex_file, cls_file]),
            (self.compile_pdf, [tex_file]),
        ]
        for func, args in steps:
            success, msg = func(*args)
            if not success:
                return False, msg
        return True, "Build pipeline completed"
