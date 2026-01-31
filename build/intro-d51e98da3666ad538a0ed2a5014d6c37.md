# Slide Forge Documentation

Welcome to the official documentation for **Slide Forge** - a powerful tool that converts LaTeX Beamer presentations into professional PowerPoint slides.

## What is Slide Forge?

Slide Forge is a Python library and command-line tool that transforms academic presentations from LaTeX Beamer format to PowerPoint (.pptx) format. It preserves the structure, styling, and content of your presentations while making them accessible in Microsoft PowerPoint.

## Key Features

- 🎯 **Accurate Conversion** - Maintains slide structure, titles, and content organization
- 🎨 **Style Preservation** - Preserves LaTeX styling and formatting in PowerPoint
- 🖼️ **Image Support** - Extracts and includes images from LaTeX presentations
- 🔧 **Flexible Options** - Multiple themes and customization options
- 📚 **Easy Integration** - Both CLI tool and Python library
- 🚀 **Fast Processing** - Efficient conversion workflow

## Who is this for?

- **Academics** who need to share LaTeX presentations with colleagues using PowerPoint
- **Students** converting thesis presentations for job talks
- **Researchers** preparing conference presentations
- **Anyone** needing to bridge the LaTeX-PowerPoint gap

## How to Use This Documentation

### 📖 **Reading Path**
1. **New Users** → Start with [Getting Started](getting-started.md)
2. **Quick Start** → Jump to [Quick Start Guide](quickstart.md)
3. **Developers** → Check the [API Reference](api/)
4. **Examples** → Browse [Examples](examples/) for real-world usage

### 🔧 **Interactive Tutorials**
Our tutorial notebooks include executable code cells that you can run directly in your browser or local environment. Look for the 📚 icon to identify interactive content.

### 📚 **Navigation**
- Use the table of contents on the left to navigate between sections
- Search functionality helps you find specific topics quickly
- Cross-references link related concepts throughout the documentation

## Quick Example

```python
from slideforge import Slide_Forge

# Initialize the converter
converter = Slide_Forge()

# Convert a LaTeX Beamer presentation
success = converter.convert_file(
    "presentation.tex", 
    "presentation.pptx",
    theme="professional",
    preserve_colors=True
)

if success:
    print("Conversion successful!")
```

## Getting Help

- 📖 **Documentation** - You're here now!
- 🐛 **Issues** - [GitHub Issues](https://github.com/marvins/slide-forge/issues)
- 💬 **Discussions** - [GitHub Discussions](https://github.com/marvins/slide-forge/discussions)
- 📧 **Contact** - slide-forge@example.com

## Contributing

We welcome contributions! See the [Contributing Guide](contributing.md) for details on how to:
- Report bugs
- Request features
- Submit pull requests
- Improve documentation

---

Let's get started transforming your LaTeX presentations into PowerPoint slides!
