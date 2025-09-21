
# Installation Instructions

## Prerequisites
- Python 3
- XeTeX (or LuaTeX)
- [uv](https://github.com/astral-sh/uv) for Python packages

## Install LaTeX and Fonts

### Arch Linux
```sh
sudo pacman -S texlive-core texlive-fontsextra tk
```

### Ubuntu/Debian
```sh
sudo apt-get install texlive-xetex texlive-fonts-extra python3-tk
```

### Fedora
```sh
sudo dnf install texlive-xetex texlive-collection-fontsrecommended python3-tkinter
```

### Windows
- Download and install [TeX Live](https://www.tug.org/texlive/).
- Ensure XeTeX or LuaTeX is available in PATH.
- Fonts: Install any required fonts manually (see README or font list in resume.tex).
- Tkinter is usually included with Python, but if you see errors, refer to your Python distribution's documentation.

### macOS
```sh
brew install --cask mactex
```

### Fonts
- Make sure to install any custom fonts referenced in `deedy-resume.cls` or `resume.tex`.
- On Linux, you can usually install fonts via your package manager or by copying them to `~/.fonts` and running `fc-cache -fv`.

## Install Python Dependencies
```sh
uv pip install -r pyproject.toml
```

## Run the GUI Editor
```sh
uv run python3 -m latexcv
```

## Build the PDF Resume
Recommended:
```sh
make
```

## Build a cross-platform binary (CLI/GUI)
```sh
make binary
```
The binary will be in `dist/cvgen` (Linux/macOS) or `dist/cvgen.exe` (Windows).

## Run the binary
GUI mode (default):
```sh
./dist/cvgen
```
CLI mode:
```sh
./dist/cvgen --cli --yaml resume.yaml --tex resume.tex --cls deedy-resume.cls
```

## Clean Build Artifacts
```sh
make clean
```
