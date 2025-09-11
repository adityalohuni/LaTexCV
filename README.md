
# CV Generator

A cross-platform, YAML-driven resume generator using LaTeX. Edit your resume in YAML, generate a PDF, and preview it with a GUI or CLI.

## Features
- Edit your resume in `resume.yaml`
- Generate `resume.tex` and PDF automatically
- GUI editor with live PDF preview
- CLI for automated builds
- Cross-platform build pipeline (Linux, macOS, Windows)
- Build standalone binary for CLI/GUI usage

## Quick Start

1. **Install dependencies**
   - Python 3
   - XeTeX (or LuaTeX)
   - [uv](https://github.com/astral-sh/uv) for Python packages

2. **Install Python packages**
   ```sh
   uv pip install -r requirements.txt
   ```

3. **Edit your resume**
   - Edit `resume.yaml` directly, or use the GUI:
   ```sh
   uv run python3 gui_resume.py
   ```

4. **Build your PDF resume**
   - With Makefile (recommended):
   ```sh
   make
   ```

5. **Build a cross-platform binary (CLI/GUI)**
   - With Makefile:
   ```sh
   make binary
   ```
   - The binary will be in `dist/cvgen` (Linux/macOS) or `dist/cvgen.exe` (Windows).

6. **Run the binary**
   - GUI mode (default):
   ```sh
   ./dist/cvgen
   ```
   - CLI mode:
   ```sh
   ./dist/cvgen --cli --yaml resume.yaml --tex resume.tex --cls deedy-resume.cls
   ```

7. **Clean build artifacts**
   ```sh
   make clean
   ```

## GUI Editor
- The GUI requires the system `tk` library (see INSTALL.md for instructions).
- Run `uv run python3 gui_resume.py` to edit your YAML and preview the PDF live.
- Requires `pdf2image` and `Pillow` (installed via `requirements.txt`).

## Installation
See `INSTALL.md` for full instructions on installing XeTeX/LuaTeX and required fonts for your OS.

---

Contributions and suggestions welcome!
