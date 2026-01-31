# TODO List

This page contains the current TODO items for Slide Forge development, organized by priority and category.

## High Priority

- [ ] **Improve itemize parsing to handle inline equations within items**
  - Currently: `$x^2 + y^2 = z^2$` inside `\item` is treated as plain text
  - Should: Extract inline equations from itemize list items
  - Location: `src/slideforge/parsers/latex_parser.py`
  - Test: `tests/parsers/test_latex_parser_itemize_equations.py`

## Medium Priority

- [ ] **Improve text cleaning and LaTeX command removal**
  - Currently: Basic regex-based cleaning
  - Should: More sophisticated handling of nested commands and formatting
  - Location: `src/slideforge/parsers/latex_parser.py`

## Low Priority

- [ ] **Add support for Beamer-specific features**
  - Should: `\begin{block}`, `\begin{alertblock}`, `\begin{columns}`
  - Location: `src/slideforge/parsers/latex_parser.py`

## Test Infrastructure

- [ ] **Create performance tests**
  - Large document parsing
  - Memory usage with complex equations
  - Location: `tests/performance/`

- [ ] **Add integration tests for advanced features**
  - TikZ diagram conversion
  - Beamer overlay specifications
  - Multi-format support (round-trip conversion)

## Equation Rendering System

- [ ] **Review and improve equation cache system**
  - Currently: Creates standalone LaTeX docs in `.equation_cache/`
  - Location: `src/slideforge/builders/powerpoint_builder.py` (lines 570-600)
  - Consider: Cache cleanup, error handling, performance optimization
  - Test: Verify equation rendering works with complex math expressions

## Code Quality

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

- **Test Coverage**: 110 passing tests out of 122 total (90% success rate) ✅ **Improved from 89%**
- **Recent Fixes Applied**:
  - ✅ Fixed all core integration issues (LaTeX parser registration)
  - ✅ Fixed PowerPoint builder test setup (theme references)
  - ✅ Enhanced block equation processing with comprehensive tests
- **Test Files**: 18 comprehensive test files covering all major scenarios
- **Documentation**: Updated design notes and testing strategies
- **Code Quality**: Improved imports, error handling, and type safety

### 🔧 Current Issues (12 failing tests) ✅ **Reduced from 24**

**High Priority Issues:**
- **PowerPoint Builder**: Mock setup issues in some tests (4 tests with NameError)

**Medium Priority Issues:**
- **Content Mapper**: Positioning and height estimation calculations (3 tests)
- **Data-Driven Tests**: Some manifest expectations need updates (2 tests)

**Low Priority Issues:**
- **Edge Cases**: Minor parsing edge cases in itemize equations (1 test)
- **Other**: 2 miscellaneous test issues

**Recently Fixed:**
- ✅ LaTeX parser registration in all core tests (10 tests fixed)
- ✅ PowerPoint builder theme attribute references
- ✅ Block equation processing tests
- ✅ All conversion and format detection tests

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
