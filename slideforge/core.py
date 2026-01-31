"""
Slide Forge Core API
Main interface for LaTeX to PowerPoint conversion
"""

from .parser import LaTeXParser
from .mapper import ContentMapper
from .builder import PowerPointBuilder

class SlideForge:
    """Main Slide Forge API for converting LaTeX to PowerPoint"""
    
    def __init__(self):
        self.parser = LaTeXParser()
        self.mapper = ContentMapper()
        self.builder = PowerPointBuilder()
    
    def convert_file(self, latex_file: str, output_file: str, **kwargs):
        """
        Convert LaTeX Beamer file to PowerPoint presentation
        
        Args:
            latex_file: Path to input .tex file
            output_file: Path to output .pptx file
            **kwargs: Additional options for conversion
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Parse LaTeX into structured data
            document = self.parser.parse_file(latex_file)
            
            # Map LaTeX elements to PowerPoint structure
            slides = self.mapper.map_document(document)
            
            # Build PowerPoint presentation
            self.builder.build_presentation(slides)
            
            # Save presentation
            self.builder.save(output_file)
            
            return True
            
        except Exception as e:
            print(f"Conversion failed: {e}")
            return False
    
    def convert_string(self, latex_content: str, output_file: str, **kwargs):
        """
        Convert LaTeX string content to PowerPoint presentation
        
        Args:
            latex_content: LaTeX source code as string
            output_file: Path to output .pptx file
            **kwargs: Additional options for conversion
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Parse LaTeX string into structured data
            document = self.parser.parse_string(latex_content)
            
            # Map LaTeX elements to PowerPoint structure
            slides = self.mapper.map_document(document)
            
            # Build PowerPoint presentation
            self.builder.build_presentation(slides)
            
            # Save presentation
            self.builder.save(output_file)
            
            return True
            
        except Exception as e:
            print(f"Conversion failed: {e}")
            return False
