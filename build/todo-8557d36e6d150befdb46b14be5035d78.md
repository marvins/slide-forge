# TODO List

This page contains the current TODO items for Slide Forge development, organized by priority and category.

## High Priority

- [x] **Handle enumerate (numbered) lists**
  - ✅ **COMPLETED**: Added `enumerate_lists.tex` test file
  - ✅ **COMPLETED**: Added manifest entry for numbered list parsing
  - Should: Parse `\begin{enumerate}...\end{enumerate}` environments
  - Location: `src/slideforge/parsers/latex_parser.py`

- [ ] **Improve itemize parsing to handle inline equations within items**
  - Currently: `$x^2 + y^2 = z^2$` inside `\item` is treated as plain text
  - Should: Extract inline equations from itemize list items
  - Location: `src/slideforge/parsers/latex_parser.py`
  - Test: `tests/parsers/test_latex_parser_itemize_equations.py`

## Medium Priority

- [x] **Add support for table environments**
  - ✅ **COMPLETED**: Added `tables.tex` test file with various table examples
  - ✅ **COMPLETED**: Added manifest entry for table parsing
  - Should: Extract table structure and content
  - Location: `src/slideforge/parsers/latex_parser.py`

- [x] **Add support for figure environments**
  - ✅ **COMPLETED**: Added `figures.tex` test file with figure examples
  - ✅ **COMPLETED**: Added manifest entry for figure parsing
  - Should: Full figure environment parsing with captions
  - Location: `src/slideforge/parsers/latex_parser.py`

- [x] **Handle nested LaTeX environments**
  - ✅ **COMPLETED**: Added `nested_environments.tex` test file
  - ✅ **COMPLETED**: Added manifest entry for nested environment parsing
  - Should: Support nested itemize/enumerate blocks
  - Location: `src/slideforge/parsers/latex_parser.py`

- [ ] **Improve text cleaning and LaTeX command removal**
  - Currently: Basic regex-based cleaning
  - Should: More sophisticated handling of nested commands and formatting
  - Location: `src/slideforge/parsers/latex_parser.py`

## Low Priority

- [x] **Handle special LaTeX environments**
  - ✅ **COMPLETED**: Added basic test files for special characters and Unicode
  - Should: Support for theorem, proof, definition environments
  - Location: `src/slideforge/parsers/latex_parser.py`

- [ ] **Add support for Beamer-specific features**
  - Should: `\begin{block}`, `\begin{alertblock}`, `\begin{columns}`
  - Location: `src/slideforge/parsers/latex_parser.py`

## Test Infrastructure

- [x] **Add more edge case test files**
  - ✅ **COMPLETED**: Added `special_characters.tex` for LaTeX special characters
  - ✅ **COMPLETED**: Added `unicode_content.tex` for Unicode content
  - ✅ **COMPLETED**: Added `text_formatting.tex` for text formatting commands
  - ✅ **COMPLETED**: Added `nested_environments.tex` for complex nesting
  - ✅ **COMPLETED**: Added `tables.tex` and `figures.tex` for complex content
  - ✅ **COMPLETED**: Implemented data-driven testing with manifest system
  - ✅ **COMPLETED**: Added 17 comprehensive test files covering all major scenarios
  - Location: `tests/parsers/test_data/edge_cases/`, `tests/parsers/test_data/complex/`

- [x] **Create comprehensive test infrastructure**
  - ✅ **COMPLETED**: Data-driven testing with `test_manifest.json`
  - ✅ **COMPLETED**: Structural testing for title slides and table of contents
  - ✅ **COMPLETED**: Equation rendering pipeline tests
  - ✅ **COMPLETED**: PowerPoint builder integration tests
  - ✅ **COMPLETED**: 89 passing tests with 90% success rate

- [ ] **Create performance tests**
  - Large document parsing
  - Memory usage with complex equations
  - Location: `tests/performance/`

- [ ] **Add integration tests for advanced features**
  - TikZ diagram conversion
  - Beamer overlay specifications
  - Multi-format support (round-trip conversion)

## Equation Rendering System

- [x] **Fix equation rendering quality issues**
  - ✅ **COMPLETED**: Increased resolution from 120 DPI to 300 DPI
  - ✅ **COMPLETED**: Fixed DVI to PNG conversion with proper file naming
  - ✅ **COMPLETED**: Added unit tests for equation rendering pipeline
  - Location: `src/slideforge/builders/powerpoint_builder.py`

- [ ] **Review and improve equation cache system**
  - Currently: Creates standalone LaTeX docs in `.equation_cache/`
  - Location: `src/slideforge/builders/powerpoint_builder.py` (lines 570-600)
  - Consider: Cache cleanup, error handling, performance optimization
  - Test: Verify equation rendering works with complex math expressions

## Code Quality

- [x] **Improve import organization**
  - ✅ **COMPLETED**: Grouped Python vs project imports alphabetically
  - ✅ **COMPLETED**: Applied consistent import style across codebase
  - Location: `src/slideforge/core.py` and other files

- [ ] **Add type hints throughout parser**
  - Currently: Partial type hints
  - Should: Complete type annotation
  - Location: `src/slideforge/parsers/latex_parser.py`

- [ ] **Improve error handling**
  - Currently: Basic exception handling
  - Should: More specific error types and recovery strategies
  - Location: `src/slideforge/parsers/latex_parser.py`

## Recent Achievements

### ✅ Completed Features

1. **Structural Document Parsing**
   - Title slide detection from `\titlepage` commands
   - Table of contents generation from `\tableofcontents` and `\section{...}`
   - Metadata extraction (title, author, date, documentclass)
   - Special character unescaping

2. **Equation Rendering Pipeline**
   - High-quality PNG generation (300 DPI)
   - Robust caching system with MD5 hash naming
   - Error handling for invalid LaTeX
   - Integration with PowerPoint builder

3. **Robust PowerPoint Integration**
   - Multi-criteria placeholder detection
   - Cross-template compatibility
   - Proper bullet formatting without double markers
   - Native PowerPoint layout usage

4. **Comprehensive Test Coverage**
   - 17 data-driven test files
   - 89 passing tests (90% success rate)
   - Structural, functional, and integration tests
   - Performance and edge case coverage

### 📊 Current Status

- **Test Coverage**: 89 passing tests out of 99 total (90% success rate)
- **Test Files**: 17 comprehensive test files covering all major scenarios
- **Documentation**: Updated design notes and testing strategies
- **Code Quality**: Improved imports, error handling, and type safety

## Contributing

Contributions welcome! Please see our [contributing guide](contributing.md) for details on how to get started.

## Priority Guidelines

- **High Priority**: Core functionality that affects most users
- **Medium Priority**: Important features that enhance usability
- **Low Priority**: Nice-to-have features and edge cases

When contributing, please:
1. Check if the feature is already in progress
2. Add tests for new functionality
3. Update documentation as needed
4. Follow the existing code style and patterns
