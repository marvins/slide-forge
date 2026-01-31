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

"""Abstract base classes for Slide Forge parsers and builders."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path

from .models.universal import Universal_Document, Conversion_Options, Slide_Structure


class Base_Parser(ABC):
    """Abstract base class for input format parsers."""

    @abstractmethod
    def parse_file(self, filepath: Path, **kwargs) -> Universal_Document:
        """
        Parse a file and return a Universal_Document object.

        Args:
            filepath: Path to input file
            **kwargs: Additional parsing options

        Returns:
            Universal_Document object with parsed content

        Raises:
            ParseError: If parsing fails
        """
        pass

    @abstractmethod
    def parse_string(self, content: str, **kwargs) -> Universal_Document:
        """
        Parse string content and return a Universal_Document object.

        Args:
            content: String content to parse
            **kwargs: Additional parsing options

        Returns:
            Universal_Document object with parsed content

        Raises:
            ParseError: If parsing fails
        """
        pass

    @abstractmethod
    def get_supported_extensions(self) -> list[str]:
        """
        Get list of supported file extensions.

        Returns:
            List of supported file extensions (e.g., ['.tex', '.pptx'])
        """
        pass

    def validate_file(self, filepath: Path) -> bool:
        """
        Validate that the file can be parsed.

        Args:
            filepath: Path to file to validate

        Returns:
            True if file is supported and valid
        """
        if not filepath.exists():
            return False

        return filepath.suffix.lower() in self.get_supported_extensions()


class Base_Builder(ABC):
    """Abstract base class for output format builders."""

    @abstractmethod
    def build_presentation(self, slides: list[Slide_Structure],
                          output_file: Path, **kwargs) -> bool:
        """
        Build a presentation from slide structures.

        Args:
            slides: List of Slide_Structure objects
            output_file: Path to output file
            **kwargs: Additional build options

        Returns:
            True if build successful, False otherwise

        Raises:
            BuilderError: If build fails
        """
        pass

    @abstractmethod
    def get_supported_extensions(self) -> list[str]:
        """
        Get list of supported output extensions.

        Returns:
            List of supported output extensions (e.g., ['.pptx', '.tex'])
        """
        pass

    @abstractmethod
    def get_default_theme(self) -> str:
        """
        Get the default theme for this builder.

        Returns:
            Default theme name
        """
        pass

    def validate_output_path(self, output_file: Path) -> bool:
        """
        Validate that the output path is supported.

        Args:
            output_file: Path to output file

        Returns:
            True if output format is supported
        """
        return output_file.suffix.lower() in self.get_supported_extensions()


class Base_Mapper(ABC):
    """Abstract base class for content mapping between formats."""

    @abstractmethod
    def map_document(self, document: Document, target_format: str,
                   **kwargs) -> list[Slide_Structure]:
        """
        Map a Document to Slide_Structure list for target format.

        Args:
            document: Source Document object
            target_format: Target format ('pptx', 'latex', etc.)
            **kwargs: Additional mapping options

        Returns:
            List of Slide_Structure objects

        Raises:
            MappingError: If mapping fails
        """
        pass

    @abstractmethod
    def get_supported_conversions(self) -> Dict[str, list[str]]:
        """
        Get supported conversion mappings.

        Returns:
            Dictionary mapping source formats to list of target formats
            e.g., {'latex': ['pptx'], 'pptx': ['latex']}
        """
        pass

    def can_convert(self, source_format: str, target_format: str) -> bool:
        """
        Check if conversion from source to target format is supported.

        Args:
            source_format: Source format
            target_format: Target format

        Returns:
            True if conversion is supported
        """
        supported = self.get_supported_conversions()
        return (source_format in supported and
                target_format in supported[source_format])


class Format_Detector:
    """Utility class for detecting file formats."""

    def __init__(self):
        self.format_mappings = {
            '.tex': 'latex',
            '.latex': 'latex',
            '.pptx': 'pptx',
            '.ppt': 'pptx'
        }

    def detect_format(self, filepath: Path) -> Optional[str]:
        """
        Detect format from file path.

        Args:
            filepath: Path to file

        Returns:
            Format string or None if unknown
        """
        suffix = filepath.suffix.lower()
        return self.format_mappings.get(suffix)

    def get_format_from_extension(self, extension: str) -> Optional[str]:
        """
        Get format from file extension.

        Args:
            extension: File extension (with or without dot)

        Returns:
            Format string or None if unknown
        """
        if not extension.startswith('.'):
            extension = '.' + extension
        return self.format_mappings.get(extension.lower())
