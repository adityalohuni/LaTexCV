import os
import shutil
import subprocess

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

    def copy_files(self, tex_file, cls_file):
        # Step 2: Copy files to build dir, rename cls file to match template name
        try:
            import os
            shutil.rmtree(self.build_dir)
            os.makedirs(self.build_dir)
            cls_basename = os.path.basename(cls_file)
            shutil.copy(cls_file, os.path.join(self.build_dir, cls_basename))

            return True, "Files copied"
        except Exception as e:
            return False, f"File copy failed: {e}"

    def compile_pdf(self, tex_file, cls_file):
        # Step 3: Ensure .cls file exists in build dir before compiling
        # NOTE: Ensure your .cls files use fonts compatible with pdflatex (not xelatex-only fonts)
        try:
            # from src.core.generator.generic import generate_resume_pylatex

            # Define the directory where your files are
            build_dir = 'build'
            
            # Get the original working directory
            original_dir = os.getcwd()
            
            # Change to the build directory
            
            from src.core.generator import ResumeGenerator
            generator = ResumeGenerator(yaml_path='resume.yaml', cls_file=cls_file)

            os.chdir(build_dir)
            generator.generate()
            generator.doc.generate_pdf('resume', clean_tex=False,  silent=False)
        except Exception as e:
            if(original_dir):
                os.chdir(original_dir)
            return False, f"LaTeX compilation failed: {e}"

        finally:
            # Change back to the original directory, even if there's an error
            os.chdir(original_dir)
            return True, "PDF compiled"

    def build_pipeline(self, yaml_file, tex_file, cls_file):
        steps = [
            (self.copy_files, [tex_file, cls_file]),
            (self.compile_pdf, [tex_file, cls_file]),
        ]
        for func, args in steps:
            success, msg = func(*args)
            if not success:
                return False, msg
        return True, "Build pipeline completed"
