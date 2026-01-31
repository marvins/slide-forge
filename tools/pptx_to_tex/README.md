# PPTX to LaTeX Tools

Legacy tools for converting PowerPoint presentations to LaTeX Beamer format.

## Files

- `Makefile` - Build system with conversion targets
- `ppt_converter.py` - Original bidirectional converter
- `enhanced_pptx_converter.py` - Advanced parser with better LaTeX handling
- `latex_to_pptx.py` - LaTeX to PowerPoint conversion script

## Usage

### Using Makefile
```bash
cd tools/pptx_to_tex
make pptx2md    # PowerPoint to Markdown
make pptx2pdf   # PowerPoint to LaTeX → PDF
make clean     # Clean generated files
```

### Direct Python Usage
```bash
python ppt_converter.py input.pptx md    # PowerPoint to Markdown
python ppt_converter.py input.pptx tex   # PowerPoint to LaTeX
python enhanced_pptx_converter.py         # Advanced LaTeX to PowerPoint
```

## Note

These tools were the foundation for the Slide Forge project. For new development, see the main `slideforge` package in `src/slideforge/`.
