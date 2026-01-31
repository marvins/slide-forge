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

"""Tests for LaTeX parser."""

import pytest
from pathlib import Path
from slideforge.parsers.latex_parser import LaTeX_Parser
from slideforge.models.universal import Element_Type, Layout_Type


class TestLatexParser:
    """Test cases for LaTeX Beamer parser."""

    @pytest.fixture
    def parser(self):
        """Create LaTeX parser instance."""
        return LaTeX_Parser()

    @pytest.fixture
    def sample_latex_content(self):
        """Sample LaTeX content for testing."""
        return r"""
\documentclass{beamer}
\title{Test Presentation}
\author{Test Author}

\begin{document}

\begin{frame}{Test Frame}
    This is a test frame.

    \begin{itemize}
        \item First item
        \item Second item
    \end{itemize}

    Inline equation: $E = mc^2$

    Display equation:
    \begin{equation}
        \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
    \end{equation}
\end{frame}

\end{document}
"""

    def test_parse_basic_frame(self, parser):
        """Test parsing a basic frame with title and content."""
        latex_content = r"""
\begin{frame}{Test Frame Title}
    This is test content.
\end{frame}
"""

        document = parser.parse_string(latex_content, source_path='test.tex')

        assert document.source_format == 'latex'
        assert len(document.frames) == 1

        frame = document.frames[0]
        assert frame.frame_number == 1
        assert frame.title == 'Test Frame Title'
        assert frame.layout == Layout_Type.TITLE_AND_CONTENT
        assert len(frame.elements) == 1

        element = frame.elements[0]
        assert element.element_type == Element_Type.TEXT
        assert 'This is test content.' in element.content.text

    def test_parse_itemize_list(self, parser):
        """Test parsing itemize (bullet) lists."""
        latex_content = r"""
\begin{frame}{List Test}
    \begin{itemize}
        \item First bullet point
        \item Second bullet point
        \item Third bullet point
    \end{itemize}
\end{frame}
"""

        document = parser.parse_string(latex_content, source_path='test.tex')
        frame = document.frames[0]

        # Should have one itemize element
        itemize_elements = [e for e in frame.elements if e.element_type == Element_Type.ITEMIZE]
        assert len(itemize_elements) == 1

        itemize = itemize_elements[0]
        items = itemize.content['items']
        assert len(items) == 3
        assert 'First bullet point' in items[0]
        assert 'Second bullet point' in items[1]
        assert 'Third bullet point' in items[2]

    def test_parse_inline_equations(self, parser):
        """Test parsing inline equations."""
        latex_content = r"""
\begin{frame}{Equation Test}
    Einstein's equation: $E = mc^2$
    Pythagorean theorem: $a^2 + b^2 = c^2$
\end{frame}
"""

        document = parser.parse_string(latex_content, source_path='test.tex')
        frame = document.frames[0]

        # Should have two equation elements
        equation_elements = [e for e in frame.elements if e.element_type == Element_Type.EQUATION]
        assert len(equation_elements) == 2

        # Check first equation
        eq1 = equation_elements[0]
        assert eq1.content['latex'] == 'E = mc^2'
        assert eq1.content['type'] == 'inline'

        # Check second equation
        eq2 = equation_elements[1]
        assert eq2.content['latex'] == 'a^2 + b^2 = c^2'
        assert eq2.content['type'] == 'inline'

    def test_parse_display_equations(self, parser):
        """Test parsing display equations."""
        latex_content = r"""
\begin{frame}{Display Equations}
    Gaussian integral:
    \begin{equation}
        \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
    \end{equation}
\end{frame}
"""

        document = parser.parse_string(latex_content, source_path='test.tex')
        frame = document.frames[0]

        # Should have one equation element
        equation_elements = [e for e in frame.elements if e.element_type == Element_Type.EQUATION]
        assert len(equation_elements) == 1

        equation = equation_elements[0]
        assert '\\int' in equation.content['latex']
        assert '\\sqrt' in equation.content['latex']
        assert equation.content['type'] == 'display'

    def test_parse_mixed_content(self, parser):
        """Test parsing mixed content types."""
        latex_content = r"""
\begin{frame}{Mixed Content}
    Some text content.

    \begin{itemize}
        \item List item with equation: $x^2 + y^2 = z^2$
        \item Another item
    \end{itemize}

    Final equation:
    \begin{equation}
        \sum_{i=1}^{n} i = \frac{n(n+1)}{2}
    \end{equation}
\end{frame}
"""

        document = parser.parse_string(latex_content, source_path='test.tex')
        frame = document.frames[0]

        # Should have text, itemize, and equation elements
        text_elements = [e for e in frame.elements if e.element_type == Element_Type.TEXT]
        itemize_elements = [e for e in frame.elements if e.element_type == Element_Type.ITEMIZE]
        equation_elements = [e for e in frame.elements if e.element_type == Element_Type.EQUATION]

        assert len(text_elements) >= 1
        assert len(itemize_elements) == 1
        assert len(equation_elements) == 1

    def test_parse_empty_frame(self, parser):
        """Test parsing empty frame."""
        latex_content = r"""
\begin{frame}{Empty Frame}
\end{frame}
"""

        document = parser.parse_string(latex_content, source_path='test.tex')
        frame = document.frames[0]

        assert frame.title == 'Empty Frame'
        assert len(frame.elements) == 0

    def test_parse_multiple_frames(self, parser):
        """Test parsing multiple frames."""
        latex_content = r"""
\begin{frame}{First Frame}
    First content.
\end{frame}

\begin{frame}{Second Frame}
    Second content.
\end{frame}
"""

        document = parser.parse_string(latex_content, source_path='test.tex')

        assert len(document.frames) == 2
        assert document.frames[0].title == 'First Frame'
        assert document.frames[1].title == 'Second Frame'

    def test_extract_metadata(self, parser):
        """Test metadata extraction."""
        latex_content = r"""
\documentclass{beamer}
\title{My Presentation}
\author{John Doe}
\date{January 2026}

\begin{document}
\begin{frame}{Test}
    Content
\end{frame}
\end{document}
"""

        document = parser.parse_string(latex_content, source_path='test.tex')

        assert document.metadata.title == 'My Presentation'
        assert document.metadata.author == 'John Doe'
        assert document.metadata.date == 'January 2026'

    def test_skip_frametitle_duplicates(self, parser):
        """Test that frametitle doesn't appear as regular text."""
        latex_content = r"""
\begin{frame}{Frame Title}
    This should be the only text element.
    \frametitle{Frame Title}
    This should not create duplicate text.
\end{frame}
"""

        document = parser.parse_string(latex_content, source_path='test.tex')
        frame = document.frames[0]

        text_elements = [e for e in frame.elements if e.element_type == Element_Type.TEXT]
        # Should only have one text element (not counting the frametitle)
        assert len(text_elements) == 1
        assert 'This should be the only text element.' in text_elements[0].content.text
        assert 'This should not create duplicate text.' in text_elements[0].content.text

    def test_get_supported_extensions(self, parser):
        """Test supported file extensions."""
        extensions = parser.get_supported_extensions()
        assert '.tex' in extensions
        assert '.latex' in extensions
