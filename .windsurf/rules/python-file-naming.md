# Python File Naming Convention

## Rule
All Python files should follow Snake_Case naming convention with `.py` extension.

## Guidelines

### File Names
- Use lowercase letters with underscores (`_`) as separators
- Example: `latex_parser.py`, `content_mapper.py`, `powerpoint_builder.py`
- Avoid hyphens, spaces, or camelCase in file names
- Keep names descriptive but concise

### Class Files
- When a file contains a primary class, name the file after the class using snake_case
- Example: Class `LaTeX_Parser` → file `latex_parser.py`
- Example: Class `Content_Mapper` → file `content_mapper.py`

### Module Files
- Utility modules: `utils.py`, `helpers.py`
- Configuration: `config.py`, `settings.py`
- Constants: `constants.py`
- Exceptions: `exceptions.py`, `errors.py`

### Package Structure
```
src/slideforge/
├── __init__.py
├── core.py                 # Main Slide_Forge class
├── parsers/
│   ├── __init__.py
│   ├── latex_parser.py     # LaTeX_Parser class
│   └── base_parser.py      # Base parser functionality
├── mappers/
│   ├── __init__.py
│   ├── content_mapper.py   # Content_Mapper class
│   └── element_mappers.py   # Element-specific mappers
├── builders/
│   ├── __init__.py
│   ├── powerpoint_builder.py # PowerPoint_Builder class
│   └── slide_builders.py   # Slide-specific builders
├── models/
│   ├── __init__.py
│   ├── document.py         # Document, Frame, Element classes
│   ├── slide_structure.py  # Slide_Structure, Slide_Element classes
│   └── metadata.py         # Metadata and related classes
├── exceptions.py           # Custom exception classes
├── utils.py               # Utility functions
└── constants.py           # Project constants
```

## Examples

### ✅ Good Names
```python
latex_parser.py
content_mapper.py
powerpoint_builder.py
slide_structure.py
document.py
element.py
exceptions.py
utils.py
config.py
```

### ❌ Bad Names
```python
LaTeXParser.py           # Uses PascalCase
latex-parser.py          # Uses hyphens
latex parser.py          # Contains space
lp.py                    # Too abbreviated
parser_v2.py             # Contains version number
```

## Enforcement
This convention should be enforced through:
1. Code review guidelines
2. Automated linting rules (if applicable)
3. IDE configuration suggestions
