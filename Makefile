# Build cross-platform binary using PyInstaller
binary: check
	$(PYTHON) pip install pyinstaller
	$(PYTHON) -m PyInstaller --onefile --windowed --name cvgen gui_resume.py
	@echo "Binary built in dist/cvgen. Supports CLI and GUI."
# Cross-platform Makefile for building the resume


RESUME_YAML=resume.yaml
RESUME_TEX=resume.tex
BUILD_DIR=build
LATEX=xelatex
PYTHON=uv
CLS_DIR=cls
CLS_TEMPLATE?=$(CLS_DIR)/deedy-resume.cls


all: check $(BUILD_DIR)/resume.pdf

check:
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo "Python3 is required but not installed."; exit 1; }
	@command -v $(LATEX) >/dev/null 2>&1 || { echo "XeLaTeX is required but not installed."; exit 1; }


$(RESUME_TEX): $(RESUME_YAML) generate_resume.py
	$(PYTHON) pip install -r requirements.txt
	$(PYTHON) python generate_resume.py


$(BUILD_DIR)/resume.pdf: $(RESUME_TEX) $(CLS_TEMPLATE)
	@mkdir -p $(BUILD_DIR)
	cp $(CLS_TEMPLATE) $(BUILD_DIR)/
	cp $(RESUME_TEX) $(BUILD_DIR)/
	cd $(BUILD_DIR) && $(LATEX) resume.tex && $(LATEX) resume.tex


clean:
	rm -rf $(BUILD_DIR)/*.aux $(BUILD_DIR)/*.log $(BUILD_DIR)/*.out $(BUILD_DIR)/*.pdf $(RESUME_TEX)


.PHONY: all clean check
