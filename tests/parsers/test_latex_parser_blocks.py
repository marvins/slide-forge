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

"""Unit tests for LaTeX parser block environment support."""

import pytest
from src.slideforge.parsers.latex_parser import LaTeX_Parser
from src.slideforge.models.universal import Element_Type


class TestLaTeXParserBlocks:
    """Test LaTeX parser block environment functionality."""

    @pytest.fixture
    def parser(self):
        """Create a LaTeX parser instance."""
        return LaTeX_Parser()

    def test_basic_block_parsing(self, parser):
        """Test parsing a basic block environment."""
        latex_content = r"""
        \begin{frame}{Test Frame}
        \begin{block}{Block Title}
        This is block content.
        \end{block}
        \end{frame}
        """

        document = parser.parse_string(latex_content)
        frame = document.frames[0]

        # Should have one block element
        block_elements = [e for e in frame.elements if e.element_type == Element_Type.BLOCK]
        assert len(block_elements) == 1

        block = block_elements[0]
        assert block.content['type'] == 'block'
        assert block.content['title'] == 'Block Title'
        assert 'This is block content.' in block.content['content']

    def test_alertblock_parsing(self, parser):
        """Test parsing an alert block environment."""
        latex_content = r"""
        \begin{frame}{Test Frame}
        \begin{alertblock}{Important}
        This is an important alert.
        \end{alertblock}
        \end{frame}
        """

        document = parser.parse_string(latex_content)
        frame = document.frames[0]

        # Should have one block element
        block_elements = [e for e in frame.elements if e.element_type == Element_Type.BLOCK]
        assert len(block_elements) == 1

        block = block_elements[0]
        assert block.content['type'] == 'alertblock'
        assert block.content['title'] == 'Important'
        assert 'This is an important alert.' in block.content['content']

    def test_exampleblock_parsing(self, parser):
        """Test parsing an example block environment."""
        latex_content = r"""
        \begin{frame}{Test Frame}
        \begin{exampleblock}{Example}
        This is an example block.
        \end{exampleblock}
        \end{frame}
        """

        document = parser.parse_string(latex_content)
        frame = document.frames[0]

        # Should have one block element
        block_elements = [e for e in frame.elements if e.element_type == Element_Type.BLOCK]
        assert len(block_elements) == 1

        block = block_elements[0]
        assert block.content['type'] == 'exampleblock'
        assert block.content['title'] == 'Example'
        assert 'This is an example block.' in block.content['content']

    def test_multiple_blocks(self, parser):
        """Test parsing multiple block environments."""
        latex_content = r"""
        \begin{frame}{Test Frame}
        \begin{block}{First Block}
        First block content.
        \end{block}

        \begin{alertblock}{Alert}
        Alert content.
        \end{alertblock}

        \begin{exampleblock}{Example}
        Example content.
        \end{exampleblock}
        \end{frame}
        """

        document = parser.parse_string(latex_content)
        frame = document.frames[0]

        # Should have three block elements
        block_elements = [e for e in frame.elements if e.element_type == Element_Type.BLOCK]
        assert len(block_elements) == 3

        # Check each block type
        block_types = [block.content['type'] for block in block_elements]
        assert 'block' in block_types
        assert 'alertblock' in block_types
        assert 'exampleblock' in block_types

    def test_block_with_special_characters(self, parser):
        """Test parsing blocks with special characters."""
        latex_content = r"""
        \begin{frame}{Test Frame}
        \begin{block}{Math \& Logic}
        Content with special characters: \$, \%, \&.
        \end{block}
        \end{frame}
        """

        document = parser.parse_string(latex_content)
        frame = document.frames[0]

        block_elements = [e for e in frame.elements if e.element_type == Element_Type.BLOCK]
        assert len(block_elements) == 1

        block = block_elements[0]
        assert block.content['title'] == 'Math & Logic'
        assert 'Content with special characters' in block.content['content']

    def test_block_with_multiline_content(self, parser):
        """Test parsing blocks with multiline content."""
        latex_content = r"""
        \begin{frame}{Test Frame}
        \begin{block}{Multiline Block}
        First line of content.
        Second line of content.
        Third line of content.
        \end{block}
        \end{frame}
        """

        document = parser.parse_string(latex_content)
        frame = document.frames[0]

        block_elements = [e for e in frame.elements if e.element_type == Element_Type.BLOCK]
        assert len(block_elements) == 1

        block = block_elements[0]
        content = block.content['content']
        assert 'First line of content.' in content
        assert 'Second line of content.' in content
        assert 'Third line of content.' in content

    def test_block_with_empty_content(self, parser):
        """Test parsing blocks with empty content."""
        latex_content = r"""
        \begin{frame}{Test Frame}
        \begin{block}{Empty Block}
        \end{block}
        \end{frame}
        """

        document = parser.parse_string(latex_content)
        frame = document.frames[0]

        block_elements = [e for e in frame.elements if e.element_type == Element_Type.BLOCK]
        assert len(block_elements) == 1

        block = block_elements[0]
        assert block.content['title'] == 'Empty Block'
        assert block.content['content'] == ''

    def test_block_mixed_with_other_content(self, parser):
        """Test parsing blocks mixed with other content."""
        latex_content = r"""
        \begin{frame}{Test Frame}
        This is some regular text.

        \begin{block}{Block Title}
        This is block content.
        \end{block}

        This is more regular text.

        \begin{itemize}
        \item List item 1
        \item List item 2
        \end{itemize}
        \end{frame}
        """

        document = parser.parse_string(latex_content)
        frame = document.frames[0]

        # Should have text, block, and itemize elements
        text_elements = [e for e in frame.elements if e.element_type == Element_Type.TEXT]
        block_elements = [e for e in frame.elements if e.element_type == Element_Type.BLOCK]
        itemize_elements = [e for e in frame.elements if e.element_type == Element_Type.ITEMIZE]

        assert len(text_elements) >= 1
        assert len(block_elements) == 1
        assert len(itemize_elements) == 1

        block = block_elements[0]
        assert block.content['title'] == 'Block Title'
        assert 'This is block content.' in block.content['content']
