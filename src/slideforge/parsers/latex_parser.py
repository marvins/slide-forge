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

"""LaTeX Beamer parser implementation."""

import re
from pathlib import Path
from typing import List, Dict, Any, Optional

from ..base import Base_Parser
from ..models.universal import (
    Universal_Document, Universal_Frame, Universal_Element,
    Metadata, Element_Type, Layout_Type, Text_Content,
    create_text_element, create_image_element, create_itemize_element, create_equation_element
)
from ..exceptions import ParseError


class LaTeX_Parser(Base_Parser):
    """Parser for LaTeX Beamer presentations."""

    def __init__(self):
        """Initialize LaTeX parser."""
        # Pattern to match \begin{frame}{optional title} ... \end{frame}
        self.frame_pattern = re.compile(r'\\begin\{frame\}(?:\{([^}]*)\})?\s*(.*?)(?=\\end\{frame\}|\\begin\{frame\}|$)', re.DOTALL | re.IGNORECASE)
        self.title_pattern = re.compile(r'\\frametitle\{([^}]+)\}', re.IGNORECASE)
        self.itemize_pattern = re.compile(r'\\item\s+(.+)', re.IGNORECASE)
        self.includegraphics_pattern = re.compile(r'\\includegraphics(?:\[[^\]]*\])\{([^}]+)\}', re.IGNORECASE)
        # Equation patterns for inline and display math
        self.inline_equation_pattern = re.compile(r'\$([^$]+)\$', re.IGNORECASE)
        self.display_equation_pattern = re.compile(r'\\begin\{equation\*?\}(.*?)\\end\{equation\*?\}', re.DOTALL | re.IGNORECASE)
        self.display_equation_pattern_alt = re.compile(r'\\\[(.*?)\\\]', re.DOTALL | re.IGNORECASE)

    def parse_file(self, filepath: Path, **kwargs) -> Universal_Document:
        """
        Parse a LaTeX Beamer file and return a Universal_Document.

        Args:
            filepath: Path to .tex file
            **kwargs: Additional parsing options

        Returns:
            Universal_Document object
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            return self.parse_string(content, **kwargs)

        except FileNotFoundError:
            raise ParseError(f"File not found: {filepath}", file_path=str(filepath))
        except Exception as e:
            raise ParseError(f"Error reading file: {e}", file_path=str(filepath))

    def parse_string(self, content: str, **kwargs) -> Universal_Document:
        """
        Parse LaTeX Beamer content and return a Universal_Document.

        Args:
            content: LaTeX content as string
            **kwargs: Additional parsing options

        Returns:
            Universal_Document object
        """
        document = Universal_Document()
        document.source_format = 'latex'

        # Extract metadata
        self._extract_metadata(content, document)

        # Extract frames
        self._extract_frames(content, document)

        return document

    def get_supported_extensions(self) -> List[str]:
        """Get supported file extensions."""
        return ['.tex', '.latex']

    def _extract_metadata(self, content: str, document: Universal_Document):
        """Extract metadata from LaTeX content."""
        # Extract title
        title_match = re.search(r'\\title\{([^}]+)\}', content, re.IGNORECASE)
        if title_match:
            document.metadata.title = title_match.group(1).strip()

        # Extract author
        author_match = re.search(r'\\author\{([^}]+)\}', content, re.IGNORECASE)
        if author_match:
            document.metadata.author = author_match.group(1).strip()

        # Extract date
        date_match = re.search(r'\\date\{([^}]+)\}', content, re.IGNORECASE)
        if date_match:
            document.metadata.date = date_match.group(1).strip()

        # Extract document class
        docclass_match = re.search(r'\\documentclass(?:\[[^\]]*\])\{([^}]+)\}', content, re.IGNORECASE)
        if docclass_match:
            document.metadata.custom_properties['documentclass'] = docclass_match.group(1).strip()

    def _extract_frames(self, content: str, document: Universal_Document):
        """Extract frames from LaTeX content."""
        frame_matches = self.frame_pattern.finditer(content)

        frame_number = 1
        for match in frame_matches:
            frame_title = match.group(1)  # Title from \begin{frame}{title}
            frame_content = match.group(2)  # Frame content
            frame = self._parse_frame(frame_content, frame_number, frame_title)
            document.add_frame(frame)
            frame_number += 1

    def _parse_frame(self, frame_content: str, frame_number: int, frame_title: str = None) -> Universal_Frame:
        """Parse a single frame."""
        frame = Universal_Frame(frame_number=frame_number)

        # Set title from \begin{frame}{title} if available
        if frame_title and frame_title.strip():
            frame.title = frame_title.strip()
            frame.layout = Layout_Type.TITLE_AND_CONTENT
        else:
            # Extract frame title from \frametitle command
            title_match = self.title_pattern.search(frame_content)
            if title_match:
                frame.title = title_match.group(1).strip()
                frame.layout = Layout_Type.TITLE_AND_CONTENT
            else:
                # Check if this might be a title slide
                if frame_number == 1 and '\\titlepage' in frame_content:
                    frame.layout = Layout_Type.TITLE_SLIDE

        # Parse elements
        elements = self._parse_elements(frame_content, frame.layout)
        for element in elements:
            frame.add_element(element)

        return frame

    def _parse_elements(self, content: str, layout: Layout_Type) -> List[Universal_Element]:
        """Parse elements from frame content."""
        elements = []
        lines = content.split('\n')

        current_itemize = []
        in_itemize = False
        in_equation = False
        equation_lines = []
        current_text = []

        for line in lines:
            line = line.strip()
            if not line or line.startswith('%'):
                continue

            # Skip frametitle commands as they're handled separately
            if line.startswith('\\frametitle'):
                continue

            # Handle itemize environments
            if line.startswith('\\begin{itemize}') or line.startswith(r'\begin{itemize}'):
                # Flush any accumulated text
                if current_text:
                    text_content = ' '.join(current_text)
                    elements.append(create_text_element(text_content))
                    current_text = []
                in_itemize = True
                continue
            elif line.startswith('\\end{itemize}') or line.startswith(r'\end{itemize}'):
                # Flush any accumulated text
                if current_text:
                    text_content = ' '.join(current_text)
                    elements.append(create_text_element(text_content))
                    current_text = []
                if current_itemize:
                    elements.append(create_itemize_element(current_itemize))
                    current_itemize = []
                in_itemize = False
                continue
            elif in_itemize:
                item_match = self.itemize_pattern.match(line)
                if item_match:
                    current_itemize.append(item_match.group(1).strip())
                continue

            # Handle multi-line display equations
            if '\\\\begin{equation}' in line or '\\begin{equation}' in line:
                # Flush any accumulated text
                if current_text:
                    text_content = ' '.join(current_text)
                    elements.append(create_text_element(text_content))
                    current_text = []
                in_equation = True
                equation_lines = []
                continue

            if '\\\\end{equation}' in line or '\\end{equation}' in line:
                if in_equation:
                    equation_content = '\n'.join(equation_lines)
                    equation_text = equation_content.strip()
                    if equation_text:
                        elements.append(create_equation_element(equation_text, 'display'))
                    in_equation = False
                    equation_lines = []
                continue

            if in_equation:
                equation_lines.append(line)
                continue

            # Handle includegraphics
            img_match = self.includegraphics_pattern.search(line)
            if img_match:
                # Flush any accumulated text
                if current_text:
                    text_content = ' '.join(current_text)
                    elements.append(create_text_element(text_content))
                    current_text = []
                img_path = img_match.group(1).strip()
                elements.append(create_image_element(img_path))
                continue

            # Handle inline equations - extract equation but keep surrounding text
            inline_eq_match = self.inline_equation_pattern.search(line)
            if inline_eq_match:
                # Split the line into text and equation parts
                parts = self.inline_equation_pattern.split(line)
                for i, part in enumerate(parts):
                    if part.strip():  # Non-empty text part
                        if i % 2 == 0:  # Text part
                            current_text.append(part.strip())
                        else:  # Equation part
                            # Flush any accumulated text first
                            if current_text:
                                text_content = ' '.join(current_text)
                                elements.append(create_text_element(text_content))
                                current_text = []
                            elements.append(create_equation_element(part.strip(), 'inline'))
                continue

            # Handle text content - accumulate consecutive text lines
            # Skip frametitle lines since they're already extracted as frame titles
            if self.title_pattern.search(line):
                continue

            # Remove LaTeX commands for basic text extraction
            clean_line = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^\]]*\])?\{[^}]*\}', '', line)
            clean_line = re.sub(r'[{}]', '', clean_line).strip()

            if clean_line and not clean_line.startswith('\\'):
                current_text.append(clean_line)

        # Flush any remaining text
        if current_text:
            text_content = ' '.join(current_text)
            elements.append(create_text_element(text_content))

        return elements
