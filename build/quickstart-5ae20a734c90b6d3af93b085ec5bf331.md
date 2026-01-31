# Quick Start

Get up and running with Slide Forge in just a few minutes!

## Your First Conversion

### Command Line

```bash
# Basic conversion
slide-forge input.tex output.pptx

# With options
slide-forge input.tex output.pptx --theme professional --verbose

# Help
slide-forge --help
```

### Python API

```python
from slideforge import Slide_Forge

# Create converter instance
converter = Slide_Forge()

# Convert file
success = converter.convert_file("input.tex", "output.pptx")

if success:
    print("✅ Conversion successful!")
else:
    print("❌ Conversion failed")
```

## Example: Converting a Sample Presentation

Let's convert a sample LaTeX Beamer presentation:

### 1. Create a Sample LaTeX File

```latex
% sample.tex
\documentclass{beamer}
\usetheme{Madrid}
\title{Sample Presentation}
\author{Your Name}
\date{\today}

\begin{document}

\begin{frame}
\titlepage
\end{frame}

\begin{frame}{Introduction}
\begin{itemize}
\item First point
\item Second point
\item Third point
\end{itemize}
\end{frame}

\begin{frame}{Conclusion}
\begin{block}{Main Result}
Slide Forge makes LaTeX to PowerPoint conversion easy!
\end{block}
\end{frame}

\end{document}
```

### 2. Convert with Command Line

```bash
slide-forge sample.tex sample.pptx --theme professional
```

### 3. Convert with Python

```python
from slideforge import Slide_Forge

converter = Slide_Forge()
success = converter.convert_file(
    "sample.tex", 
    "sample.pptx",
    theme="professional",
    preserve_colors=True,
    verbose=True
)

print(f"Conversion status: {'Success' if success else 'Failed'}")
```

## Available Options

### Command Line Options

```bash
slide-forge [OPTIONS] INPUT_FILE OUTPUT_FILE

Options:
  --theme TEXT           PowerPoint theme (default, professional, academic, minimal)
  --preserve-colors     Preserve LaTeX colors in PowerPoint
  --include-images      Include images from LaTeX
  --verbose             Enable verbose output
  --help                Show help message
```

### Python API Options

```python
converter.convert_file(
    input_file="input.tex",
    output_file="output.pptx",
    theme="professional",        # default, professional, academic, minimal
    preserve_colors=True,       # bool
    include_images=True,         # bool
    verbose=True                 # bool
)
```

## Themes

Slide Forge offers several PowerPoint themes:

| Theme | Description | Use Case |
|-------|-------------|----------|
| `default` | Clean, simple design | General purpose |
| `professional` | Corporate styling | Business presentations |
| `academic` | Academic styling | Research presentations |
| `minimal` | Minimal design | Modern, clean look |

## What Gets Converted?

### ✅ Supported Elements
- Slide titles and frames
- Itemize and enumerate lists
- Blocks and theorems
- Text formatting (bold, italic, etc.)
- Images and figures
- Sections and subsections
- Tables (basic support)

### ⚠️ Partial Support
- Mathematical equations (converted to images)
- TikZ diagrams (exported as images)
- Complex formatting

### ❌ Not Yet Supported
- Animations and transitions
- Embedded videos
- Complex macros
- Bibliography references

## Tips for Best Results

### 1. Prepare Your LaTeX
```latex
% Use standard Beamer commands
\begin{frame}{Title}
\begin{itemize}
\item Clear structure
\item Standard commands
\item Simple formatting
\end{itemize}
\end{frame}
```

### 2. Check Image Paths
```latex
% Use relative paths
\includegraphics{images/diagram.png}

% Avoid absolute paths
% \includegraphics{/home/user/images/diagram.png}
```

### 3. Test Incrementally
```bash
# Start with simple presentation
slide-forge simple.tex simple.pptx

# Then try complex ones
slide-forge complex.tex complex.pptx
```

## Common Issues and Solutions

### Issue: Missing Images
```bash
# Solution: Include images flag
slide-forge input.tex output.pptx --include-images
```

### Issue: Colors Not Preserved
```bash
# Solution: Enable color preservation
slide-forge input.tex output.pptx --preserve-colors
```

### Issue: Conversion Fails
```bash
# Solution: Use verbose mode to debug
slide-forge input.tex output.pptx --verbose
```

## Next Steps

Now that you've successfully converted your first presentation:

1. 🎓 **Learn More** - Try the [Basic Tutorial](tutorials/basic-conversion.md)
2. 🔧 **Advanced Features** - Explore [Advanced Styling](tutorials/advanced-styling.md)
3. 📚 **API Reference** - Check the [Core API](api/core.md)
4. 🎯 **Real Examples** - See [Examples](examples/)

## Need Help?

- 📖 **Documentation** - Browse the full documentation
- 🐛 **Issues** - Report problems on GitHub
- 💬 **Discussions** - Ask questions in GitHub Discussions
- 📧 **Email** - Contact us at slide-forge@example.com

---

Ready to dive deeper? Continue with the [Basic Tutorial](tutorials/basic-conversion.md)!
