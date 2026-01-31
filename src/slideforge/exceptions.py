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

"""Custom exceptions for Slide Forge."""


class Slide_Forge_Error(Exception):
    """Base exception for all Slide Forge errors."""
    
    def __init__(self, message: str, details: dict = None):
        """
        Initialize Slide Forge error.
        
        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}
    
    def __str__(self) -> str:
        """String representation of the error."""
        if self.details:
            return f"{self.message} (Details: {self.details})"
        return self.message


class ParseError(Slide_Forge_Error):
    """Error raised during parsing of input files."""
    
    def __init__(self, message: str, line_number: int = None, 
                 file_path: str = None, latex_snippet: str = None):
        """
        Initialize parsing error.
        
        Args:
            message: Error message
            line_number: Line number where error occurred
            file_path: Path to file being parsed
            latex_snippet: LaTeX code snippet where error occurred
        """
        details = {}
        if line_number is not None:
            details['line_number'] = line_number
        if file_path:
            details['file_path'] = file_path
        if latex_snippet:
            details['latex_snippet'] = latex_snippet
        
        super().__init__(message, details)
        self.line_number = line_number
        self.file_path = file_path
        self.latex_snippet = latex_snippet


class MappingError(Slide_Forge_Error):
    """Error raised during content mapping between formats."""
    
    def __init__(self, message: str, element_type: str = None, 
                 source_format: str = None, target_format: str = None):
        """
        Initialize mapping error.
        
        Args:
            message: Error message
            element_type: Type of element that failed to map
            source_format: Source format
            target_format: Target format
        """
        details = {}
        if element_type:
            details['element_type'] = element_type
        if source_format:
            details['source_format'] = source_format
        if target_format:
            details['target_format'] = target_format
        
        super().__init__(message, details)
        self.element_type = element_type
        self.source_format = source_format
        self.target_format = target_format


class BuilderError(Slide_Forge_Error):
    """Error raised during building of output files."""
    
    def __init__(self, message: str, slide_number: int = None, 
                 operation: str = None, output_format: str = None):
        """
        Initialize builder error.
        
        Args:
            message: Error message
            slide_number: Slide number where error occurred
            operation: Operation that failed
            output_format: Output format being built
        """
        details = {}
        if slide_number is not None:
            details['slide_number'] = slide_number
        if operation:
            details['operation'] = operation
        if output_format:
            details['output_format'] = output_format
        
        super().__init__(message, details)
        self.slide_number = slide_number
        self.operation = operation
        self.output_format = output_format


class ValidationError(Slide_Forge_Error):
    """Error raised during validation of inputs or outputs."""
    
    def __init__(self, message: str, field: str = None, value: str = None):
        """
        Initialize validation error.
        
        Args:
            message: Error message
            field: Field that failed validation
            value: Value that failed validation
        """
        details = {}
        if field:
            details['field'] = field
        if value:
            details['value'] = value
        
        super().__init__(message, details)
        self.field = field
        self.value = value


class ConfigurationError(Slide_Forge_Error):
    """Error raised due to configuration issues."""
    
    def __init__(self, message: str, config_key: str = None, config_value: str = None):
        """
        Initialize configuration error.
        
        Args:
            message: Error message
            config_key: Configuration key that caused the error
            config_value: Configuration value that caused the error
        """
        details = {}
        if config_key:
            details['config_key'] = config_key
        if config_value:
            details['config_value'] = config_value
        
        super().__init__(message, details)
        self.config_key = config_key
        self.config_value = config_value


class UnsupportedFormatError(Slide_Forge_Error):
    """Error raised when trying to use an unsupported format."""
    
    def __init__(self, message: str, format_name: str = None, 
                 operation: str = None):
        """
        Initialize unsupported format error.
        
        Args:
            message: Error message
            format_name: Name of unsupported format
            operation: Operation being attempted
        """
        details = {}
        if format_name:
            details['format_name'] = format_name
        if operation:
            details['operation'] = operation
        
        super().__init__(message, details)
        self.format_name = format_name
        self.operation = operation


class ConversionError(Slide_Forge_Error):
    """Error raised during the conversion process."""
    
    def __init__(self, message: str, source_file: str = None, 
                 target_file: str = None, stage: str = None):
        """
        Initialize conversion error.
        
        Args:
            message: Error message
            source_file: Source file path
            target_file: Target file path
            stage: Stage where conversion failed
        """
        details = {}
        if source_file:
            details['source_file'] = source_file
        if target_file:
            details['target_file'] = target_file
        if stage:
            details['stage'] = stage
        
        super().__init__(message, details)
        self.source_file = source_file
        self.target_file = target_file
        self.stage = stage
