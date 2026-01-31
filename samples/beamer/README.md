# Sample Beamer Presentation

A comprehensive LaTeX Beamer presentation demonstrating various features and capabilities.

## Files

- `sample_presentation.tex` - Main presentation file with diverse slide types
- `Makefile` - Build system for compilation and image generation
- `images/` - Directory containing sample images
  - `create_sample_images.py` - Script to generate sample images
  - `sample_chart.png` - Sample bar chart
  - `diagram1.png` - System architecture diagram
  - `diagram2.png` - Data flow diagram
  - `diagram3.png` - Results visualization
  - `thank_you.png` - Thank you graphic

## Quick Start

### Prerequisites
- LaTeX distribution (TeX Live, MiKTeX, etc.)
- Python 3 with PIL/Pillow for image generation
- Make (optional, for using the Makefile)

### Building the Presentation

#### Using Makefile (Recommended)
```bash
# Create sample images first
make images

# Build the PDF
make

# Or build everything at once
make all

# View the result (macOS)
make view

# Clean auxiliary files
make clean

# Clean everything including PDF
make clean-all
```

#### Manual Compilation
```bash
# Create images
cd images && python3 create_sample_images.py && cd ..

# Compile LaTeX (run multiple times for references)
pdflatex sample_presentation.tex
pdflatex sample_presentation.tex
pdflatex sample_presentation.tex
```

## Presentation Features

This sample includes:

### **Content Types**
- Title slide with author information
- Table of contents
- Text formatting (bold, italic, colors)
- Mathematical equations and theorems
- Code listings with syntax highlighting
- Data tables
- Images and figures
- TikZ diagrams

### **Layout Features**
- Multi-column layouts
- Blocks (standard, alert, example)
- Itemized and enumerated lists
- Nested lists
- Overlays and progressive display

### **Advanced Features**
- Mathematical environments (theorems, proofs, corollaries)
- TikZ graphics and diagrams
- Code listings with syntax highlighting
- Image inclusion and positioning
- Custom colors and themes

## Presentation Structure

1. **Introduction** - Overview of Beamer capabilities
2. **Text and Formatting** - Various text formatting options
3. **Mathematical Content** - Equations, theorems, and proofs
4. **Images and Graphics** - Image inclusion and layouts
5. **Tables and Data** - Formatted data tables
6. **Code Examples** - Syntax-highlighted code listings
7. **TikZ Graphics** - Custom vector graphics
8. **Advanced Features** - Overlays and complex layouts
9. **Conclusion** - Summary and thank you slide

## Customization

### Changing Theme
Edit the theme settings in the preamble:
```latex
\usetheme{Madrid}           % Try: Berlin, Warsaw, Copenhagen
\usecolortheme{seahorse}    % Try: beaver, crane, dolphin
```

### Adding New Slides
Follow the existing pattern:
```latex
\begin{frame}{Slide Title}
% Slide content here
\end{frame}
```

### Modifying Images
Edit `images/create_sample_images.py` or replace with your own images.

## Troubleshooting

### Common Issues

1. **Missing packages**: Install the full TeX Live distribution
2. **Image errors**: Run `make images` to generate sample images
3. **Compilation errors**: Check LaTeX log file for specific errors
4. **Font issues**: Ensure system fonts are available

### Getting Help

```bash
# Check for required tools
make check

# Show all available targets
make help
```

## Output

The compiled presentation will be saved as `sample_presentation.pdf` in the same directory.
