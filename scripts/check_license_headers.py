#!/usr/bin/env python3
"""
License header checker for Slide Forge project.
Checks that all Python and Bash files have the proper MIT license header.
"""


import sys
import os
from pathlib import Path

LICENSE_HEADER = '''# Copyright (c) 2026 Slide Forge Team
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
# SOFTWARE.'''


def check_license_header(filepath):
    """Check if a file has the proper license header."""
    # Skip __init__.py files and the license checker itself
    if filepath.name == '__init__.py' or filepath.name == 'check_license_headers.py':
        return True

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, IOError):
        # Skip binary files or files that can't be read
        return True

    lines = content.split('\n')

    # For bash scripts and Python scripts with shebang, skip shebang line
    start_idx = 0
    if (filepath.suffix in ['.sh', '.py'] and lines and lines[0].startswith('#!')):
        start_idx = 1

    # Check if file has enough lines for header
    if len(lines) - start_idx < 20:
        if start_idx > 0:
            print(f'❌ {filepath}: File too short (less than 20 lines after shebang)')
        else:
            print(f'❌ {filepath}: File too short (less than 20 lines)')
        return False

    # Check for license header
    header_lines = lines[start_idx:start_idx + 20]
    header_content = '\n'.join(header_lines)

    if LICENSE_HEADER in header_content:
        return True
    else:
        print(f'❌ {filepath}: Missing or incorrect license header')
        return False


def main():
    """Main entry point."""
    # Check all Python and Bash files in src/, tests/, scripts/, tools/
    failed = False
    for directory in ['src', 'tests', 'scripts', 'tools']:
        if Path(directory).exists():
            for py_file in Path(directory).rglob('*.py'):
                if not check_license_header(py_file):
                    failed = True
            for sh_file in Path(directory).rglob('*.sh'):
                if not check_license_header(sh_file):
                    failed = True

    if failed:
        print('\n💡 To fix: Add the license header to the top of each file')
        print('📖 See .windsurf/rules/license-header.md for the exact format')
        sys.exit(1)
    else:
        print('✅ All Python and Bash files have proper license headers')


if __name__ == '__main__':
    main()
