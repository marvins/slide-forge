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
- [ ] **Post-Phase Update**: Update README, design docs, and Jupyter Book

### Phase 2: Advanced Features
- [ ] Theme preservation
- [ ] Image handling
- [ ] Math equation support
- [ ] Custom styling options
- [ ] **Post-Phase Update**: Update README, design docs, and Jupyter Book

### Phase 3: Professional Features
- [ ] TikZ diagram support
- [ ] Advanced LaTeX commands
- [ ] Batch processing
- [ ] GUI application
- [ ] **Post-Phase Update**: Update README, design docs, and Jupyter Book

## Post-Phase Update Guidelines

After completing each development phase, perform these updates to keep documentation synchronized:

### 📝 Update README.md
- [ ] Update feature checkboxes (mark completed items)
- [ ] Update Quick Start section with new capabilities
- [ ] Add new usage examples for implemented features
- [ ] Update installation requirements if new dependencies were added
- [ ] Refresh project structure if new modules were created

### 📚 Update Jupyter Book (`docs/book/`)
- [x] Update API reference documentation in `api/` directory
- [ ] Create new tutorial notebooks for implemented features
- [ ] Add new examples to `examples/` directory
- [x] Update configuration files if new Sphinx extensions are needed
- [x] Test local build with `jupyter-book build docs/book`
- [x] Update table of contents (`_toc.yml`) with new content
- [x] Set up basic auto-generated API documentation (currently manual, will be fully automated as modules are implemented)

### 🔄 Sync Checklist
- [ ] All code examples in documentation work with current implementation
- [ ] API documentation matches actual code signatures
- [ ] Installation instructions are up-to-date
- [ ] Feature lists are accurate (no promised but unimplemented features)
- [ ] Links between documents are working
- [ ] Version numbers and dates are current

### 📋 Documentation Review
- [ ] Read through all updated sections for clarity
- [ ] Test code examples in a fresh environment
- [ ] Verify cross-references and links
- [ ] Check for consistency in terminology and formatting
- [ ] Ensure all new content follows project documentation standards

---

## TODO: Documentation Setup

### 1. Create Jupyter Book Structure
- [x] Install Jupyter Book dependencies: `pip install jupyter-book sphinx`
- [x] Initialize Jupyter Book in `docs/book/` directory
- [x] Create `_config.yml` with Sphinx extensions for API docs
- [x] Create `_toc.yml` with book structure (intro, API, tutorials, examples)
- [x] Convert existing `docs/class-diagrams.md` to Jupyter Book format
- [ ] Create interactive tutorial notebooks for basic conversion
- [x] Set up auto-generated API documentation from docstrings
- [x] Test local build with `jupyter-book build docs/book`

### 2. Setup GitHub Actions for Auto-Deployment
- [x] Create `.github/workflows/docs.yml` workflow file
- [x] Configure workflow to trigger on push to `main` branch
- [x] Set up Python environment and install dependencies
- [x] Add Jupyter Book build step
- [x] Configure GitHub Pages deployment to `gh-pages` branch
- [x] Add PR preview functionality (optional)
- [ ] Test workflow with sample documentation changes
- [ ] Configure GitHub repository settings for GitHub Pages
- [ ] Verify documentation is accessible at `https://marvins.github.io/slide-forge/`

---

## Documentation Deployment

### Automatic Documentation

Slide Forge uses GitHub Actions to automatically build and deploy documentation:

#### **Triggers**
- **Push to `main`**: Builds and deploys to GitHub Pages
- **Pull Requests**: Builds and provides preview with download link

#### **What Gets Built**
- Jupyter Book with all documentation pages
- Auto-generated API documentation
- Class diagrams and architecture docs
- Installation and quick start guides

#### **Deployment URL**
Once deployed, documentation is available at:
`https://marvins.github.io/slide-forge/`

#### **Local Development**
To build documentation locally:
```bash
cd docs/book
jupyter-book build --html
jupyter-book start  # Serve on http://localhost:3000
```

#### **Workflow Features**
- ✅ **Cached dependencies** for faster builds
- ✅ **PR previews** with download links
- ✅ **Documentation quality checks**
- ✅ **Broken link detection**
- ✅ **Coverage verification**

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
