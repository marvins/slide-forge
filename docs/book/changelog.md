# Changelog

All notable changes to Slide Forge will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Sequence diagrams documentation
- Design notes documentation
- Contributing guidelines

### Changed
- Improved positioning system in PowerPoint builder
- Enhanced content mapper with layout calculations

### Fixed
- Font size handling using proper Pt() units
- Image path resolution relative to source document
- Text element overlapping issues

## [0.1.0] - 2026-01-30

### Added
- Initial LaTeX Beamer to PowerPoint conversion
- Core Slide_Forge controller class
- LaTeX parser for basic Beamer structures
- PowerPoint builder using python-pptx
- Content mapper for format conversion
- Universal data models for format-agnostic representation
- Support for text, itemize, images, and block elements
- Basic layout system (title slide, title and content, two column)
- Theme system with multiple PowerPoint themes
- Image path resolution and embedding
- Error handling and logging
- Sample conversion script

### Supported Features
- LaTeX Beamer frame parsing
- Text content extraction
- Bullet point lists (itemize)
- Image inclusion and positioning
- Basic slide layouts
- Font size and color handling
- Multiple PowerPoint themes

### Known Limitations
- Math equations not yet supported
- TikZ diagrams not yet supported
- Complex table formatting limited
- Custom LaTeX commands not supported
- Overlay specifications ignored

## [Future Plans]

### Version 0.2.0 (Planned)
- Math equation support
- Enhanced table handling
- TikZ diagram rendering
- Custom LaTeX commands
- Performance optimizations

### Version 0.3.0 (Planned)
- PowerPoint to LaTeX conversion
- Markdown to PowerPoint support
- Advanced animations
- Template system
- Plugin architecture

### Version 1.0.0 (Long-term)
- Full LaTeX Beamer compatibility
- Round-trip conversion support
- Comprehensive testing suite
- Performance benchmarks
- Production-ready stability
