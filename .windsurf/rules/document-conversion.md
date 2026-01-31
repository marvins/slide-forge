---
description: Document Conversion Workflow Rules
---

# Document Conversion Workflow Rules

This document provides comprehensive rules and best practices for the document conversion system that handles PowerPoint, LaTeX (Beamer), and Markdown (Marp) formats.

## Core Conversion Workflows

### PowerPoint to PDF Workflow
```bash
make pptx2pdf
```
- Converts PowerPoint files to LaTeX Beamer
- Compiles LaTeX to PDF with XeLaTeX
- Outputs to `output/` directory
- Handles image extraction and theme application

### PowerPoint to Markdown Workflow
```bash
make pptx2md
```
- Converts PowerPoint to Marp-compatible Markdown
- Preserves bullet points and indentation
- Extracts images to `pptx/` directory
- Includes Marp frontmatter

### Beamer to PDF Workflow
```bash
make beamer2pdf
```
- Builds existing LaTeX Beamer presentations
- Uses UASLP-inspired theme by default
- Outputs to `output/` directory
- Handles custom fonts and colors

### Beamer to PowerPoint Workflow
```bash
make beamer2pptx
```
- Converts LaTeX Beamer to PowerPoint format
- Uses existing converter as stub implementation
- Copies generated PPTX to `output/` directory

## Directory Structure

```
Document-Experiments/
├── pptx/                    # PowerPoint files and conversions
│   ├── *.pptx              # Input PowerPoint files
│   ├── *.md                # Generated Markdown files
│   ├── *.tex               # Generated LaTeX files
│   └── *.png               # Extracted images
├── latex/                   # LaTeX presentations
│   ├── *.tex               # Beamer presentations
│   └── images/             # Presentation images
├── build/                   # LaTeX compilation artifacts
├── output/                  # Final outputs (PDFs, PPTX)
├── ppt_converter.py         # Main conversion script
├── Makefile                # Build system
└── requirements.txt        # Python dependencies
```

## File Management Rules

### Input Files
- **PowerPoint**: Place in `pptx/` directory
- **LaTeX**: Place in `latex/` directory
- **Markdown**: Generated automatically

### Output Files
- **PDFs**: Always go to `output/` directory
- **PPTX**: Copy to `output/` directory when generated
- **Images**: Extracted to respective directories

### Cleanup Rules
```bash
make clean      # Remove auxiliary files
make distclean  # Remove all generated files
```

## Conversion Features

### PowerPoint Processing
- **Text Extraction**: Preserves slide content and structure
- **Image Extraction**: Automatically saves images as PNG files
- **Theme Analysis**: Extracts colors, fonts, and styling
- **Bullet Detection**: Preserves PowerPoint bullet structure
- **Title Extraction**: Attempts to extract slide titles (partial)

### LaTeX Generation
- **Beamer Support**: Complete Beamer document structure
- **Custom Themes**: Auto-generated based on PowerPoint analysis
- **Font Handling**: Helvetica font support
- **Color Schemes**: Custom color definitions
- **TikZ Diagrams**: Architecture and flow diagrams

### Markdown Generation
- **Marp Compatibility**: Full Marp frontmatter support
- **Slide Separators**: Proper `---` separators
- **Bullet Points**: Multi-level bullet preservation
- **Image References**: Automatic image linking

## Theme System

### UASLP-Inspired Theme
- **Colors**: Deep blue headers, gray body, orange accents
- **Fonts**: Helvetica font family
- **Layout**: Clean title slides, underlined frame titles
- **Blocks**: Custom styled alert and example blocks

### Custom Theme Generation
- **Automatic Analysis**: Extracts colors from PowerPoint
- **Font Size Detection**: Analyzes text sizing
- **Color Mapping**: Maps PowerPoint colors to LaTeX equivalents
- **Layout Optimization**: Clean, professional appearance

## Build System Rules

### Makefile Targets
- **Primary**: `make beamer2pdf`, `make pptx2pdf`, `make pptx2md`
- **Utility**: `make clean`, `make help`, `make config`
- **Development**: `make quick`, `make view`, `make watch`

### Virtual Environment
- **Activation**: Automatically sourced for all Python commands
- **Dependencies**: Managed through `requirements.txt`
- **Isolation**: Clean separation from system Python

## Error Handling

### Common Issues
- **Missing Images**: Check image paths and directory structure
- **Font Issues**: Ensure font packages are installed
- **Compilation Errors**: Check LaTeX logs for specific errors
- **Permission Issues**: Verify file and directory permissions

### Debugging
- **Verbose Mode**: Use `-v` flag with converter
- **Configuration**: Use `make config` to check file detection
- **Logs**: Check LaTeX compilation logs in `build/` directory

## Best Practices

### File Organization
- Keep input files in appropriate directories
- Use descriptive filenames
- Regular cleanup of generated files
- Version control important source files

### Conversion Workflow
- Test conversions with small files first
- Verify output quality before large conversions
- Check image extraction and placement
- Validate theme application

### Performance
- Use `make quick` for rapid development iterations
- Batch process multiple files when possible
- Clean build directory regularly

## Troubleshooting

### PowerPoint Issues
- **Corrupted Files**: Try opening in PowerPoint first
- **Complex Layouts**: May require manual adjustment
- **Embedded Media**: Check extraction success
- **Password Protection**: Remove before conversion

### LaTeX Issues
- **Package Errors**: Install missing LaTeX packages
- **Font Errors**: Check font availability
- **Compilation**: Review LaTeX error messages
- **Encoding**: Ensure UTF-8 encoding

### Markdown Issues
- **Marp Rendering**: Validate Marp syntax
- **Image Paths**: Check relative path references
- **Frontmatter**: Verify YAML syntax
- **Special Characters**: Check encoding issues

## Integration Examples

### Git Workflow
```bash
git add .
git commit -m "Update presentation with UASLP theme"
git push origin main
```

### Documentation Updates
- Update README.md with new features
- Document custom theme changes
- Update help text in Makefile
- Add examples to documentation
