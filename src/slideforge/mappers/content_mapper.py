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

"""Content mapper for converting between presentation formats."""

from typing import List, Dict, Any

from ..base import Base_Mapper
from ..models.universal import Universal_Document, Universal_Frame
from ..exceptions import MappingError


class Content_Mapper(Base_Mapper):
    """Content mapper for bidirectional format conversions."""
    
    def __init__(self):
        """Initialize content mapper."""
        self.supported_conversions = {
            'latex': ['pptx'],
            'pptx': ['latex']  # Future support
        }
    
    def map_document(self, document: Universal_Document, target_format: str, 
                   **kwargs) -> List[Any]:
        """
        Map a Universal_Document to slide structures for target format.
        
        Args:
            document: Source Universal_Document
            target_format: Target format ('pptx', 'latex', etc.)
            **kwargs: Additional mapping options
            
        Returns:
            List of slide structures appropriate for target format
        """
        if target_format == 'pptx':
            return self._map_to_powerpoint(document, **kwargs)
        elif target_format == 'latex':
            return self._map_to_latex(document, **kwargs)
        else:
            raise MappingError(f"Unsupported target format: {target_format}", 
                           target_format=target_format)
    
    def get_supported_conversions(self) -> Dict[str, List[str]]:
        """Get supported conversion mappings."""
        return self.supported_conversions
    
    def _map_to_powerpoint(self, document: Universal_Document, **kwargs) -> List[Any]:
        """
        Map Universal_Document to PowerPoint slide structures.
        
        Args:
            document: Source document
            **kwargs: Additional options
            
        Returns:
            List of slide structures for PowerPoint builder
        """
        # For now, return the frames directly
        # In a full implementation, this would convert Universal_Frame
        # to PowerPoint-specific slide structures
        return document.frames
    
    def _map_to_latex(self, document: Universal_Document, **kwargs) -> List[Any]:
        """
        Map Universal_Document to LaTeX slide structures.
        
        Args:
            document: Source document
            **kwargs: Additional options
            
        Returns:
            List of slide structures for LaTeX builder
        """
        # Future implementation for PPTX to LaTeX conversion
        raise MappingError("PowerPoint to LaTeX conversion not yet implemented",
                           source_format="pptx", target_format="latex")
