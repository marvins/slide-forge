#!/usr/bin/env python3

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
Failing test for itemize inline equation parsing.
This test documents a known limitation that should be fixed later.
"""

import pytest
from slideforge.parsers.latex_parser import LaTeX_Parser
from slideforge.models.universal import Element_Type


class TestItemizeInlineEquations:
    """Test inline equations within itemize lists."""

    @pytest.fixture
    def parser(self):
        """Create LaTeX parser instance."""
        return LaTeX_Parser()

    def test_itemize_with_inline_equations(self, parser):
        """
        Test that inline equations within itemize items are properly extracted.

        This test currently FAILS because the itemize parser doesn't handle inline equations.
        When this test passes, it means the feature has been implemented.

        TODO: Implement inline equation extraction from itemize items
        """
        latex_content = r"""
\begin{frame}{Mixed Content}
    \begin{itemize}
        \item List item with equation: $x^2 + y^2 = z^2$
        \item Another item
    \end{itemize}
\end{frame}
"""

        document = parser.parse_string(latex_content, source_path='test.tex')
        frame = document.frames[0]

        # Count elements by type
        element_counts = {}
        equation_types = []

        for element in frame.elements:
            element_type = element.element_type.value
            element_counts[element_type] = element_counts.get(element_type, 0) + 1

            if element_type == "equation":
                eq_type = element.content.get('type', 'unknown')
                equation_types.append(eq_type)

        # Current behavior (failing test expectation):
        # - We get 1 itemize element with the equation as plain text
        # - No separate equation elements are extracted

        # Expected behavior (when feature is implemented):
        # - Should get 1 itemize element
        # - Should get 1 inline equation element
        # - The equation should be extracted from the itemize item

        # This assertion documents the current limitation
        assert element_counts.get("itemize", 0) == 1, "Should have one itemize element"

        # This assertion will FAIL until the feature is implemented
        # TODO: Implement inline equation extraction from itemize items
        assert element_counts.get("equation", 0) == 1, "Should extract inline equation from itemize"
        assert "inline" in equation_types, "Should identify equation as inline type"

    def test_itemize_with_multiple_inline_equations(self, parser):
        """
        Test multiple inline equations within a single itemize item.

        This test documents another limitation that should be addressed.
        """
        latex_content = r"""
\begin{frame}{Multiple Equations}
    \begin{itemize}
        \item First equation: $E = mc^2$ and second: $a^2 + b^2 = c^2$
    \end{itemize}
\end{frame}
"""

        document = parser.parse_string(latex_content, source_path='test.tex')
        frame = document.frames[0]

        # Current behavior: Everything is treated as plain text in the itemize
        itemize_elements = [e for e in frame.elements if e.element_type == Element_Type.ITEMIZE]
        assert len(itemize_elements) == 1

        # Expected behavior (when implemented):
        # - Should extract 2 inline equations from the itemize item
        # - Should preserve the text parts as separate elements or within the itemize

        # TODO: Implement multiple inline equation extraction
        pass

    def test_itemize_with_display_equation(self, parser):
        """
        Test display equations within itemize items.

        This is another edge case that should be handled.
        """
        latex_content = r"""
\begin{frame}{Display in Itemize}
    \begin{itemize}
        \item Here's an equation:
        \begin{equation}
            \sum_{i=1}^{n} i = \frac{n(n+1)}{2}
        \end{equation}
        \item Next item
    \end{itemize}
\end{frame}
"""

        document = parser.parse_string(latex_content, source_path='test.tex')
        frame = document.frames[0]

        # Current behavior: Display equation is not properly handled within itemize
        # Expected behavior: Should extract the display equation properly

        # TODO: Handle display equations within itemize environments
        pass
