#!/usr/bin/env python3
"""
Quick demo of Slide Forge API
"""

from slideforge import SlideForge

# Simple conversion
forge = SlideForge()
success = forge.convert_file(
    "latex/presentation.tex",
    "latex/slideforge_output.pptx"
)

if success:
    print("✅ Slide Forge conversion successful!")
else:
    print("❌ Conversion failed")

# Advanced usage with options
forge.convert_file(
    "latex/presentation.tex",
    "latex/slideforge_custom.pptx",
    theme="professional",
    preserve_colors=True,
    include_images=True
)
