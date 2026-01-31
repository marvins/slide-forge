#!/usr/bin/env python3
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
