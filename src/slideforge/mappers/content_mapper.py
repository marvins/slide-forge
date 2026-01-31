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

"""Content mapper for converting between presentation formats."""

from typing import List, Dict, Any

from ..base import Base_Mapper
from ..models.universal import (
    Universal_Document, Universal_Frame, Universal_Element,
    Position, Size, Layout_Type, Element_Type
)
from ..exceptions import MappingError


class Content_Mapper(Base_Mapper):
    """Content mapper for bidirectional format conversions."""

    def __init__(self):
        """Initialize content mapper."""
        self.supported_conversions = {
            'latex': ['pptx'],
            'pptx': ['latex']  # Future support
        }

    def map_document(self, document: Universal_Document, target_format: str,
                   **kwargs) -> List[Any]:
        """
        Map a Universal_Document to slide structures for target format.

        Args:
            document: Source Universal_Document
            target_format: Target format ('pptx', 'latex', etc.)
            **kwargs: Additional mapping options

        Returns:
            List of slide structures appropriate for target format
        """
        if target_format == 'pptx':
            return self._map_to_powerpoint(document, **kwargs)
        elif target_format == 'latex':
            return self._map_to_latex(document, **kwargs)
        else:
            raise MappingError(f"Unsupported target format: {target_format}",
                           target_format=target_format)

    def get_supported_conversions(self) -> Dict[str, List[str]]:
        """Get supported conversion mappings."""
        return self.supported_conversions

    def _map_to_powerpoint(self, document: Universal_Document, **kwargs) -> List[Any]:
        """
        Map Universal_Document to PowerPoint slide structures with proper positioning.

        Args:
            document: Source document
            **kwargs: Additional options

        Returns:
            List of slide structures for PowerPoint builder with positions set
        """
        positioned_frames = []

        for frame in document.frames:
            positioned_frame = self._position_frame_elements(frame)
            positioned_frames.append(positioned_frame)

        return positioned_frames

    def _position_frame_elements(self, frame: Universal_Frame) -> Universal_Frame:
        """
        Calculate and set positions for all elements in a frame based on layout.

        Args:
            frame: Universal_Frame with unpositioned elements

        Returns:
            Universal_Frame with positioned elements
        """
        # Layout constants (in inches from top-left)
        MARGIN_LEFT = 1.0
        MARGIN_RIGHT = 1.0
        MARGIN_TOP = 2.5  # Below title
        ELEMENT_SPACING = 0.4
        SLIDE_WIDTH = 10.0
        CONTENT_WIDTH = SLIDE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT

        current_y = MARGIN_TOP

        # Create a new frame with positioned elements
        positioned_frame = Universal_Frame(
            frame_number=frame.frame_number,
            title=frame.title,
            subtitle=frame.subtitle,
            layout=frame.layout,
            background_color=frame.background_color,
            notes=frame.notes,
            metadata=frame.metadata
        )

        for element in frame.elements:
            positioned_element = self._position_element(element, current_y, MARGIN_LEFT, CONTENT_WIDTH)
            positioned_frame.add_element(positioned_element)

            # Update current_y based on element height
            if positioned_element.position:
                element_height = positioned_element.position.height or 0.5
                current_y += element_height + ELEMENT_SPACING

        return positioned_frame

    def _position_element(self, element: Universal_Element, current_y: float,
                         left_margin: float, content_width: float) -> Universal_Element:
        """
        Calculate position for a single element.

        Args:
            element: Universal_Element to position
            current_y: Current vertical position
            left_margin: Left margin in inches
            content_width: Available content width in inches

        Returns:
            Universal_Element with calculated position
        """
        # Calculate element dimensions based on type
        if element.element_type == Element_Type.TEXT:
            height = self._estimate_text_height(element.content, content_width)
        elif element.element_type == Element_Type.ITEMIZE:
            height = self._estimate_itemize_height(element.content, content_width)
        elif element.element_type == Element_Type.IMAGE:
            height = 4.0  # Default image height
        elif element.element_type == Element_Type.BLOCK:
            height = self._estimate_text_height(element.content, content_width)
        else:
            height = 0.5  # Default height

        # Create position object
        position = Position(
            x=left_margin,
            y=current_y,
            width=content_width,
            height=height
        )

        # Create new element with position
        positioned_element = Universal_Element(
            element_type=element.element_type,
            content=element.content,
            position=position,
            size=element.size,
            level=element.level,
            style=element.style,
            metadata=element.metadata
        )

        return positioned_element

    def _estimate_text_height(self, content, width: float) -> float:
        """Estimate height needed for text content."""
        if isinstance(content, str):
            text = content
        else:
            text = str(content)

        # Rough estimation: ~0.3 inches per line
        lines = len(text.split('\n'))
        return max(0.3, lines * 0.3)

    def _estimate_itemize_height(self, content, width: float) -> float:
        """Estimate height needed for itemize content."""
        if isinstance(content, dict) and 'items' in content:
            items = content['items']
        else:
            items = [str(content)]

        # Rough estimation: ~0.4 inches per bullet point
        return max(0.4, len(items) * 0.4)

    def _map_to_latex(self, document: Universal_Document, **kwargs) -> List[Any]:
        """
        Map Universal_Document to LaTeX slide structures.

        Args:
            document: Source document
            **kwargs: Additional options

        Returns:
            List of slide structures for LaTeX builder
        """
        # Future implementation for PPTX to LaTeX conversion
        raise MappingError("PowerPoint to LaTeX conversion not yet implemented",
                           source_format="pptx", target_format="latex")
