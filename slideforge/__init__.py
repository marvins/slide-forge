"""
Slide Forge - LaTeX Beamer to PowerPoint Converter
A Python library for creating PowerPoint presentations from LaTeX Beamer source.
"""

from .parser import LaTeXParser
from .mapper import ContentMapper
from .builder import PowerPointBuilder
from .core import SlideForge

__version__ = "0.1.0"
__all__ = ["SlideForge", "LaTeXParser", "ContentMapper", "PowerPointBuilder"]
