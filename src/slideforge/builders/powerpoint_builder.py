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

"""PowerPoint builder implementation using python-pptx."""

from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

from pptx import Presentation
from pptx.util import Inches
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

from ..base import Base_Builder
from ..models.universal import Universal_Frame, Universal_Element, Element_Type, Layout_Type
from ..exceptions import BuilderError


class PowerPoint_Builder(Base_Builder):
    """Builder for PowerPoint presentations using python-pptx."""

    def __init__(self):
        """Initialize PowerPoint builder."""
        self.supported_themes = ['default', 'professional', 'academic', 'minimal']
        self.default_theme = 'default'
        self.logger = logging.getLogger(__name__)

        # Theme configurations
        self.theme_configs = {
            'default': {
                'slide_width': Inches(10),
                'slide_height': Inches(7.5),
                'title_font_size': 44,
                'content_font_size': 18,
                'title_color': RGBColor(0, 0, 0),
                'content_color': RGBColor(0, 0, 0),
                'background_color': RGBColor(255, 255, 255)
            },
            'professional': {
                'slide_width': Inches(10),
                'slide_height': Inches(7.5),
                'title_font_size': 40,
                'content_font_size': 16,
                'title_color': RGBColor(0, 32, 96),
                'content_color': RGBColor(32, 32, 32),
                'background_color': RGBColor(255, 255, 255)
            },
            'academic': {
                'slide_width': Inches(10),
                'slide_height': Inches(7.5),
                'title_font_size': 42,
                'content_font_size': 17,
                'title_color': RGBColor(0, 0, 128),
                'content_color': RGBColor(0, 0, 0),
                'background_color': RGBColor(255, 255, 255)
            },
            'minimal': {
                'slide_width': Inches(10),
                'slide_height': Inches(7.5),
                'title_font_size': 36,
                'content_font_size': 14,
                'title_color': RGBColor(64, 64, 64),
                'content_color': RGBColor(64, 64, 64),
                'background_color': RGBColor(255, 255, 255)
            }
        }

    def build_presentation(self, slides: List[Universal_Frame],
                          output_file: Path, **kwargs) -> bool:
        """
        Build a PowerPoint presentation from slide structures.

        Args:
            slides: List of Universal_Frame objects
            output_file: Path to output .pptx file
            **kwargs: Additional build options
                - theme: PowerPoint theme
                - preserve_colors: Preserve colors from source
                - include_images: Include images from source
                - verbose: Enable verbose output

        Returns:
            True if build successful, False otherwise

        Raises:
            BuilderError: If build fails
        """
        try:
            # Get options
            theme = kwargs.get('theme', self.default_theme)
            preserve_colors = kwargs.get('preserve_colors', True)
            include_images = kwargs.get('include_images', True)
            verbose = kwargs.get('verbose', False)

            if verbose:
                self.logger.info(f"Building PowerPoint presentation with theme: {theme}")
                self.logger.info(f"Output file: {output_file}")
                self.logger.info(f"Number of slides: {len(slides)}")

            # Validate theme
            if theme not in self.supported_themes:
                raise BuilderError(f"Unsupported theme: {theme}",
                               operation="build_presentation", output_format="pptx")

            # Get theme configuration
            config = self.theme_configs[theme]

            # Create presentation
            prs = Presentation()

            # Set slide dimensions
            prs.slide_width = config['slide_width']
            prs.slide_height = config['slide_height']

            # Build each slide
            for i, slide in enumerate(slides, 1):
                if verbose:
                    self.logger.info(f"Building slide {i}: {slide.title or 'No title'}")

                slide_layout = self._determine_layout(slide, prs)
                slide_obj = prs.slides.add_slide(slide_layout)

                # Add title if present
                if slide.title:
                    title_shape = slide_obj.shapes.title
                    title_shape.text = slide.title
                    if preserve_colors:
                        title_shape.text_frame.paragraphs[0].font.color.rgb = config['title_color']
                    title_shape.text_frame.paragraphs[0].font.size = config['title_font_size']

                # Add elements
                self._add_elements_to_slide(slide_obj, slide.elements, config, preserve_colors, include_images)

            # Ensure output directory exists
            output_file.parent.mkdir(parents=True, exist_ok=True)

            # Save presentation
            prs.save(output_file)

            if verbose:
                self.logger.info(f"Successfully built PowerPoint presentation: {output_file}")

            return True

        except Exception as e:
            raise BuilderError(f"Failed to build PowerPoint presentation: {e}",
                           operation="build_presentation", output_format="pptx")

    def get_supported_extensions(self) -> List[str]:
        """Get supported output extensions."""
        return ['.pptx']

    def get_default_theme(self) -> str:
        """Get default theme."""
        return self.default_theme

    def _determine_layout(self, slide: Universal_Frame, presentation):
        """Determine the appropriate slide layout for the frame."""
        if slide.layout == Layout_Type.TITLE_SLIDE:
            return presentation.slide_layouts[0]  # Title Slide
        elif slide.layout == Layout_Type.TITLE_AND_CONTENT:
            return presentation.slide_layouts[1]  # Title and Content
        elif slide.layout == Layout_Type.TWO_COLUMN:
            return presentation.slide_layouts[3]  # Two Content
        else:
            return presentation.slide_layouts[1]  # Title and Content (default)

    def _add_elements_to_slide(self, slide_obj, elements: List[Universal_Element],
                              config: Dict[str, Any], preserve_colors: bool, include_images: bool):
        """Add elements to a PowerPoint slide."""
        for element in elements:
            try:
                if element.element_type == Element_Type.TEXT:
                    self._add_text_element(slide_obj, element, config, preserve_colors)
                elif element.element_type == Element_Type.TITLE:
                    self._add_title_element(slide_obj, element, config, preserve_colors)
                elif element.element_type == Element_Type.ITEMIZE:
                    self._add_itemize_element(slide_obj, element, config, preserve_colors)
                elif element.element_type == Element_Type.IMAGE and include_images:
                    self._add_image_element(slide_obj, element, config)
                elif element.element_type == Element_Type.BLOCK:
                    self._add_block_element(slide_obj, element, config, preserve_colors)
                # Add more element types as needed
            except Exception as e:
                self.logger.warning(f"Failed to add element {element.element_type}: {e}")

    def _add_text_element(self, slide_obj, element: Universal_Element,
                          config: Dict[str, Any], preserve_colors: bool):
        """Add a text element to the slide."""
        content = element.content
        if isinstance(content, str):
            text = content
        else:
            text = content.text

        # Add text as a text box
        left = Inches(1) if element.position else Inches(1)
        top = Inches(2) if element.position else Inches(2)
        width = Inches(8) if element.size else Inches(8)
        height = Inches(1) if element.size else Inches(1)

        text_box = slide_obj.shapes.add_textbox(left, top, width, height)
        text_frame = text_box.text_frame
        p = text_frame.paragraphs[0]
        p.text = text
        p.font.size = config['content_font_size']

        if preserve_colors:
            p.font.color.rgb = config['content_color']

    def _add_title_element(self, slide_obj, element: Universal_Element,
                           config: Dict[str, Any], preserve_colors: bool):
        """Add a title element to the slide."""
        content = element.content
        if isinstance(content, str):
            text = content
        else:
            text = content.text

        # Add to existing title shape if available, otherwise create new one
        if slide_obj.shapes.title:
            title_shape = slide_obj.shapes.title
            title_shape.text = text
            if preserve_colors:
                title_shape.text_frame.paragraphs[0].font.color.rgb = config['title_color']
                title_shape.text_frame.paragraphs[0].font.size = config['title_font_size']
        else:
            # Create new title text box
            left = Inches(1) if element.position else Inches(1)
            top = Inches(0.5) if element.position else Inches(0.5)
            width = Inches(8) if element.size else Inches(8)
            height = Inches(1) if element.size else Inches(1)

            title_box = slide_obj.shapes.add_textbox(left, top, width, height)
            title_frame = title_box.text_frame
            p = title_frame.paragraphs[0]
            p.text = text
            p.font.size = config['title_font_size']
            p.font.bold = True

            if preserve_colors:
                p.font.color.rgb = config['title_color']

    def _add_itemize_element(self, slide_obj, element: Universal_Element,
                           config: Dict[str, Any], preserve_colors: bool):
        """Add a bullet list element to the slide."""
        content = element.content
        if isinstance(content, dict) and 'items' in content:
            items = content['items']
        else:
            # Try to parse as string
            items = [str(content)]

        left = Inches(1) if element.position else Inches(1)
        top = Inches(2) if element.position else Inches(2)
        width = Inches(8) if element.size else Inches(8)

        text_box = slide_obj.shapes.add_textbox(left, top, width, Inches(len(items) * 0.5))
        text_frame = text_box.text_frame

        for i, item in enumerate(items):
            if i > 0:
                p = text_frame.add_paragraph()
            else:
                p = text_frame.paragraphs[0]

            p.text = f"• {item}"
            p.level = element.level
            p.font.size = config['content_font_size']

            if preserve_colors:
                p.font.color.rgb = config['content_color']

    def _add_image_element(self, slide_obj, element: Universal_Element,
                          config: Dict[str, Any]):
        """Add an image element to the slide."""
        content = element.content
        if isinstance(content, dict) and 'path' in content:
            image_path = content['path']
        else:
            image_path = str(content)

        try:
            # Convert relative paths to absolute
            if not Path(image_path).is_absolute():
                # Assume relative to current working directory
                image_path = Path.cwd() / image_path

            if Path(image_path).exists():
                left = Inches(1) if element.position else Inches(1)
                top = Inches(2) if element.position else Inches(2)
                width = Inches(6) if element.size else Inches(6)
                height = Inches(4) if element.size else None

                slide_obj.shapes.add_picture(image_path, left, top, width, height)
            else:
                self.logger.warning(f"Image file not found: {image_path}")
        except Exception as e:
            self.logger.warning(f"Failed to add image {image_path}: {e}")

    def _add_block_element(self, slide_obj, element: Universal_Element,
                          config: Dict[str, Any], preserve_colors: bool):
        """Add a block/quote element to the slide."""
        content = element.content
        if isinstance(content, str):
            text = content
        else:
            text = str(content)

        left = Inches(1) if element.position else Inches(1)
        top = Inches(2) if element.position else Inches(2)
        width = Inches(8) if element.size else Inches(8)
        height = Inches(1) if element.size else Inches(1)

        text_box = slide_obj.shapes.add_textbox(left, top, width, height)
        text_frame = text_box.text_frame
        p = text_frame.paragraphs[0]
        p.text = text
        p.font.size = config['content_font_size']
        p.font.italic = True

        if preserve_colors:
            p.font.color.rgb = config['content_color']
