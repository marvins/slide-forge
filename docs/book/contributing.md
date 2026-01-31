# Contributing

We welcome contributions to Slide Forge! This document provides guidelines for contributing to the project.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Development Setup

1. Fork the repository
2. Clone your fork locally
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install in development mode:
   ```bash
   pip install -e .
   ```
5. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Running Tests

```bash
python -m pytest tests/
```

## Code Style

We use the following tools for code formatting and linting:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting

Run them before submitting:
```bash
black src/
isort src/
flake8 src/
```

## Project Structure

```
slide-forge/
├── src/slideforge/
│   ├── core.py              # Main controller
│   ├── parsers/             # Input format parsers
│   ├── builders/            # Output format builders
│   ├── mappers/             # Content mappers
│   ├── models/              # Universal data models
│   └── exceptions.py        # Custom exceptions
├── tests/                   # Test suite
├── docs/                    # Documentation
├── samples/                 # Sample files
└── scripts/                 # Utility scripts
```

## Contributing Guidelines

### Bug Reports

- Use the GitHub issue tracker
- Include:
  - Python version
  - Operating system
  - Minimal reproduction example
  - Expected vs actual behavior

### Feature Requests

- Open an issue with "Feature Request" label
- Describe the use case
- Suggest API design if applicable

### Pull Requests

1. Create a feature branch from `main`
2. Make your changes
3. Add tests for new functionality
4. Update documentation if needed
5. Ensure all tests pass
6. Submit a pull request with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots if applicable

### Development Areas

We welcome contributions in these areas:

#### New Parsers
- PowerPoint to LaTeX
- Markdown to PowerPoint
- HTML to PowerPoint

#### New Builders
- LaTeX builder (for round-trip conversion)
- HTML builder
- PDF builder

#### Enhanced Features
- Math equation rendering
- TikZ diagram support
- Advanced animations
- Template system

#### Documentation
- API documentation
- Tutorials
- Examples
- Performance guides

## Testing Guidelines

### Unit Tests

- Test individual components in isolation
- Mock external dependencies
- Cover edge cases and error conditions

### Integration Tests

- Test end-to-end conversion workflows
- Use real sample files
- Verify output quality

### Test Data

Place test files in `tests/fixtures/`:
```
tests/fixtures/
├── latex/
│   ├── simple.tex
│   ├── complex.tex
│   └── broken.tex
└── expected/
    ├── simple.pptx
    └── complex.pptx
```

## Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create git tag
4. Build and publish to PyPI
5. Update documentation

## Community

- GitHub Discussions: Q&A and general discussion
- Issues: Bug reports and feature requests
- Pull Requests: Code contributions

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions. We follow the [Python Community Code of Conduct](https://www.python.org/psf/conduct/).

Thank you for contributing to Slide Forge! 🚀
