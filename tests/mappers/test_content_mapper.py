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

"""Tests for content mapper."""

import pytest
from slideforge.mappers.content_mapper import Content_Mapper
from slideforge.models.universal import (
    Universal_Document, Universal_Frame, Universal_Element,
    Element_Type, Layout_Type, Position
)


class TestContentMapper:
    """Test cases for content mapper."""

    @pytest.fixture
    def mapper(self):
        """Create content mapper instance."""
        return Content_Mapper()

    @pytest.fixture
    def sample_document(self):
        """Create sample universal document."""
        doc = Universal_Document()

        # Add frames with different layouts
        frame1 = Universal_Frame(
            frame_number=1,
            title="Title Slide",
            elements=[],
            layout=Layout_Type.TITLE_SLIDE
        )

        frame2 = Universal_Frame(
            frame_number=2,
            title="Content Slide",
            elements=[
                Universal_Element(
                    element_type=Element_Type.TEXT,
                    content="This is some text content"
                ),
                Universal_Element(
                    element_type=Element_Type.ITEMIZE,
                    content={'items': ['Item 1', 'Item 2', 'Item 3']}
                )
            ],
            layout=Layout_Type.TITLE_AND_CONTENT
        )

        frame3 = Universal_Frame(
            frame_number=3,
            title="Two Column Slide",
            elements=[
                Universal_Element(
                    element_type=Element_Type.TEXT,
                    content="Left column content"
                ),
                Universal_Element(
                    element_type=Element_Type.TEXT,
                    content="Right column content"
                )
            ],
            layout=Layout_Type.TWO_COLUMN
        )

        doc.frames = [frame1, frame2, frame3]
        return doc

    def test_get_supported_conversions(self, mapper):
        """Test supported conversion mappings."""
        conversions = mapper.get_supported_conversions()
        assert 'latex' in conversions
        assert 'pptx' in conversions['latex']

    def test_can_convert(self, mapper):
        """Test conversion capability checking."""
        assert mapper.can_convert('latex', 'pptx')
        assert not mapper.can_convert('pptx', 'latex')  # Not implemented yet

    def test_map_to_powerpoint(self, mapper, sample_document):
        """Test mapping to PowerPoint format."""
        result = mapper.map_document(sample_document, 'pptx')

        assert len(result) == 3  # Should have 3 frames

        # Check that frames were positioned
        for frame in result:
            assert hasattr(frame, 'elements')
            for element in frame.elements:
                if element.element_type == Element_Type.TEXT:
                    assert element.position is not None
                    assert element.position.x is not None
                    assert element.position.y is not None
                    assert element.position.width is not None
                    assert element.position.height is not None

    def test_position_frame_elements_title_slide(self, mapper):
        """Test positioning for title slide."""
        frame = Universal_Frame(
            frame_number=1,
            title="Title Slide",
            elements=[
                Universal_Element(
                    element_type=Element_Type.SUBTITLE,
                    content="Subtitle content"
                )
            ],
            layout=Layout_Type.TITLE_SLIDE
        )

        positioned_frame = mapper._position_frame_elements(frame)

        assert positioned_frame.frame_number == 1
        assert positioned_frame.title == "Title Slide"
        assert positioned_frame.layout == Layout_Type.TITLE_SLIDE

        # Check element positioning
        element = positioned_frame.elements[0]
        assert element.position.x == 1.0  # MARGIN_LEFT
        assert element.position.y == 2.5  # MARGIN_TOP
        assert element.position.width == 8.0  # CONTENT_WIDTH
        assert element.position.height >= 0.5  # Minimum height

    def test_position_frame_elements_content_slide(self, mapper):
        """Test positioning for content slide."""
        frame = Universal_Frame(
            frame_number=1,
            title="Content Slide",
            elements=[
                Universal_Element(
                    element_type=Element_Type.TEXT,
                    content="First paragraph"
                ),
                Universal_Element(
                    element_type=Element_Type.ITEMIZE,
                    content={'items': ['Item 1', 'Item 2', 'Item 3', 'Item 4']}
                ),
                Universal_Element(
                    element_type=Element_Type.TEXT,
                    content="Second paragraph"
                )
            ],
            layout=Layout_Type.TITLE_AND_CONTENT
        )

        positioned_frame = mapper._position_frame_elements(frame)

        # Check that elements are positioned vertically
        elements = positioned_frame.elements

        # First element should be at top
        assert elements[0].position.y == 2.5  # MARGIN_TOP

        # Second element should be below first
        assert elements[1].position.y > elements[0].position.y

        # Third element should be below second
        assert elements[2].position.y > elements[1].position.y

        # Check spacing
        spacing = elements[1].position.y - (elements[0].position.y + elements[0].position.height)
        assert spacing >= 0.4  # ELEMENT_SPACING

    def test_position_element_text(self, mapper):
        """Test positioning of text elements."""
        element = Universal_Element(
            element_type=Element_Type.TEXT,
            content="Sample text content"
        )

        positioned = mapper._position_element(element, 2.5, 1.0, 8.0)

        assert positioned.element_type == Element_Type.TEXT
        assert positioned.content == "Sample text content"
        assert positioned.position.x == 1.0
        assert positioned.position.y == 2.5
        assert positioned.position.width == 8.0
        assert positioned.position.height >= 0.3  # Minimum height for text

    def test_position_element_itemize(self, mapper):
        """Test positioning of itemize elements."""
        element = Universal_Element(
            element_type=Element_Type.ITEMIZE,
            content={'items': ['Item 1', 'Item 2', 'Item 3']}
        )

        positioned = mapper._position_element(element, 2.5, 1.0, 8.0)

        assert positioned.element_type == Element_Type.ITEMIZE
        assert len(positioned.content['items']) == 3
        assert positioned.position.x == 1.0
        assert positioned.position.y == 2.5
        assert positioned.position.width == 8.0
        assert positioned.position.height >= 1.2  # 3 items * 0.4 each

    def test_position_element_image(self, mapper):
        """Test positioning of image elements."""
        element = Universal_Element(
            element_type=Element_Type.IMAGE,
            content={'path': 'test.png'}
        )

        positioned = mapper._position_element(element, 2.5, 1.0, 8.0)

        assert positioned.element_type == Element_Type.IMAGE
        assert positioned.position.x == 1.0
        assert positioned.position.y == 2.5
        assert positioned.position.width == 8.0
        assert positioned.position.height == 4.0  # Default image height

    def test_position_element_block(self, mapper):
        """Test positioning of block elements."""
        element = Universal_Element(
            element_type=Element_Type.BLOCK,
            content="Block quote content"
        )

        positioned = mapper._position_element(element, 2.5, 1.0, 8.0)

        assert positioned.element_type == Element_Type.BLOCK
        assert positioned.position.x == 1.0
        assert positioned.position.y == 2.5
        assert positioned.position.width == 8.0
        assert positioned.position.height == 1.0  # Default block height

    def test_estimate_text_height(self, mapper):
        """Test text height estimation."""
        # Single line
        height1 = mapper._estimate_text_height("Single line of text", 8.0)
        assert height1 >= 0.3

        # Multiple lines
        height2 = mapper._estimate_text_height("Line 1\nLine 2\nLine 3", 8.0)
        assert height2 >= 0.9  # 3 lines * 0.3 each

        # Empty text
        height3 = mapper._estimate_text_height("", 8.0)
        assert height3 >= 0.3  # Minimum height

    def test_estimate_itemize_height(self, mapper):
        """Test itemize height estimation."""
        # Single item
        height1 = mapper._estimate_itemize_height(['Single item'], 8.0)
        assert height1 >= 0.4

        # Multiple items
        height2 = mapper._estimate_itemize_height(['Item 1', 'Item 2', 'Item 3'], 8.0)
        assert height2 >= 1.2  # 3 items * 0.4 each

        # Empty list
        height3 = mapper._estimate_itemize_height([], 8.0)
        assert height3 >= 0.4  # Minimum height

    def test_map_to_latex_not_implemented(self, mapper):
        """Test that LaTeX mapping is not implemented yet."""
        doc = Universal_Document()

        with pytest.raises(Exception):
            mapper.map_document(doc, 'latex')

    def test_preserve_frame_metadata(self, mapper, sample_document):
        """Test that frame metadata is preserved during mapping."""
        result = mapper.map_document(sample_document, 'pptx')

        for i, original_frame in enumerate(sample_document.frames):
            mapped_frame = result[i]

            assert mapped_frame.frame_number == original_frame.frame_number
            assert mapped_frame.title == original_frame.title
            assert mapped_frame.layout == original_frame.layout
            assert mapped_frame.background_color == original_frame.background_color
            assert mapped_frame.notes == original_frame.notes

    def test_preserve_element_metadata(self, mapper, sample_document):
        """Test that element metadata is preserved during mapping."""
        result = mapper.map_document(sample_document, 'pptx')

        for original_frame in sample_document.frames:
            for original_element in original_frame.elements:
                # Find corresponding element in mapped frame
                mapped_frame = next(f for f in result if f.frame_number == original_frame.frame_number)
                mapped_element = next(e for e in mapped_frame.elements if e.content == original_element.content)

                assert mapped_element.element_type == original_element.element_type
                assert mapped_element.level == original_element.level
                assert mapped_element.style == original_element.style
                assert mapped_element.metadata == original_element.metadata
