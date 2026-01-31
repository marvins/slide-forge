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

"""Tests for universal data models."""

import pytest
from slideforge.models.universal import (
    Universal_Document, Universal_Frame, Universal_Element,
    Element_Type, Layout_Type, Formatting, Text_Content,
    Position, Size, Conversion_Options,
    create_text_element, create_image_element, create_itemize_element, create_equation_element,
    merge_documents
)


class TestUniversalModels:
    """Test cases for universal data models."""

    def test_universal_document_creation(self):
        """Test Universal_Document creation."""
        doc = Universal_Document()

        assert doc.source_format is None
        assert doc.source_path is None
        assert len(doc.frames) == 0
        assert doc.metadata is not None

    def test_universal_document_with_frames(self):
        """Test Universal_Document with frames."""
        doc = Universal_Document()

        frame1 = Universal_Frame(frame_number=1, title="Frame 1")
        frame2 = Universal_Frame(frame_number=2, title="Frame 2")

        doc.add_frame(frame1)
        doc.add_frame(frame2)

        assert len(doc.frames) == 2
        assert doc.frames[0].frame_number == 1
        assert doc.frames[1].frame_number == 2
        assert doc.frames[0].title == "Frame 1"
        assert doc.frames[1].title == "Frame 2"

    def test_universal_frame_creation(self):
        """Test Universal_Frame creation."""
        frame = Universal_Frame(
            frame_number=1,
            title="Test Frame",
            subtitle="Test Subtitle",
            layout=Layout_Type.TITLE_AND_CONTENT,
            background_color="#FFFFFF"
        )

        assert frame.frame_number == 1
        assert frame.title == "Test Frame"
        assert frame.subtitle == "Test Subtitle"
        assert frame.layout == Layout_Type.TITLE_AND_CONTENT
        assert frame.background_color == "#FFFFFF"
        assert len(frame.elements) == 0

    def test_universal_frame_add_elements(self):
        """Test adding elements to Universal_Frame."""
        frame = Universal_Frame(frame_number=1)

        text_elem = create_text_element("Test text")
        image_elem = create_image_element("test.png", "Test caption")

        frame.add_element(text_elem)
        frame.add_element(image_elem)

        assert len(frame.elements) == 2
        assert frame.elements[0].element_type == Element_Type.TEXT
        assert frame.elements[1].element_type == Element_Type.IMAGE

    def test_get_elements_by_type(self):
        """Test filtering elements by type."""
        frame = Universal_Frame(frame_number=1)

        text_elem = create_text_element("Text content")
        itemize_elem = create_itemize_element(["Item 1", "Item 2"])
        image_elem = create_image_element("test.png")

        frame.add_element(text_elem)
        frame.add_element(itemize_elem)
        frame.add_element(image_elem)

        text_elements = frame.get_elements_by_type(Element_Type.TEXT)
        assert len(text_elements) == 1
        assert text_elements[0].content.text == "Text content"

        image_elements = frame.get_elements_by_type(Element_Type.IMAGE)
        assert len(image_elements) == 1
        assert image_elements[0].content['path'] == "test.png"

        itemize_elements = frame.get_elements_by_type(Element_Type.ITEMIZE)
        assert len(itemize_elements) == 1
        assert len(itemize_elements[0].content['items']) == 2

    def test_get_text_elements(self):
        """Test getting all text-based elements."""
        frame = Universal_Frame(frame_number=1)

        text_elem = create_text_element("Regular text")
        title_elem = create_text_element("Title text", Element_Type.TITLE)
        subtitle_elem = create_text_element("Subtitle text", Element_Type.SUBTITLE)

        frame.add_element(text_elem)
        frame.add_element(title_elem)
        frame.add_element(subtitle_elem)

        text_elements = frame.get_text_elements()
        assert len(text_elements) == 3

        element_types = [elem.element_type for elem in text_elements]
        assert Element_Type.TEXT in element_types
        assert Element_Type.TITLE in element_types
        assert Element_Type.SUBTITLE in element_types

    def test_universal_element_creation(self):
        """Test Universal_Element creation."""
        element = Universal_Element(
            element_type=Element_Type.TEXT,
            content="Test content",
            position=Position(x=1.0, y=2.0, width=8.0, height=1.0),
            size=Size(width=10.0, height=6.0),
            level=1,
            style={"bold": True},
            metadata={"custom": "data"}
        )

        assert element.element_type == Element_Type.TEXT
        assert element.content == "Test content"
        assert element.position.x == 1.0
        assert element.position.y == 2.0
        assert element.position.width == 8.0
        assert element.position.height == 1.0
        assert element.size.width == 10.0
        assert element.size.height == 6.0
        assert element.level == 1
        assert element.style["bold"] is True
        assert element.metadata["custom"] == "data"

    def test_text_content_creation(self):
        """Test Text_Content creation."""
        text_content = Text_Content(
            text="Sample text",
            formatting=[Formatting.BOLD, Formatting.ITALIC],
            font_size=14,
            font_color="#FF0000"
        )

        assert text_content.text == "Sample text"
        assert Formatting.BOLD in text_content.formatting
        assert Formatting.ITALIC in text_content.formatting
        assert text_content.font_size == 14
        assert text_content.font_color == "#FF0000"

    def test_position_creation(self):
        """Test Position creation."""
        position = Position(x=1.5, y=2.5, width=8.5, height=1.5)

        assert position.x == 1.5
        assert position.y == 2.5
        assert position.width == 8.5
        assert position.height == 1.5

        # Test with optional parameters
        position_minimal = Position(x=1.0, y=2.0)
        assert position_minimal.x == 1.0
        assert position_minimal.y == 2.0
        assert position_minimal.width is None
        assert position_minimal.height is None

    def test_size_creation(self):
        """Test Size creation."""
        size = Size(width=10.0, height=6.0, scale=1.5)

        assert size.width == 10.0
        assert size.height == 6.0
        assert size.scale == 1.5

        # Test with optional parameter
        size_minimal = Size(width=8.0, height=4.0)
        assert size_minimal.width == 8.0
        assert size_minimal.height == 4.0
        assert size_minimal.scale is None

    def test_conversion_options_defaults(self):
        """Test Conversion_Options default values."""
        options = Conversion_Options()

        assert options.preserve_colors is True
        assert options.include_images is True
        assert options.include_notes is False
        assert options.verbose is False
        assert options.output_format is None
        assert options.custom_settings == {}

    def test_conversion_options_custom(self):
        """Test Conversion_Options custom values."""
        options = Conversion_Options(
            preserve_colors=False,
            include_images=False,
            include_notes=True,
            verbose=True,
            output_format="pptx",
            custom_settings={"theme": "professional"}
        )

        assert options.preserve_colors is False
        assert options.include_images is False
        assert options.include_notes is True
        assert options.verbose is True
        assert options.output_format == "pptx"
        assert options.custom_settings["theme"] == "professional"

    def test_create_text_element(self):
        """Test create_text_element utility function."""
        element = create_text_element("Test text")

        assert element.element_type == Element_Type.TEXT
        assert isinstance(element.content, Text_Content)
        assert element.content.text == "Test text"
        assert element.content.formatting == []

    def test_create_text_element_with_formatting(self):
        """Test create_text_element with formatting."""
        element = create_text_element(
            "Test text",
            formatting=[Formatting.BOLD, Formatting.ITALIC]
        )

        assert element.content.formatting == [Formatting.BOLD, Formatting.ITALIC]

    def test_create_text_element_different_type(self):
        """Test create_text_element with different element type."""
        element = create_text_element("Title text", Element_Type.TITLE)

        assert element.element_type == Element_Type.TITLE
        assert element.content.text == "Title text"

    def test_create_image_element(self):
        """Test create_image_element utility function."""
        element = create_image_element("test.png", "Test caption")

        assert element.element_type == Element_Type.IMAGE
        assert element.content['path'] == "test.png"
        assert element.content['caption'] == "Test caption"

    def test_create_image_element_with_position(self):
        """Test create_image_element with position and size."""
        position = Position(x=1.0, y=2.0)
        size = Size(width=6.0, height=4.0)

        element = create_image_element("test.png", "Test caption", position, size)

        assert element.position == position
        assert element.size == size

    def test_create_itemize_element(self):
        """Test create_itemize_element utility function."""
        element = create_itemize_element(["Item 1", "Item 2", "Item 3"])

        assert element.element_type == Element_Type.ITEMIZE
        assert element.content['items'] == ["Item 1", "Item 2", "Item 3"]
        assert element.level == 0

    def test_create_itemize_element_with_level(self):
        """Test create_itemize_element with nesting level."""
        element = create_itemize_element(["Nested item"], level=2)

        assert element.level == 2

    def test_create_equation_element_inline(self):
        """Test create_equation_element utility function."""
        element = create_equation_element("E = mc^2", "inline")

        assert element.element_type == Element_Type.EQUATION
        assert element.content['latex'] == "E = mc^2"
        assert element.content['type'] == 'inline'

    def test_create_equation_element_display(self):
        """Test create_equation_element with display type."""
        element = create_equation_element("\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}", "display")

        assert element.element_type == Element_Type.EQUATION
        assert element.content['latex'] == "\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}"
        assert element.content['type'] == 'display'

    def test_merge_documents(self):
        """Test merge_documents utility function."""
        doc1 = Universal_Document()
        doc1.metadata.title = "Document 1"

        frame1 = Universal_Frame(frame_number=1, title="Frame 1")
        doc1.add_frame(frame1)

        doc2 = Universal_Document()
        doc2.metadata.title = "Document 2"

        frame2 = Universal_Frame(frame_number=2, title="Frame 2")
        frame3 = Universal_Frame(frame_number=3, title="Frame 3")
        doc2.add_frame(frame2)
        doc2.add_frame(frame3)

        merged = merge_documents(doc1, doc2)

        # doc2 metadata should take precedence
        assert merged.metadata.title == "Document 2"

        # All frames should be merged
        assert len(merged.frames) == 3
        assert merged.frames[0].title == "Frame 1"
        assert merged.frames[1].title == "Frame 2"
        assert merged.frames[2].title == "Frame 3"

    def test_element_to_text_content(self):
        """Test Universal_Element.to_text_content method."""
        # Test with string content
        element1 = Universal_Element(Element_Type.TEXT, "Direct text")
        text_content1 = element1.to_text_content()
        assert text_content1.text == "Direct text"

        # Test with Text_Content
        text_content = Text_Content("Formatted text", [Formatting.BOLD])
        element2 = Universal_Element(Element_Type.TEXT, text_content)
        text_content2 = element2.to_text_content()
        assert text_content2.text == "Formatted text"
        assert text_content2.formatting == [Formatting.BOLD]

        # Test with incompatible content
        element3 = Universal_Element(Element_Type.IMAGE, {"path": "test.png"})
        text_content3 = element3.to_text_content()
        assert text_content3 is None

    def test_element_type_values(self):
        """Test Element_Type enum values."""
        assert Element_Type.TEXT.value == "text"
        assert Element_Type.TITLE.value == "title"
        assert Element_TYPE.SUBTITLE.value == "subtitle"
        assert Element_Type.ITEMIZE.value == "itemize"
        assert Element_Type.ENUMERATE.value == "enumerate"
        assert Element_Type.BLOCK.value == "block"
        assert Element_Type.IMAGE.value == "image"
        assert Element_Type.EQUATION.value == "equation"
        assert Element_Type.TABLE.value == "table"
        assert Element_Type.MATH.value == "math"
        assert Element_Type.CODE.value == "code"
        assert Element_Type.HYPERLINK.value == "hyperlink"
        assert Element_Type.SHAPE.value == "shape"
        assert Element_Type.CHART.value == "chart"

    def test_layout_type_values(self):
        """Test Layout_Type enum values."""
        assert Layout_Type.TITLE_SLIDE.value == "title_slide"
        assert Layout_Type.TITLE_AND_CONTENT.value == "title_and_content"
        assert Layout_Type.SECTION_HEADER.value == "section_header"
        assert Layout_Type.TWO_COLUMN.value == "two_column"
        assert Layout_Type.THREE_COLUMN.value == "three_column"
        assert Layout_Type.BLANK.value == "blank"
        assert Layout_Type.CONTENT_ONLY.value == "content_only"

    def test_formatting_values(self):
        """Test Formatting enum values."""
        assert Formatting.BOLD.value == "bold"
        assert Formatting.ITALIC.value == "italic"
        assert Formatting.UNDERLINE.value == "underline"
        assert Formatting.STRIKETHROUGH.value == "strikethrough"
        assert Formatting.SUPERSCRIPT.value == "superscript"
        assert Formatting.SUBSCRIPT.value == "subscript"
        assert Formatting.MONOSPACE.value == "monospace"
        assert Formatting.NORMAL.value == "normal"
