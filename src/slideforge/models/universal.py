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

"""Universal data models for Slide Forge - format-agnostic representations."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union
from enum import Enum
from pathlib import Path


class Element_Type(Enum):
    """Universal element types that exist across formats."""
    TEXT = "text"
    TITLE = "title"
    SUBTITLE = "subtitle"
    ITEMIZE = "itemize"
    ENUMERATE = "enumerate"
    BLOCK = "block"
    IMAGE = "image"
    EQUATION = "equation"
    TABLE = "table"
    MATH = "math"
    CODE = "code"
    HYPERLINK = "hyperlink"
    SHAPE = "shape"
    CHART = "chart"


class Layout_Type(Enum):
    """Universal slide layout types."""
    TITLE_SLIDE = "title_slide"
    TITLE_AND_CONTENT = "title_and_content"
    SECTION_HEADER = "section_header"
    TWO_COLUMN = "two_column"
    THREE_COLUMN = "three_column"
    BLANK = "blank"
    CONTENT_ONLY = "content_only"


class Formatting(Enum):
    """Text formatting options."""
    BOLD = "bold"
    ITALIC = "italic"
    UNDERLINE = "underline"
    STRIKETHROUGH = "strikethrough"
    SUPERSCRIPT = "superscript"
    SUBSCRIPT = "subscript"
    MONOSPACE = "monospace"
    NORMAL = "normal"


@dataclass
class Text_Content:
    """Text content with formatting information."""
    text: str
    formatting: List[Formatting] = field(default_factory=list)
    font_size: Optional[str] = None
    font_color: Optional[str] = None
    font_family: Optional[str] = None


@dataclass
class Position:
    """Position information for elements."""
    x: float  # Position in inches or cm
    y: float  # Position in inches or cm
    width: Optional[float] = None
    height: Optional[float] = None


@dataclass
class Size:
    """Size information for elements."""
    width: float
    height: float
    scale: Optional[float] = None  # Scale factor


@dataclass
class Universal_Element:
    """Universal element that can represent content from any format."""
    element_type: Element_Type
    content: Union[str, Text_Content, Dict[str, Any]]
    position: Optional[Position] = None
    size: Optional[Size] = None
    level: int = 0  # For nested elements like itemize
    style: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_text_content(self) -> Optional[Text_Content]:
        """Convert content to Text_Content if possible."""
        if isinstance(self.content, str):
            return Text_Content(text=self.content)
        elif isinstance(self.content, Text_Content):
            return self.content
        return None


@dataclass
class Universal_Frame:
    """Universal frame/slide representation."""
    frame_number: int
    title: Optional[str] = None
    subtitle: Optional[str] = None
    elements: List[Universal_Element] = field(default_factory=list)
    layout: Layout_Type = Layout_Type.TITLE_AND_CONTENT
    background_color: Optional[str] = None
    notes: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_element(self, element: Universal_Element) -> None:
        """Add an element to the frame."""
        self.elements.append(element)

    def get_elements_by_type(self, element_type: Element_Type) -> List[Universal_Element]:
        """Get all elements of a specific type."""
        return [elem for elem in self.elements if elem.element_type == element_type]

    def get_text_elements(self) -> List[Universal_Element]:
        """Get all text-based elements."""
        text_types = [Element_Type.TEXT, Element_Type.TITLE, Element_Type.SUBTITLE]
        return [elem for elem in self.elements if elem.element_type in text_types]


@dataclass
class Metadata:
    """Universal metadata for presentations."""
    title: Optional[str] = None
    author: Optional[str] = None
    date: Optional[str] = None
    institution: Optional[str] = None
    subject: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    language: Optional[str] = None
    version: Optional[str] = None
    created_date: Optional[str] = None
    modified_date: Optional[str] = None
    custom_properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Universal_Document:
    """Universal document representation - format-agnostic."""
    metadata: Metadata = field(default_factory=Metadata)
    frames: List[Universal_Frame] = field(default_factory=list)
    source_format: Optional[str] = None  # 'latex', 'pptx', etc.
    source_path: Optional[Path] = None
    global_settings: Dict[str, Any] = field(default_factory=dict)

    def add_frame(self, frame: Universal_Frame) -> None:
        """Add a frame to the document."""
        self.frames.append(frame)

    def get_frame_by_number(self, frame_number: int) -> Optional[Universal_Frame]:
        """Get a frame by its number."""
        for frame in self.frames:
            if frame.frame_number == frame_number:
                return frame
        return None

    def get_total_frames(self) -> int:
        """Get total number of frames."""
        return len(self.frames)

    def get_title_frame(self) -> Optional[Universal_Frame]:
        """Get the title frame (usually first frame with title)."""
        for frame in self.frames:
            if frame.title and frame.layout == Layout_Type.TITLE_SLIDE:
                return frame
        return None


@dataclass
class Conversion_Options:
    """Options for conversion processes."""
    theme: str = "default"
    preserve_colors: bool = True
    preserve_fonts: bool = True
    preserve_layouts: bool = True
    include_images: bool = True
    include_notes: bool = False
    verbose: bool = False
    output_format: Optional[str] = None
    custom_settings: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for easy serialization."""
        return {
            'theme': self.theme,
            'preserve_colors': self.preserve_colors,
            'preserve_fonts': self.preserve_fonts,
            'preserve_layouts': self.preserve_layouts,
            'include_images': self.include_images,
            'include_notes': self.include_notes,
            'verbose': self.verbose,
            'output_format': self.output_format,
            'custom_settings': self.custom_settings
        }


# Utility functions for working with universal models

def create_text_element(text: str, element_type: Element_Type = Element_Type.TEXT,
                       formatting: List[Formatting] = None) -> Universal_Element:
    """Create a text element with optional formatting."""
    content = Text_Content(text=text, formatting=formatting or [])
    return Universal_Element(element_type=element_type, content=content)


def create_image_element(image_path: str, caption: str = None,
                        position: Position = None, size: Size = None) -> Universal_Element:
    """Create an image element."""
    content = {'path': image_path, 'caption': caption}
    return Universal_Element(
        element_type=Element_Type.IMAGE,
        content=content,
        position=position,
        size=size
    )


def create_itemize_element(items: List[str], level: int = 0) -> Universal_Element:
    """Create an itemize (bullet list) element."""
    content = {'items': items}
    return Universal_Element(
        element_type=Element_Type.ITEMIZE,
        content=content,
        level=level
    )


def create_equation_element(latex: str, equation_type: str = 'inline') -> Universal_Element:
    """Create an equation element with LaTeX content."""
    content = {
        'latex': latex,
        'type': equation_type  # 'inline' or 'display'
    }
    return Universal_Element(
        element_type=Element_Type.EQUATION,
        content=content
    )


def merge_documents(doc1: Universal_Document, doc2: Universal_Document) -> Universal_Document:
    """Merge two universal documents."""
    merged = Universal_Document()

    # Merge metadata (doc2 takes precedence)
    merged.metadata = doc2.metadata or doc1.metadata

    # Merge frames
    merged.frames = doc1.frames + doc2.frames

    # Merge global settings
    merged.global_settings = {**doc1.global_settings, **doc2.global_settings}

    return merged
