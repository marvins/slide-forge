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

"""Tests for LaTeX parser structural functionality."""

import pytest
from pathlib import Path
from slideforge.parsers.latex_parser import LaTeX_Parser
from slideforge.models.universal import Layout_Type, Element_Type


class TestLaTeXParserStructure:
    """Test cases for LaTeX parser structural features."""

    @pytest.fixture
    def parser(self):
        """Create LaTeX parser instance."""
        return LaTeX_Parser()

    def test_title_slide_detection(self, parser):
        """Test that title slides are properly detected from \\titlepage."""
        latex_content = r"""
\documentclass{beamer}
\title{Test Presentation}
\author{Test Author}
\date{2024}

\begin{document}
\begin{frame}
\titlepage
\end{frame}

\begin{frame}{Regular Slide}
Some content here
\end{frame}
\end{document}
"""

        document = parser.parse_string(latex_content)

        # Should have 2 frames
        assert len(document.frames) == 2

        # First frame should be title slide
        title_frame = document.frames[0]
        assert title_frame.layout == Layout_Type.TITLE_SLIDE
        assert title_frame.title == "Test Presentation"

        # Second frame should be regular slide
        content_frame = document.frames[1]
        assert content_frame.layout == Layout_Type.TITLE_AND_CONTENT
        assert content_frame.title == "Regular Slide"

    def test_table_of_contents_generation(self, parser):
        """Test that table of contents is properly generated."""
        latex_content = r"""
\documentclass{beamer}
\title{Test Presentation}
\author{Test Author}

\begin{document}
\begin{frame}{Outline}
\tableofcontents
\end{frame}

\section{Introduction}
\section{Methods}
\section{Results}
\section{Conclusion}
\end{document}
"""

        document = parser.parse_string(latex_content)

        # Should collect sections
        assert len(parser.sections) == 4
        assert "Introduction" in parser.sections
        assert "Methods" in parser.sections
        assert "Results" in parser.sections
        assert "Conclusion" in parser.sections

        # Should have outline frame with table of contents
        outline_frame = document.frames[0]
        assert outline_frame.title == "Outline"
        assert len(outline_frame.elements) == 1

        toc_element = outline_frame.elements[0]
        assert toc_element.element_type == Element_Type.ITEMIZE
        assert toc_element.content['items'] == ['Introduction', 'Methods', 'Results', 'Conclusion']

    def test_metadata_extraction(self, parser):
        """Test that metadata is properly extracted."""
        latex_content = r"""
\documentclass{beamer}
\title{Advanced Machine Learning}
\subtitle{Deep Learning Techniques}
\author{Dr. Jane Smith}
\institute{University of Technology}
\date{January 2024}

\begin{document}
\begin{frame}
\titlepage
\end{frame}
\end{document}
"""

        document = parser.parse_string(latex_content)

        # Check extracted metadata
        assert document.metadata.title == "Advanced Machine Learning"
        assert document.metadata.author == "Dr. Jane Smith"
        assert document.metadata.date == "January 2024"

        # Check document class extraction
        assert 'documentclass' in document.metadata.custom_properties
        assert document.metadata.custom_properties['documentclass'] == 'beamer'

    def test_complex_document_structure(self, parser):
        """Test parsing of a complete document with all structural elements."""
        latex_content = r"""
\documentclass[aspectratio=169]{beamer}
\title{Complex Presentation}
\author{Research Team}
\date{\today}

\begin{document}

% Title slide
\begin{frame}
\titlepage
\end{frame}

% Outline
\begin{frame}{Agenda}
\tableofcontents
\end{frame}

% Section 1
\section{Background}

\begin{frame}{Background}
\begin{itemize}
    \item First point
    \item Second point
\end{itemize}
\end{frame}

% Section 2
\section{Methodology}

\begin{frame}{Methodology}
Some methodology content
\end{frame}

% Section 3
\section{Results}

\begin{frame}{Results}
Results content here
\end{frame}

\end{document}
"""

        document = parser.parse_string(latex_content)

        # Should have 5 frames total
        assert len(document.frames) == 5

        # Check title slide
        title_frame = document.frames[0]
        assert title_frame.layout == Layout_Type.TITLE_SLIDE
        assert title_frame.title == "Complex Presentation"

        # Check outline slide
        outline_frame = document.frames[1]
        assert outline_frame.title == "Agenda"
        assert len(outline_frame.elements) == 1
        toc_element = outline_frame.elements[0]
        assert toc_element.element_type == Element_Type.ITEMIZE
        assert toc_element.content['items'] == ["Background", "Methodology", "Results"]

        # Check section collection
        assert len(parser.sections) == 3
        assert parser.sections == ["Background", "Methodology", "Results"]

        # Check content slides
        background_frame = document.frames[2]
        assert background_frame.title == "Background"
        assert len(background_frame.elements) == 1  # itemize content

        methodology_frame = document.frames[3]
        assert methodology_frame.title == "Methodology"

        results_frame = document.frames[4]
        assert results_frame.title == "Results"

    def test_empty_sections_handling(self, parser):
        """Test handling of documents with no sections."""
        latex_content = r"""
\documentclass{beamer}
\title{Simple Presentation}
\author{Simple Author}

\begin{document}
\begin{frame}
\titlepage
\end{frame}

\begin{frame}{Content}
No sections here
\end{frame}
\end{document}
"""

        document = parser.parse_string(latex_content)

        # Should have no sections collected
        assert len(parser.sections) == 0

        # Should still parse frames correctly
        assert len(document.frames) == 2
        assert document.frames[0].layout == Layout_Type.TITLE_SLIDE

    def test_multiple_table_of_contents(self, parser):
        """Test handling of multiple table of contents commands."""
        latex_content = r"""
\documentclass{beamer}
\title{Multi TOC Test}

\begin{document}
\section{Part 1}
\section{Part 2}

\begin{frame}{First Outline}
\tableofcontents
\end{frame}

\begin{frame}{Second Outline}
\tableofcontents
\end{frame}
\end{document}
"""

        document = parser.parse_string(latex_content)

        # Should have 2 outline frames
        assert len(document.frames) == 2

        # Both should have table of contents
        for frame in document.frames:
            assert len(frame.elements) == 1
            assert frame.elements[0].element_type == Element_Type.ITEMIZE
            assert frame.elements[0].content['items'] == ['Part 1', 'Part 2']

    def test_section_with_special_characters(self, parser):
        """Test handling of sections with special characters."""
        latex_content = r"""
\documentclass{beamer}
\title{Special Characters}

\begin{document}
\section{Math \& Logic}
\section{Data \& Analysis}
\section{AI/ML: Future \& Present}

\begin{frame}{Outline}
\tableofcontents
\end{frame}
\end{document}
"""

        document = parser.parse_string(latex_content)

        # Should handle special characters correctly
        assert len(parser.sections) == 3
        assert "Math & Logic" in parser.sections
        assert "Data & Analysis" in parser.sections
        assert "AI/ML: Future & Present" in parser.sections

        # Table of contents should preserve special characters
        toc_element = document.frames[0].elements[0]
        assert toc_element.element_type == Element_Type.ITEMIZE
        assert "Math & Logic" in toc_element.content['items']
        assert "Data & Analysis" in toc_element.content['items']
        assert "AI/ML: Future & Present" in toc_element.content['items']
