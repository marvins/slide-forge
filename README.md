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
# Install pre-commit hooks (recommended)
pre-commit install

# Run checks manually
pre-commit run --all-files

# Individual tools
black src/
flake8 src/
mypy src/
```

### Pre-commit Hooks

This project uses pre-commit hooks to enforce code quality:

- **License header check** - Ensures all Python files have the proper MIT license header
- **Black formatting** - Automatic code formatting
- **Flake8 linting** - Code style checks
- **MyPy type checking** - Static type analysis

The hooks will automatically run before each commit. If they fail, the commit will be blocked until issues are resolved.

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
- [ ] Create interactive tutorial notebooks for basic conversion

### 2. Setup GitHub Actions for Auto-Deployment
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

## TODO

### High Priority

- [ ] **Improve itemize parsing to handle inline equations within items**
  - Currently: `$x^2 + y^2 = z^2$` inside `\item` is treated as plain text
  - Should: Extract inline equations from itemize list items
  - Location: `src/slideforge/parsers/latex_parser.py`
  - Test: `tests/parsers/test_latex_parser_itemize_equations.py`

### Medium Priority

- [ ] **Handle enumerate (numbered) lists**
  - Currently: Only itemize (bullet) lists are supported
  - Should: Parse `\begin{enumerate}...\end{enumerate}` environments
  - Location: `src/slideforge/parsers/latex_parser.py`

- [ ] **Improve text cleaning and LaTeX command removal**
  - Currently: Basic regex-based cleaning
  - Should: More sophisticated handling of nested commands and formatting
  - Location: `src/slideforge/parsers/latex_parser.py`

- [ ] **Add support for table environments**
  - Currently: Tables are not parsed
  - Should: Extract table structure and content
  - Location: `src/slideforge/parsers/latex_parser.py`

### Low Priority

- [ ] **Add support for figure environments**
  - Currently: `\includegraphics` is basic
  - Should: Full figure environment parsing with captions
  - Location: `src/slideforge/parsers/latex_parser.py`

- [ ] **Handle special LaTeX environments**
  - Currently: Limited environment support
  - Should: Support for theorem, proof, definition environments
  - Location: `src/slideforge/parsers/latex_parser.py`

### Test Infrastructure

- [ ] **Add more edge case test files**
  - Special characters in math mode
  - Unicode content in various contexts
  - Malformed nested environments
  - Location: `tests/parsers/test_data/edge_cases/`

- [ ] **Create performance tests**
  - Large document parsing
  - Memory usage with complex equations
  - Location: `tests/performance/`

### Equation Rendering System

- [ ] **Review and improve equation cache system**
  - Currently: Creates standalone LaTeX docs in `.equation_cache/`
  - Location: `src/slideforge/builders/powerpoint_builder.py` (lines 570-600)
  - Consider: Cache cleanup, error handling, performance optimization
  - Test: Verify equation rendering works with complex math expressions

### Code Quality

- [ ] **Add type hints throughout parser**
  - Currently: Partial type hints
  - Should: Complete type annotation
  - Location: `src/slideforge/parsers/latex_parser.py`

- [ ] **Improve error handling**
  - Currently: Basic exception handling
  - Should: More specific error types and recovery strategies
  - Location: `src/slideforge/parsers/latex_parser.py`

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
