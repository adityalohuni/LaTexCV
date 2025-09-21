# LaTeXCV: YAML-Driven Resume Generator

> A modern, cross-platform resume builder powered by YAML and LaTeX. Edit your resume in YAML, generate beautiful PDFs, and preview instantly with a GUI or automate builds via CLI.

---

## Features

- **YAML-based resume editing**: All resume content is managed in `resume.yaml`.
- **Automatic PDF generation**: Converts YAML to LaTeX and compiles to PDF.
- **Live GUI editor**: Edit YAML and preview PDF instantly (Tkinter-based, with PDF preview).
- **CLI support**: Automate builds and integrate into CI/CD pipelines.
- **Cross-platform**: Works on Linux, macOS, and Windows.
- **Custom LaTeX templates**: Easily swap `.cls` files for different resume styles.
- **Binary builds**: Create standalone CLI/GUI executables for easy distribution.

---

## Quick Start

1. **Install prerequisites**
   - Python 3.13+
   - XeTeX (or LuaTeX)
   - [uv](https://github.com/astral-sh/uv) for Python package management

2. **Install Python dependencies**
   ```sh
   uv pip install -r pyproject.toml
   ```

3. **Edit your resume**
   - Directly edit `resume.yaml` or use the GUI editor:
   ```sh
   uv run python3 -m latexcv.main
   ```

4. **Build your PDF resume**
   - Recommended (Makefile):
   ```sh
   make
   ```

5. **Build a cross-platform binary (CLI/GUI)**
   ```sh
   make binary
   ```
   - Output: `dist/latexcv` (Linux/macOS) or `dist/latexcv.exe` (Windows)

6. **Run the binary**
   - GUI mode (default):
   ```sh
   ./dist/latexcv
   ```
   - CLI mode:
   ```sh
   ./dist/latexcv --yaml resume.yaml --tex resume.tex --cls cls/deedy.cls
   ```

7. **Clean build artifacts**
   ```sh
   make clean
   ```

---

## GUI Editor

- Requires system `tk` library and Python packages (`pdf2image`, `Pillow`).
- Run: `uv run python3 -m latexcv.main` (or use the binary).
- Edit YAML and preview PDF live.
- Select `.cls` template from dropdown for custom styles.

---

## CLI Usage

```sh
python3 -m latexcv.main --yaml resume.yaml --tex resume.tex --cls cls/deedy.cls
```

---

## Installation

See [`docs/INSTALL.md`](docs/INSTALL.md) for full instructions on installing XeTeX/LuaTeX, fonts, and platform-specific setup.

---

## Project Structure

- `resume.yaml` — Your resume data
- `cls/` — LaTeX class templates
- `src/` — Source code
- `build/` — Build artifacts
- `Makefile` — Build and automation
- `docs/` — Documentation

---

## Contributing

Pull requests and suggestions are welcome! See issues for ideas or improvements.

---

## License

MIT License
