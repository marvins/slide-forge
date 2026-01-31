#!/usr/bin/env python3
#
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
"""
Convert sample LaTeX Beamer presentation to PowerPoint format
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path so we can import slideforge
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from slideforge import Slide_Forge

def main():
    """Convert the sample Beamer presentation to PowerPoint"""

    # Define paths
    project_root = Path(__file__).parent.parent
    tex_file = project_root / "samples" / "beamer" / "sample_presentation.tex"
    output_dir = project_root / "outputs"
    pptx_file = output_dir / "sample_presentation.pptx"

    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)

    # Check if input file exists
    if not tex_file.exists():
        print(f"Error: Input file {tex_file} not found!")
        return 1

    print(f"Converting {tex_file} to {pptx_file}...")

    try:
        # Convert LaTeX to PowerPoint using the new API
        converter = Slide_Forge()
        success = converter.convert_file(str(tex_file), str(pptx_file), verbose=True)

        if success:
            print(f"Successfully converted to {pptx_file}")
            return 0
        else:
            print(f"Conversion failed")
            return 1
    except Exception as e:
        print(f"Error during conversion: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
