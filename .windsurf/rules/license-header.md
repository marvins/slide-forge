# License Header Requirement

## Rule
All Python source files must include the project license header at the top of the file.

## Header Template
```python
# Copyright (c) 2026 Slide Forge Team
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
```

## Implementation Guidelines

### File Structure
1. **License header** (lines 1-20)
2. **Empty line** (line 21)
3. **Module docstring** (if applicable)
4. **Imports**
5. **Code implementation**

### Example Complete File
```python
# Copyright (c) 2026 Slide Forge Team
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""LaTeX parser module for converting LaTeX Beamer presentations to structured data."""

#  Python Standard Libraries
from typing import List, Optional

#  Project Libraries
from .models.document import Document, Frame


class LaTeX_Parser:
    """Parser for LaTeX Beamer presentations."""

    def __init__(self):
        """Initialize the LaTeX parser."""
        pass

    def parse_file(self, filepath: str) -> Document:
        """Parse a LaTeX file and return a Document object."""
        pass
```

## Files That Require Headers

### ✅ Must Include Header
- All `.py` files in `src/`
- All `.py` files in `tests/`
- All `.py` files in `scripts/`
- All `.py` files in `tools/`
- All `.sh` files in `scripts/`
- All `.sh` files in `tools/`

### ❌ Exceptions
- `__init__.py` files (use minimal header or just copyright line)
- Configuration files that don't contain code
- Generated files
- Temporary files

## Bash Script Header Format

For bash scripts, the license header should come **after** the shebang line:

```bash
#!/bin/bash

# Copyright (c) 2026 Slide Forge Team
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Development Setup Script for Slide Forge
# This script sets up the development environment with pre-commit hooks

set -e
```

**Note**: The license header content is **identical** for both Python and Bash files. The only difference is that Bash scripts include a shebang line (`#!/bin/bash`) before the header.

## Enforcement

### Automated Checks
- Pre-commit hooks should verify header presence
- CI/CD pipeline should check for missing headers
- IDE templates should include header by default

### Code Review
- Pull requests must verify headers are present
- New files should be created with header included
- Modified files should maintain header integrity

### Tools
- Use `license-header` checker tools
- Configure IDE to insert header automatically
- Add to project linting configuration

## Header Maintenance
- Update year annually (automated script recommended)
- Ensure consistent formatting across all files
- Verify header is exactly 20 lines as specified
