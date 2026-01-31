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

"""Tests for Slide Forge core functionality."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from slideforge.core import Slide_Forge
from slideforge.models.universal import (
    Universal_Document, Universal_Frame, Universal_Element,
    Element_Type, Layout_Type
)


class TestSlideForge:
    """Test cases for Slide Forge core controller."""

    @pytest.fixture
    def slide_forge(self):
        """Create Slide_Forge instance."""

        # Create instance without auto-registration for testing
        slide_forge = Slide_Forge()

        # Clear auto-registered components for clean test
        slide_forge.parsers = {}
        slide_forge.builders = {}

        # Keep mapper as it's expected to be initialized
        return slide_forge

    @pytest.fixture
    def sample_latex_file(self, tmp_path):
        """Create sample LaTeX file."""
        latex_content = r"""
\documentclass{beamer}
\title{Test Presentation}
\author{Test Author}

\begin{document}

\begin{frame}{Test Frame}
    This is a test slide with some content.

    \begin{itemize}
        \item First bullet point
        \item Second bullet point
    \end{itemize}
\end{frame}

\end{document}
"""

        tex_file = tmp_path / "test.tex"
        tex_file.write_text(latex_content)
        return tex_file

    @pytest.fixture
    def output_file(self, tmp_path):
        """Create temporary output file path."""
        return tmp_path / "test_output.pptx"

    def test_initialization(self, slide_forge):
        """Test Slide_Forge initialization."""
        assert slide_forge is not None
        assert slide_forge.format_detector is not None
        assert slide_forge.parsers == {}
        assert slide_forge.builders == {}
        assert slide_forge.mapper is not None
        assert slide_forge.default_options is not None

    def test_initialize_components(self, slide_forge):
        """Test component initialization."""
        slide_forge._initialize_components()

        # Should have registered components
        assert len(slide_forge.parsers) > 0
        assert len(slide_forge.builders) > 0

        # Check that specific components were registered
        assert 'latex' in slide_forge.parsers
        assert 'pptx' in slide_forge.builders

    def test_register_parser(self, slide_forge):
        """Test parser registration."""
        mock_parser = Mock()

        slide_forge.register_parser('test', mock_parser)

        assert 'test' in slide_forge.parsers
        assert slide_forge.parsers['test'] == mock_parser

    def test_register_builder(self, slide_forge):
        """Test builder registration."""
        mock_builder = Mock()

        slide_forge.register_builder('test', mock_builder)

        assert 'test' in slide_forge.builders
        assert slide_forge.builders['test'] == mock_builder

    def test_register_mapper(self, slide_forge):
        """Test mapper registration."""
        mock_mapper = Mock()

        slide_forge.register_mapper(mock_mapper)

        assert slide_forge.mapper == mock_mapper

    def test_get_supported_formats(self, slide_forge):
        """Test getting supported formats."""
        formats = slide_forge.get_supported_formats()

        assert 'input' in formats
        assert 'output' in formats
        assert 'latex' in formats['input']
        assert 'pptx' in formats['output']

    def test_get_supported_conversions(self, slide_forge):
        """Test getting supported conversions."""
        conversions = slide_forge.get_supported_conversions()

        assert isinstance(conversions, list)
        # Should have latex to pptx conversion
        assert any(source == 'latex' and 'pptx' in targets for source, targets in conversions)

    def test_convert_file_success(self, slide_forge, sample_latex_file, output_file):
        """Test successful file conversion."""
        success = slide_forge.convert_file(
            str(sample_latex_file),
            str(output_file),
            verbose=False
        )

        assert success
        assert output_file.exists()

    def test_convert_string_success(self, slide_forge, output_file):
        """Test successful string conversion."""
        latex_content = r"""
\begin{frame}{Test Frame}
    Test content
\end{frame}
"""

        success = slide_forge.convert_string(
            latex_content,
            str(output_file),
            'latex',
            verbose=False
        )

        assert success
        assert output_file.exists()

    def test_convert_file_missing_parser(self, slide_forge, output_file):
        """Test conversion with missing parser."""
        # Create a file with unsupported extension
        unsupported_file = Path("test.unsupported")
        unsupported_file.write_text("content")

        try:
            slide_forge.convert_file(str(unsupported_file), str(output_file))
            assert False, "Should have failed with missing parser"
        except Exception:
            pass  # Expected to fail
        finally:
            unsupported_file.unlink(missing_ok=True)

    def test_convert_file_missing_builder(self, slide_forge, sample_latex_file, tmp_path):
        """Test conversion with missing builder."""
        unsupported_output = tmp_path / "test.unsupported"

        try:
            slide_forge.convert_file(
                str(sample_latex_file),
                str(unsupported_output),
                target_format='unsupported'
            )
            assert False, "Should have failed with missing builder"
        except Exception:
            pass  # Expected to fail
        finally:
            unsupported_output.unlink(missing_ok=True)

    def test_set_default_options(self, slide_forge):
        """Test setting default options."""
        slide_forge.set_default_options(
            preserve_colors=False,
            verbose=True,
            theme="professional"
        )

        assert slide_forge.default_options.preserve_colors is False
        assert slide_forge.default_options.verbose is True
        assert slide_forge.default_options.theme == 'professional'

    def test_set_default_options_invalid_option(self, slide_forge):
        """Test setting invalid default option."""
        # Should not raise error, just log warning
        slide_forge.set_default_options(invalid_option="test")

        # Invalid option should not be set
        assert not hasattr(slide_forge.default_options, 'invalid_option')

    def test_convert_file_with_options(self, slide_forge, sample_latex_file, output_file):
        """Test conversion with custom options."""
        success = slide_forge.convert_file(
            str(sample_latex_file),
            str(output_file),
            theme="professional",
            preserve_colors=False,
            verbose=True
        )

        assert success
        assert output_file.exists()

    def test_convert_string_with_options(self, slide_forge, output_file):
        """Test string conversion with custom options."""
        latex_content = r"""
\begin{frame}{Test Frame}
    Test content
\end{frame}
"""

        success = slide_forge.convert_string(
            latex_content,
            str(output_file),
            'latex',
            theme="academic",
            preserve_colors=True,
            verbose=True
        )

        assert success
        assert output_file.exists()

    def test_convert_file_no_source_format(self, slide_forge, sample_latex_file, output_file):
        """Test conversion without specifying source format."""
        success = slide_forge.convert_file(
            str(sample_latex_file),
            str(output_file),
            verbose=False
        )

        assert success
        assert output_file.exists()

    def test_convert_string_no_target_format(self, slide_forge, output_file):
        """Test string conversion without specifying target format."""
        latex_content = r"""
\begin{frame}{Test Frame}
    Test content
\end{frame}
"""

        success = slide_forge.convert_string(
            latex_content,
            str(output_file),
            'latex',
            verbose=False
        )

        assert success
        assert output_file.exists()

    @patch('slideforge.core.Slide_Forge._initialize_components')
    def test_no_components_available(self, mock_init, slide_forge, sample_latex_file, output_file):
        """Test conversion when no components are available."""
        # Mock initialization to have no components
        slide_forge.parsers = {}
        slide_forge.builders = {}
        slide_forge.mapper = None

        try:
            slide_forge.convert_file(str(sample_latex_file), str(output_file))
            assert False, "Should have failed with no components"
        except Exception:
            pass  # Expected to fail

    def test_document_to_slides_no_mapper(self, slide_forge):
        """Test _document_to_slides when no mapper is available."""
        doc = Universal_Document()
        frame = Universal_Frame(frame_number=1, title="Test")
        doc.add_frame(frame)

        slide_forge.mapper = None
        slides = slide_forge._document_to_slides(doc)

        assert slides == []  # Should return empty list

    def test_error_handling(self, slide_forge):
        """Test error handling in conversion."""
        # Test with invalid LaTeX content
        invalid_latex = r"""
\begin{frame}{Invalid Frame
    Missing closing brace
\end{document}
"""

        try:
            slide_forge.convert_string(invalid_latex, "test.pptx", "latex")
            assert False, "Should have failed with invalid LaTeX"
        except Exception:
            pass  # Expected to fail

    def test_verbose_logging(self, slide_forge, sample_latex_file, output_file, caplog):
        """Test verbose logging during conversion."""
        import logging

        with caplog.at_level(logging.INFO):
            success = slide_forge.convert_file(
                str(sample_latex_file),
                str(output_file),
                verbose=True
            )

            # Should have logged conversion start and success messages
            assert any("Starting conversion" in record.message for record in caplog.records)
            assert any("Successfully built" in record.message for record in caplog.records)

    def test_custom_settings_passed_through(self, slide_forge, sample_latex_file, output_file):
        """Test that custom settings are passed through correctly."""
        # Register mock components for testing
        from unittest.mock import Mock
        mock_parser = Mock()
        mock_document = Mock()
        mock_document.get_total_frames.return_value = 1
        mock_document.source_format = 'latex'
        mock_document.source_path = sample_latex_file
        mock_parser.parse_file.return_value = mock_document

        slide_forge.parsers['latex'] = mock_parser
        slide_forge.builders['pptx'] = Mock()

        # Configure mapper to avoid iteration issues
        slide_forge.mapper = Mock()
        slide_forge.mapper.can_convert.return_value = True
        slide_forge.mapper.map_document.return_value = []

        custom_settings = {"custom_option": "custom_value"}

        with patch.object(slide_forge.builders['pptx'], 'build_presentation') as mock_build:
            slide_forge.convert_file(
                str(sample_latex_file),
                str(output_file),
                custom_settings=custom_settings
            )

            # Check that custom settings were passed (merged with source_path)
            mock_build.assert_called_once()
            call_args = mock_build.call_args
            build_options = call_args[1]
            assert 'custom_option' in build_options
            assert build_options['custom_option'] == 'custom_value'
            assert 'source_path' in build_options

    def test_source_path_passed_to_builder(self, slide_forge, sample_latex_file, output_file):
        """Test that source path is passed to builder."""
        # Register mock components for testing
        from unittest.mock import Mock
        mock_parser = Mock()
        mock_document = Mock()
        mock_document.get_total_frames.return_value = 1
        mock_document.source_format = 'latex'
        mock_document.source_path = sample_latex_file
        mock_parser.parse_file.return_value = mock_document

        slide_forge.parsers['latex'] = mock_parser
        slide_forge.builders['pptx'] = Mock()
        # Configure mapper to avoid iteration issues
        slide_forge.mapper = Mock()
        slide_forge.mapper.can_convert.return_value = True
        slide_forge.mapper.map_document.return_value = []

        with patch.object(slide_forge.builders['pptx'], 'build_presentation') as mock_build:
            slide_forge.convert_file(
                str(sample_latex_file),
                str(output_file)
            )

            # Check that source_path was added to build options
            call_args = mock_build.call_args
            assert 'source_path' in call_args[1]
            assert call_args[1]['source_path'] == str(sample_latex_file)
