# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-01-30

### Added
- Bidirectional presentation conversion architecture
- Universal data models for format-agnostic representation
- Abstract base classes for parsers, builders, and mappers
- Auto-generated API documentation system
- Jupyter Book documentation with MyST Markdown
- GitHub Actions CI/CD for documentation deployment
- Comprehensive exception hierarchy
- LaTeX Beamer parser implementation
- PowerPoint builder (placeholder implementation)
- Content mapper for format conversions

### Changed
- Refactored from monolithic conversion to modular architecture
- Updated core API to use `Slide_Forge` class with bidirectional support
- Switched from manual to auto-generated API documentation
- Updated documentation deployment to use `myst build` with proper BASE_URL support

### Fixed
- Import errors in CLI application (`SlideForge` → `Slide_Forge`)
- Missing type hints in base classes (`Slide_Structure` → `Universal_Frame`)
- BASE_URL configuration for GitHub Pages deployment
- Auto-generated API documentation generation

### Deprecated
- Old monolithic conversion functions
- Manual API documentation maintenance

## [0.1.0] - 2026-01-30

### Added
- Initial project structure
- Basic LaTeX Beamer to PowerPoint conversion concept
- Development rules and guidelines
- Project documentation setup
- Sample conversion script

### Changed
- Project initialization and basic architecture

---

## Version History

### Version 0.1.0 (Current)
- **Status**: Development/Alpha
- **Features**: Basic conversion framework, documentation system
- **Stability**: Experimental - API may change

### Future Versions
- **0.2.0**: Full LaTeX to PowerPoint implementation
- **0.3.0**: PowerPoint to LaTeX conversion
- **1.0.0**: Stable release with full bidirectional support

---

## Migration Guide

### From 0.1.0 to 0.1.1 (Current)

If you were using the old API:

```python
# Old way (deprecated)
from slideforge.core import convert_latex_to_pptx
convert_latex_to_pptx("input.tex", "output.pptx")

# New way (current)
from slideforge import Slide_Forge
converter = Slide_Forge()
converter.convert_file("input.tex", "output.pptx")
```

### Breaking Changes

- Core API moved from standalone functions to `Slide_Forge` class
- Import path changed from `slideforge.core` to `slideforge`
- Function signatures updated to use keyword arguments

---

## Contributing to Changelog

When adding new features or fixing bugs, please update this changelog:

1. Add entries under the appropriate version section
2. Use the format: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`
3. Be specific about what changed and why
4. Include migration notes for breaking changes
5. Update version number according to semantic versioning

---

*This changelog follows the principles of [Keep a Changelog](https://keepachangelog.com/).*
