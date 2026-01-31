# Makefile for building Beamer presentations

# Variables
TEX_FILE = sample_presentation
BUILD_DIR = build
PDF_FILE = $(BUILD_DIR)/$(TEX_FILE).pdf
AUX_FILE = $(BUILD_DIR)/$(TEX_FILE).aux
LOG_FILE = $(BUILD_DIR)/$(TEX_FILE).log
NAV_FILE = $(BUILD_DIR)/$(TEX_FILE).nav
OUT_FILE = $(BUILD_DIR)/$(TEX_FILE).out
SNM_FILE = $(BUILD_DIR)/$(TEX_FILE).snm
TOC_FILE = $(BUILD_DIR)/$(TEX_FILE).toc
VDB_FILE = $(BUILD_DIR)/$(TEX_FILE).vrb
FLS_FILE = $(BUILD_DIR)/$(TEX_FILE).fls
FDB_FILE = $(BUILD_DIR)/$(TEX_FILE).fdb_latexmk

# Default target
all: $(PDF_FILE)

# Main compilation rule
$(PDF_FILE): $(TEX_FILE).tex images/*.png | $(BUILD_DIR)
	@echo "Building $(TEX_FILE).pdf..."
	pdflatex -output-directory $(BUILD_DIR) $(TEX_FILE)
	@if [ -f $(AUX_FILE) ]; then pdflatex -output-directory $(BUILD_DIR) $(TEX_FILE); fi
	@if [ -f $(AUX_FILE) ]; then pdflatex -output-directory $(BUILD_DIR) $(TEX_FILE); fi
	@echo "Build complete: $(PDF_FILE)"

# Create build directory
$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)

# Create sample images
images:
	@echo "Creating sample images..."
	cd images && python3 create_sample_images.py
	@echo "Sample images created"

# Clean auxiliary files
clean:
	@echo "Cleaning auxiliary files..."
	rm -f $(AUX_FILE) $(LOG_FILE) $(NAV_FILE) $(OUT_FILE) $(SNM_FILE) $(TOC_FILE) $(VDB_FILE) $(FLS_FILE) $(FDB_FILE)
	@echo "Clean complete"

# Clean everything including PDF
clean-all: clean
	@echo "Cleaning all generated files..."
	rm -f $(PDF_FILE)
	@echo "All files cleaned"

# Force rebuild
rebuild: clean-all all

# View the PDF (macOS)
view: $(PDF_FILE)
	open $(PDF_FILE)

# Check for required tools
check:
	@echo "Checking for required tools..."
	@which pdflatex > /dev/null || (echo "Error: pdflatex not found. Please install TeX Live or MiKTeX." && exit 1)
	@which python3 > /dev/null || (echo "Error: python3 not found." && exit 1)
	@echo "All required tools found"

# Help target
help:
	@echo "Available targets:"
	@echo "  all       - Build the PDF (default)"
	@echo "  images    - Create sample images"
	@echo "  clean     - Remove auxiliary files"
	@echo "  clean-all - Remove all generated files"
	@echo "  rebuild   - Clean and rebuild"
	@echo "  view      - Build and open PDF (macOS)"
	@echo "  check     - Check for required tools"
	@echo "  help      - Show this help"

# Declare phony targets
.PHONY: all images clean clean-all rebuild view check help $(BUILD_DIR)

# Default goal
.DEFAULT_GOAL := all
