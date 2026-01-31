# Slide Forge

LaTeX Beamer to PowerPoint converter - Transform your academic presentations into professional PowerPoint slides.

## Quick Start

### Installation

```bash
pip install slide-forge
```

### Basic Usage

```bash
# Convert LaTeX Beamer to PowerPoint
slide-forge -i presentation.tex -o presentation.pptx

# With options
slide-forge -i slides.tex -o slides.pptx --theme professional --verbose
```

### Python API

```python
from slideforge import SlideForge

forge = SlideForge()
success = forge.convert_file("presentation.tex", "presentation.pptx")

if success:
    print("Conversion successful!")
```

## Features

- ✅ **LaTeX Beamer parsing** - Handles frames, blocks, itemize, etc.
- ✅ **Professional PowerPoint output** - Clean, formatted slides
- ✅ **Image support** - Extract and include LaTeX images
- ✅ **Theme preservation** - Maintain LaTeX styling in PowerPoint
- ✅ **Command-line interface** - Easy to use CLI tool
- ✅ **Python library** - Integrate into your workflows

## Project Structure

```
slide-forge/
├── src/slideforge/
│   ├── __init__.py
│   ├── core.py              # Main API
│   ├── parser.py            # LaTeX parsing (TODO)
│   ├── mapper.py            # Content mapping (TODO)
│   ├── builder.py           # PowerPoint building (TODO)
│   └── apps/
│       ├── __init__.py
│       └── cli.py           # Command-line interface
├── tests/                   # Test suite
├── docs/                    # Documentation
├── pyproject.toml          # Package configuration
└── README.md
```

## Development

### Setup

```bash
# Clone repository
git clone https://github.com/slideforge/slide-forge
cd slide-forge

# Install in development mode
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Quality

```bash
black src/
flake8 src/
mypy src/
```

## Architecture

Slide Forge follows a modular architecture:

1. **Parser** - Extracts structure from LaTeX Beamer files
2. **Mapper** - Maps LaTeX elements to PowerPoint equivalents  
3. **Builder** - Creates PowerPoint presentations using python-pptx

See [docs/class-diagrams.md](docs/class-diagrams.md) for detailed architecture diagrams.

## Roadmap

### Phase 1: Core Functionality
- [x] Basic project structure
- [x] CLI interface
- [ ] LaTeX parser implementation
- [ ] PowerPoint builder implementation
- [ ] Basic conversion workflow

### Phase 2: Advanced Features
- [ ] Theme preservation
- [ ] Image handling
- [ ] Math equation support
- [ ] Custom styling options

### Phase 3: Professional Features
- [ ] TikZ diagram support
- [ ] Advanced LaTeX commands
- [ ] Batch processing
- [ ] GUI application

## Contributing

Contributions welcome! Please see our [contributing guidelines](CONTRIBUTING.md).

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Citation

If you use Slide Forge in your research, please cite:

```
Slide Forge: LaTeX Beamer to PowerPoint Converter
https://github.com/slideforge/slide-forge
```
