
# Makefile for LaTeX presentation compilation
# Supports both pdfLaTeX and XeLaTeX compilation

# Variables
LATEX_ENGINE = xelatex
LATEX_FLAGS = -interaction=nonstopmode -shell-escape
BIB_ENGINE = bibtex
GLOSSARY_ENGINE = makeglossaries

# Default target
.PHONY: all clean help pdf view watch

# Find all .tex files in the current directory and subdirectories
TEX_FILES := $(wildcard **/*.tex *.tex)
# Get the main .tex file (prefer pptx/ directory)
MAIN_TEX := $(firstword $(wildcard pptx/*.tex))
# Fallback to any .tex file if none in pptx/
ifeq ($(MAIN_TEX),)
    MAIN_TEX := $(firstword $(TEX_FILES))
endif
# Default main file if no .tex files found
ifeq ($(MAIN_TEX),)
    MAIN_TEX = main.tex
endif

# Output directory
BUILD_DIR = build
OUTPUT_DIR = output

# All targets
all: pdf

# Help target
help:
	@echo "Available targets:"
	@echo "  all        - Build PDF (default)"
	@echo "  pdf        - Build PDF using $(LATEX_ENGINE)"
	@echo "  pdflatex   - Build PDF using pdfLaTeX"
	@echo "  xelatex    - Build PDF using XeLaTeX"
	@echo "  lualatex   - Build PDF using LuaLaTeX"
	@echo "  pptx2pdf   - Convert PowerPoint to LaTeX and build PDF"
	@echo "  pptx2md    - Convert PowerPoint to Markdown"
	@echo "  pptx       - Convert PowerPoint to both Markdown and LaTeX"
	@echo "  convert-md - Convert PowerPoint to Markdown"
	@echo "  convert-tex- Convert PowerPoint to LaTeX"
	@echo "  clean      - Remove auxiliary files"
	@echo "  distclean  - Remove all generated files including PDFs"
	@echo "  view       - Open PDF in default viewer"
	@echo "  watch      - Watch for changes and recompile automatically"
	@echo "  install-deps - Install required LaTeX packages"
	@echo ""
	@echo "Variables:"
	@echo "  MAIN_TEX   - Main LaTeX file (currently: $(MAIN_TEX))"
	@echo "  LATEX_ENGINE - LaTeX engine to use (currently: $(LATEX_ENGINE))"

# Create directories
$(BUILD_DIR) $(OUTPUT_DIR):
	@mkdir -p $@

# PDF compilation with specified engine
pdf: $(BUILD_DIR) $(OUTPUT_DIR)
	@echo "Building $(MAIN_TEX) with $(LATEX_ENGINE)..."
	@cp pptx/*.png $(BUILD_DIR)/ 2>/dev/null || true
	@cd $(BUILD_DIR) && $(LATEX_ENGINE) $(LATEX_FLAGS) ../$(MAIN_TEX)
	@cp $(BUILD_DIR)/$(basename $(MAIN_TEX)).pdf $(OUTPUT_DIR)/ 2>/dev/null || true
	@echo "PDF created in $(OUTPUT_DIR)/"

# Specific engine targets
pdflatex: LATEX_ENGINE = pdflatex
pdflatex: pdf

xelatex: LATEX_ENGINE = xelatex
xelatex: pdf

lualatex: LATEX_ENGINE = lualatex
lualatex: pdf

# Full compilation with bibliography and glossaries
full: $(BUILD_DIR) $(OUTPUT_DIR)
	@echo "Full compilation of $(MAIN_TEX)..."
	@cp pptx/*.png $(BUILD_DIR)/ 2>/dev/null || true
	@cd $(BUILD_DIR) && $(LATEX_ENGINE) $(LATEX_FLAGS) ../$(MAIN_TEX)
	@if grep -q "\\bibliography" ../$(MAIN_TEX); then \
		echo "Running bibliography..."; \
		cd $(BUILD_DIR) && $(BIB_ENGINE) $(basename $(MAIN_TEX)); \
	fi
	@if grep -q "\\makeglossaries" ../$(MAIN_TEX); then \
		echo "Running glossaries..."; \
		cd $(BUILD_DIR) && $(GLOSSARY_ENGINE) $(basename $(MAIN_TEX)); \
	fi
	@cd $(BUILD_DIR) && $(LATEX_ENGINE) $(LATEX_FLAGS) ../$(MAIN_TEX)
	@cd $(BUILD_DIR) && $(LATEX_ENGINE) $(LATEX_FLAGS) ../$(MAIN_TEX)
	@cp $(BUILD_DIR)/$(basename $(MAIN_TEX)).pdf $(OUTPUT_DIR)/ 2>/dev/null || true
	@echo "Full compilation complete. PDF in $(OUTPUT_DIR)/"

# Clean auxiliary files
clean:
	@echo "Cleaning auxiliary files..."
	@rm -rf $(BUILD_DIR)
	@rm -f *.aux *.log *.out *.toc *.nav *.snm *.vrb *.bbl *.blg *.fls *.fdb_latexmk
	@rm -f *.synctex.gz *.figlist *.makefile *.fls *.fdb_latexmk *.auxlock
	@rm -f *.acn *.acr *.alg *.glg *.glo *.gls *.glsdefs *.ist *.xdy
	@rm -f slide_*.png
	@find . -name "*.aux" -delete
	@find . -name "*.log" -delete
	@find . -name "*.out" -delete
	@echo "Clean complete."

# Remove all generated files
distclean: clean
	@echo "Removing all generated files..."
	@rm -rf $(OUTPUT_DIR)
	@rm -f *.pdf
	@find . -name "*.pdf" -delete
	@echo "Distclean complete."

# View PDF
view: pdf
	@if command -v xdg-open > /dev/null 2>&1; then \
		xdg-open $(OUTPUT_DIR)/$(basename $(MAIN_TEX)).pdf; \
	elif command -v open > /dev/null 2>&1; then \
		open $(OUTPUT_DIR)/$(basename $(MAIN_TEX)).pdf; \
	else \
		echo "Could not determine PDF viewer. Please open $(OUTPUT_DIR)/$(basename $(MAIN_TEX)).pdf manually."; \
	fi

# Watch for changes and recompile
watch:
	@echo "Watching for changes in .tex files..."
	@if command -v inotifywait > /dev/null 2>&1; then \
		while inotifywait -e modify **/*.tex *.tex; do \
			echo "Change detected, recompiling..."; \
			$(MAKE) pdf; \
		done; \
	elif command -v fswatch > /dev/null 2>&1; then \
		fswatch -o **/*.tex *.tex | while read event; do \
			echo "Change detected, recompiling..."; \
			$(MAKE) pdf; \
		done; \
	else \
		echo "Neither inotifywait nor fswatch found. Please install one for watch functionality."; \
		echo "On Ubuntu/Debian: sudo apt-get install inotify-tools"; \
		echo "On macOS: brew install fswatch"; \
	fi

# Install LaTeX dependencies (works with texlive)
install-deps:
	@echo "Installing LaTeX packages..."
	@if command -v tlmgr > /dev/null 2>&1; then \
		tlmgr install beamer graphicx hyperref inputenc fontenc \
			geometry amsmath amssymb listings xcolor bookmark \
			cleveref biblatex glossaries minted; \
	else \
		echo "tlmgr not found. Please install TeX Live or use your package manager."; \
		echo "On Ubuntu/Debian: sudo apt-get install texlive-full"; \
		echo "On macOS: brew install --cask mactex"; \
	fi

# Convert PowerPoint to formats (requires ppt_converter.py)
pptx2pdf: convert-tex pdf
	@echo "PowerPoint → LaTeX → PDF complete!"

pptx2md: convert-md
	@echo "PowerPoint → Markdown complete!"
	@echo "Markdown files are in pptx/ directory"

pptx: convert-md convert-tex

convert-md:
	@echo "Converting PowerPoint to Markdown..."
	@for file in pptx/*.pptx; do \
		bash -c "source venv/bin/activate && python3 ppt_converter.py \"$$file\" md"; \
	done

convert-tex:
	@echo "Converting PowerPoint to LaTeX..."
	@for file in pptx/*.pptx; do \
		bash -c "source venv/bin/activate && python3 ppt_converter.py \"$$file\" tex"; \
	done

convert-all: convert-md convert-tex

# Quick build for development (faster, no bibliography)
quick: $(BUILD_DIR)
	@echo "Quick build of $(MAIN_TEX)..."
	@cp pptx/*.png $(BUILD_DIR)/ 2>/dev/null || true
	@cd $(BUILD_DIR) && $(LATEX_ENGINE) $(LATEX_FLAGS) -draftmode ../$(MAIN_TEX)
	@cd $(BUILD_DIR) && $(LATEX_ENGINE) $(LATEX_FLAGS) ../$(MAIN_TEX)
	@cp $(BUILD_DIR)/$(basename $(MAIN_TEX)).pdf . 2>/dev/null || true
	@echo "Quick build complete."

# Show current configuration
config:
	@echo "Current configuration:"
	@echo "  Main file: $(MAIN_TEX)"
	@echo "  LaTeX engine: $(LATEX_ENGINE)"
	@echo "  Build directory: $(BUILD_DIR)"
	@echo "  Output directory: $(OUTPUT_DIR)"
	@echo "  Available .tex files: $(TEX_FILES)"
