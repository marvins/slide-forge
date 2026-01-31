# Installation

This guide will help you install Slide Forge on your system.

## System Requirements

- **Python 3.8 or higher**
- **pip** (Python package manager)
- **Optional**: Git for cloning the repository

## Installation Methods

### Method 1: Install from PyPI (Recommended)

```bash
# Install the latest stable version
pip install slide-forge

# Or install with optional dependencies
pip install slide-forge[dev]  # Development tools
pip install slide-forge[docs]  # Documentation tools
```

### Method 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/marvins/slide-forge.git
cd slide-forge

# Install in development mode
pip install -e .
```

### Method 3: Install from GitHub

```bash
# Install directly from GitHub
pip install git+https://github.com/marvins/slide-forge.git
```

## Verification

After installation, verify that Slide Forge is working correctly:

### Command Line
```bash
slide-forge --version
slide-forge --help
```

### Python
```python
from slideforge import Slide_Forge
print("Slide Forge imported successfully!")
```

## Dependencies

Slide Forge automatically installs its core dependencies:

- **python-pptx** - PowerPoint file creation
- **pyparsing** - LaTeX parsing
- **Pillow** - Image processing
- **click** - Command-line interface

### Optional Dependencies

For development:
```bash
pip install slide-forge[dev]
```
Includes:
- pytest (testing)
- black (code formatting)
- flake8 (linting)
- mypy (type checking)

For documentation:
```bash
pip install slide-forge[docs]
```
Includes:
- jupyter-book
- sphinx
- myst-parser

## Troubleshooting

### Common Issues

#### 1. Python Version Error
```
ERROR: Package requires a different Python
```
**Solution**: Upgrade to Python 3.8 or higher:
```bash
python3.8 -m pip install slide-forge
```

#### 2. Permission Denied
```
ERROR: Could not install packages due to an EnvironmentError
```
**Solution**: Use user installation:
```bash
pip install --user slide-forge
```

#### 3. Import Error
```python
ModuleNotFoundError: No module named 'slideforge'
```
**Solution**: Check your Python path and installation:
```bash
python -c "import sys; print(sys.path)"
which python
pip show slide-forge
```

### Platform-Specific Notes

#### Windows
- Use PowerShell or Command Prompt
- Consider using Windows Subsystem for Linux (WSL)
- Some LaTeX features may require MiKTeX or TeX Live

#### macOS
- Use the built-in Python or install from Homebrew
- Xcode command line tools may be required for some dependencies

#### Linux
- Use your distribution's package manager for Python
- Consider using virtual environments for isolation

## Virtual Environment Setup (Recommended)

For a clean installation, use a virtual environment:

```bash
# Create virtual environment
python3 -m venv slide-forge-env

# Activate it
# On macOS/Linux:
source slide-forge-env/bin/activate
# On Windows:
slide-forge-env\Scripts\activate

# Install Slide Forge
pip install slide-forge

# Deactivate when done
deactivate
```

## Next Steps

After successful installation:

1. 📖 Read the [Quick Start Guide](quickstart.md)
2. 🧪 Try the [Basic Tutorial](tutorials/basic-conversion.md)
3. 📚 Explore the [API Reference](api/)
4. 🎯 Check out [Examples](examples/)

---

Having trouble? Check our [Troubleshooting Guide](reference/troubleshooting.md) or open an issue on GitHub.
