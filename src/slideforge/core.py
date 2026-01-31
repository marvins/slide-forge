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

"""Slide Forge Core - Bidirectional presentation converter."""

#  Python Standard Libraries
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

#  Project Libraries
from .base import Base_Parser, Base_Builder, Base_Mapper, Format_Detector
from .models.universal import Universal_Document, Conversion_Options
from .exceptions import Slide_Forge_Error, ParseError, BuilderError, MappingError


class Slide_Forge:
    """
    Main controller for Slide Forge bidirectional conversions.

    Supports conversions between LaTeX Beamer, PowerPoint, and other presentation formats.
    """

    def __init__(self):
        """Initialize Slide Forge with default configuration."""
        self.logger = logging.getLogger(__name__)

        # Initialize components
        self.parsers = {}
        self.builders = {}
        self.mapper = None
        self.format_detector = Format_Detector()

        # Set default options
        self.default_options = Conversion_Options()

        # Initialize components (will register available parsers/builders)
        self._initialize_components()

    def _initialize_components(self):
        """Initialize available parsers and builders."""
        try:
            # Import and register LaTeX parser
            from .parsers.latex_parser import LaTeX_Parser
            self.register_parser('latex', LaTeX_Parser())
            self.logger.info("Registered LaTeX parser")
        except ImportError:
            self.logger.warning("LaTeX parser not available")

        try:
            # Import and register PowerPoint parser (future)
            # from .parsers.pptx_parser import PowerPoint_Parser
            # self.register_parser('pptx', PowerPoint_Parser())
            # self.logger.info("Registered PowerPoint parser")
            pass
        except ImportError:
            self.logger.warning("PowerPoint parser not available")

        try:
            # Import and register PowerPoint builder
            from .builders.powerpoint_builder import PowerPoint_Builder
            self.register_builder('pptx', PowerPoint_Builder())
            self.logger.info("Registered PowerPoint builder")
        except ImportError:
            self.logger.warning("PowerPoint builder not available")

        try:
            # Import and register LaTeX builder (future)
            # from .builders.latex_builder import LaTeX_Builder
            # self.register_builder('latex', LaTeX_Builder())
            # self.logger.info("Registered LaTeX builder")
            pass
        except ImportError:
            self.logger.warning("LaTeX builder not available")

        try:
            # Import and register content mapper
            from .mappers.content_mapper import Content_Mapper
            self.mapper = Content_Mapper()
            self.logger.info("Registered content mapper")
        except ImportError:
            self.logger.warning("Content mapper not available")

    def register_parser(self, format_name: str, parser: Base_Parser):
        """
        Register a parser for a specific format.

        Args:
            format_name: Format identifier (e.g., 'latex', 'pptx')
            parser: Parser instance
        """
        self.parsers[format_name] = parser
        self.logger.info(f"Registered parser for format: {format_name}")

    def register_builder(self, format_name: str, builder: Base_Builder):
        """
        Register a builder for a specific format.

        Args:
            format_name: Format identifier (e.g., 'pptx', 'latex')
            builder: Builder instance
        """
        self.builders[format_name] = builder
        self.logger.info(f"Registered builder for format: {format_name}")

    def register_mapper(self, mapper: Base_Mapper):
        """
        Register a content mapper.

        Args:
            mapper: Mapper instance
        """
        self.mapper = mapper
        self.logger.info("Registered content mapper")

    def convert_file(self, input_file: str, output_file: str, **kwargs) -> bool:
        """
        Convert a presentation file from one format to another.

        Args:
            input_file: Path to input file
            output_file: Path to output file
            **kwargs: Additional conversion options
                - theme: Output theme
                - preserve_colors: Preserve colors from source
                - include_images: Include images in output
                - verbose: Enable verbose logging
                - source_format: Force source format detection
                - target_format: Force target format detection

        Returns:
            True if conversion successful, False otherwise

        Raises:
            Slide_Forge_Error: If conversion fails
        """
        try:
            # Convert paths
            input_path = Path(input_file)
            output_path = Path(output_file)

            # Create conversion options
            default_dict = self.default_options.to_dict()

            # Merge custom_settings properly
            kwargs_custom_settings = kwargs.get('custom_settings', {})
            merged_custom_settings = {**default_dict.get('custom_settings', {}), **kwargs_custom_settings}

            # Create final kwargs dict
            final_kwargs = {**default_dict, **kwargs}
            final_kwargs['custom_settings'] = merged_custom_settings

            options = Conversion_Options(**final_kwargs)

            if options.verbose:
                self.logger.setLevel(logging.DEBUG)
                self.logger.info(f"Starting conversion: {input_path} -> {output_path}")

            # Detect formats
            source_format = kwargs.get('source_format') or self.format_detector.detect_format(input_path)
            target_format = kwargs.get('target_format') or self.format_detector.detect_format(output_path)

            if not source_format:
                raise ParseError(f"Cannot detect source format for: {input_path}")
            if not target_format:
                raise BuilderError(f"Cannot detect target format for: {output_path}")

            if options.verbose:
                self.logger.info(f"Converting from {source_format} to {target_format}")

            # Validate parsers and builders
            if source_format not in self.parsers:
                raise ParseError(f"No parser available for format: {source_format}")
            if target_format not in self.builders:
                raise BuilderError(f"No builder available for format: {target_format}")

            # Parse input document
            parser = self.parsers[source_format]
            document = parser.parse_file(input_path, **options.custom_settings)
            document.source_format = source_format
            document.source_path = input_path

            if options.verbose:
                self.logger.info(f"Parsed {document.get_total_frames()} frames from {source_format}")

            # Map content between formats
            if self.mapper:
                if not self.mapper.can_convert(source_format, target_format):
                    raise MappingError(f"Cannot convert from {source_format} to {target_format}")

                slide_structures = self.mapper.map_document(document, target_format, **options.custom_settings)
                if options.verbose:
                    self.logger.info(f"Mapped content to {len(slide_structures)} slide structures")
            else:
                # Direct conversion when no mapper needed (same format)
                slide_structures = self._document_to_slides(document)
                if options.verbose:
                    self.logger.info("Direct conversion (no mapping needed)")

            # Build output document
            builder = self.builders[target_format]

            # Pass source path for image resolution (convert to string)
            build_options = {**options.custom_settings, 'source_path': str(document.source_path)}
            success = builder.build_presentation(slide_structures, output_path, **build_options)

            if success and options.verbose:
                self.logger.info(f"Successfully built {target_format} document: {output_path}")

            return success

        except Exception as e:
            self.logger.error(f"Conversion failed: {e}")
            if isinstance(e, Slide_Forge_Error):
                raise
            else:
                raise Slide_Forge_Error(f"Unexpected error during conversion: {e}")

    def convert_string(self, content: str, output_file: str, source_format: str, **kwargs) -> bool:
        """
        Convert content from string to output file.

        Args:
            content: Source content as string
            output_file: Path to output file
            source_format: Format of the source content ('latex', 'pptx', etc.)
            **kwargs: Additional conversion options

        Returns:
            True if conversion successful, False otherwise
        """
        try:
            output_path = Path(output_file)

            # Create conversion options
            options = Conversion_Options(**{**self.default_options.to_dict(), **kwargs})

            if options.verbose:
                self.logger.info(f"Converting {source_format} string to {output_path}")

            # Detect target format
            target_format = kwargs.get('target_format') or self.format_detector.detect_format(output_path)

            if not target_format:
                raise BuilderError(f"Cannot detect target format for: {output_path}")

            # Validate parser and builder
            if source_format not in self.parsers:
                raise ParseError(f"No parser available for format: {source_format}")
            if target_format not in self.builders:
                raise BuilderError(f"No builder available for format: {target_format}")

            # Parse content
            parser = self.parsers[source_format]
            document = parser.parse_string(content, **options.custom_settings)
            document.source_format = source_format

            # Map and build
            if self.mapper and self.mapper.can_convert(source_format, target_format):
                slide_structures = self.mapper.map_document(document, target_format, **options.custom_settings)
            else:
                slide_structures = self._document_to_slides(document)

            builder = self.builders[target_format]

            # Pass source path for image resolution (empty for string conversion)
            build_options = {**options.custom_settings, 'source_path': ''}
            return builder.build_presentation(slide_structures, output_path, **build_options)

        except Exception as e:
            self.logger.error(f"String conversion failed: {e}")
            if isinstance(e, Slide_Forge_Error):
                raise
            else:
                raise Slide_Forge_Error(f"Unexpected error during string conversion: {e}")

    def _document_to_slides(self, document: Universal_Document) -> List[Any]:
        """
        Convert Universal_Document to slide structures (placeholder implementation).

        This method should be implemented by specific mappers or builders.
        """
        # For now, return empty list - this will be implemented by mappers
        return []

    def get_supported_formats(self) -> Dict[str, List[str]]:
        """
        Get information about supported input/output formats.

        Returns:
            Dictionary with 'input' and 'output' format lists
        """
        return {
            'input': list(self.parsers.keys()),
            'output': list(self.builders.keys())
        }

    def get_supported_conversions(self) -> List[tuple]:
        """
        Get list of supported conversion pairs.

        Returns:
            List of (source_format, target_format) tuples
        """
        conversions = []
        if self.mapper:
            supported = self.mapper.get_supported_conversions()
            for source, targets in supported.items():
                for target in targets:
                    if source in self.parsers and target in self.builders:
                        conversions.append((source, target))
        return conversions

    def set_default_options(self, **kwargs):
        """
        Set default conversion options.

        Args:
            **kwargs: Default options to set
        """
        for key, value in kwargs.items():
            if hasattr(self.default_options, key):
                setattr(self.default_options, key, value)
            elif key == 'custom_settings':
                # Handle custom_settings specially
                self.default_options.custom_settings.update(value)
            else:
                self.logger.warning(f"Unknown default option: {key}")
