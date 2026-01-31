# One Class Per File Convention

## Rule
Each Python file should contain primarily one main class. This is an optional but recommended convention for better code organization and maintainability.

## Guidelines

### Primary Class Per File
- Each `.py` file should have one primary class that gives the file its name
- Supporting classes, enums, and utility functions may be included if they're closely related
- The main class should be the most important/complex class in the file

### File Structure Template
```python
# Copyright (c) 2026 Slide Forge Team
# [Full license header...]

"""Module description focusing on the primary class."""

from typing import List, Optional
from .other_module import SomeClass


class Primary_Class:
    """Main class for this module - the reason this file exists."""
    
    def __init__(self):
        """Initialize the primary class."""
        pass
    
    def main_methods(self):
        """Primary functionality."""
        pass


# Supporting classes (if closely related)
class SupportingEnum:
    """Enum or helper class used by Primary_Class."""
    VALUE1 = "value1"
    VALUE2 = "value2"


def utility_function():
    """Utility function used by Primary_Class."""
    pass
```

### When to Combine Classes

### ✅ Acceptable to Combine
- **Helper classes**: Small classes used only by the main class
- **Enums**: Enums specific to the main class functionality
- **Data classes**: Simple data containers used by the main class
- **Exception classes**: Custom exceptions for the main class
- **Factory classes**: Classes that create instances of the main class

### Examples of Acceptable Combinations
```python
# latex_parser.py
class LaTeX_Parser:
    """Main parser class."""
    pass

class Parse_Error(Exception):
    """Exception raised during parsing."""
    pass

class Token_Type(Enum):
    """Token types used by the parser."""
    TEXT = "text"
    COMMAND = "command"
```

### ❌ Should Be Separate Files
- **Unrelated classes**: Classes that serve different purposes
- **Same-level classes**: Two classes of similar importance
- **Large helper classes**: Helper classes that are complex enough to stand alone
- **Framework classes**: Classes that could be used independently

### Examples of What to Separate
```python
# ❌ Bad - Two main classes in one file
class LaTeX_Parser:
    """Parses LaTeX files."""
    pass

class PowerPoint_Builder:
    """Builds PowerPoint presentations."""
    pass
    # This should be in powerpoint_builder.py
```

## Directory Structure Examples

### Good Structure
```
src/slideforge/
├── parsers/
│   ├── latex_parser.py      # LaTeX_Parser + Parse_Error + Token_Type
│   └── base_parser.py      # Base_Parser + Parser_Config
├── mappers/
│   ├── content_mapper.py   # Content_Mapper + Mapping_Error
│   └── element_mappers.py   # Text_Mapper + Image_Mapper (related)
├── builders/
│   ├── powerpoint_builder.py # PowerPoint_Builder + Builder_Error
│   └── slide_builders.py   # Title_Slide_Builder + Content_Slide_Builder
└── models/
    ├── document.py         # Document + Frame + Element
    ├── slide_structure.py  # Slide_Structure + Slide_Element
    └── metadata.py         # Metadata + Document_Info
```

## Benefits

### ✅ Advantages
- **Clear organization**: Easy to find specific classes
- **Better navigation**: IDE can locate files by class name
- **Focused responsibility**: Each file has a clear purpose
- **Easier testing**: Test files map cleanly to source files
- **Reduced merge conflicts**: Fewer developers editing the same file
- **Better documentation**: Each file can focus on one class

### ⚠️ Trade-offs
- **More files**: Can increase file count
- **Import overhead**: May need more imports
- **Related code spread**: Helper classes might be separated

## Enforcement

### Code Review Guidelines
- Review new files for single-class focus
- Suggest splitting when files grow too large
- Ensure file names match primary class names

### Automated Checks (Optional)
- Check if file contains multiple large classes
- Verify file name matches main class name
- Flag files that exceed reasonable complexity

### IDE Configuration
- Configure file templates to encourage single-class structure
- Use code folding to manage larger files when necessary

## Exceptions to the Rule

### Acceptable Violations
- **Test files**: Multiple test classes per file is common
- **Configuration files**: Multiple related config classes
- **Legacy code**: Existing complex files during refactoring
- **Prototype code**: Early development before proper structure

### Process for Exceptions
1. Document why the exception is necessary
2. Plan future refactoring if applicable
3. Ensure the file remains maintainable
4. Consider splitting during major refactoring cycles
