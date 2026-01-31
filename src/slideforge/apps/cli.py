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
Slide Forge CLI Application
Command-line interface for LaTeX to PowerPoint conversion
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from ..core import SlideForge


def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser"""
    parser = argparse.ArgumentParser(
        prog="slide-forge",
        description="Convert LaTeX Beamer presentations to PowerPoint",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  slide-forge -i presentation.tex -o presentation.pptx
  slide-forge --input slides.tex --output slides.pptx --verbose
  slide-forge -i presentation.tex -o output.pptx --theme professional
        """
    )

    # Input/Output arguments
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Input LaTeX Beamer file (.tex)"
    )

    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output PowerPoint file (.pptx)"
    )

    # Conversion options
    parser.add_argument(
        "--theme",
        choices=["default", "professional", "academic", "minimal"],
        default="default",
        help="PowerPoint theme to apply (default: default)"
    )

    parser.add_argument(
        "--preserve-colors",
        action="store_true",
        help="Preserve LaTeX colors in PowerPoint"
    )

    parser.add_argument(
        "--include-images",
        action="store_true",
        default=True,
        help="Include images from LaTeX (default: True)"
    )

    parser.add_argument(
        "--no-images",
        action="store_true",
        help="Exclude images from conversion"
    )

    # Output options
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    return parser


def validate_inputs(input_file: str, output_file: str) -> bool:
    """Validate input and output file paths"""
    # Check input file exists
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: Input file '{input_file}' does not exist")
        return False

    if not input_path.suffix.lower() == '.tex':
        print(f"Error: Input file must be a .tex file")
        return False

    # Check output directory exists
    output_path = Path(output_file)
    if not output_path.parent.exists():
        print(f"Error: Output directory '{output_path.parent}' does not exist")
        return False

    if not output_path.suffix.lower() == '.pptx':
        print(f"Error: Output file must be a .pptx file")
        return False

    return True


def convert_file(args: argparse.Namespace) -> int:
    """Perform the conversion with given arguments"""
    try:
        # Validate inputs
        if not validate_inputs(args.input, args.output):
            return 1

        if args.verbose:
            print(f"Converting '{args.input}' to '{args.output}'...")

        # Create SlideForge instance
        forge = SlideForge()

        # Prepare conversion options
        options = {
            'theme': args.theme,
            'preserve_colors': args.preserve_colors,
            'include_images': not args.no_images,
            'verbose': args.verbose
        }

        # Perform conversion
        success = forge.convert_file(args.input, args.output, **options)

        if success:
            print(f"✅ Successfully converted to '{args.output}'")
            return 0
        else:
            print("❌ Conversion failed")
            return 1

    except KeyboardInterrupt:
        print("\n⏹️  Conversion cancelled by user")
        return 1
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def main() -> int:
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()

    # Handle image options
    if args.no_images:
        args.include_images = False

    return convert_file(args)


if __name__ == "__main__":
    sys.exit(main())
