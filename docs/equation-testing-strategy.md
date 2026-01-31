# Equation Testing Strategy

## Testing Approach for LaTeX Equations

## 1. Data Structure Tests
Test that equations are correctly parsed and classified:

```python
def test_equation_parsing(self, parser, fixtures_dir):
    """Test that equations are extracted as equation elements."""
    tex_content = r"""
    \begin{frame}{Math Frame}
        Inline equation: $E = mc^2$
        
        Display equation:
        \begin{equation}
            \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
        \end{equation}
    \end{frame}
    """
    
    document = parser.parse_string(tex_content, 'test.tex')
    frame = document.frames[0]
    
    # Should have 2 equation elements
    equation_elements = [e for e in frame.elements if e.element_type == Element_Type.EQUATION]
    assert len(equation_elements) == 2
    
    # Check inline equation
    inline_eq = equation_elements[0]
    assert inline_eq.content['latex'] == 'E = mc^2'
    assert inline_eq.content['type'] == 'inline'
    
    # Check display equation
    display_eq = equation_elements[1]
    assert '\\int' in display_eq.content['latex']
    assert display_eq.content['type'] == 'display'
```

## 2. Rendering Tests
Test that LaTeX equations render to images correctly:

```python
def test_equation_rendering(self, builder):
    """Test that equations render to images without errors."""
    equation_element = Universal_Element(
        element_type=Element_Type.EQUATION,
        content={
            'latex': r'\sum_{i=1}^{n} i = \frac{n(n+1)}{2}',
            'type': 'display'
        }
    )
    
    # Should render without throwing exceptions
    image_path = builder._render_latex_to_image(
        equation_element.content['latex'], 
        '/test/path'
    )
    
    assert image_path.exists()
    assert image_path.suffix in ['.png', '.svg']
```

## 3. Visual Regression Tests
Compare rendered equations against known-good images:

```python
def test_equation_visual_regression(self, builder, fixtures_dir):
    """Test that equation rendering matches expected output."""
    test_equations = [
        r'E = mc^2',
        r'\int_{0}^{\infty} e^{-x} dx = 1',
        r'\sum_{i=1}^{n} i = \frac{n(n+1)}{2}',
        r'\alpha + \beta = \gamma'
    ]
    
    for latex_eq in test_equations:
        # Render test equation
        test_image = builder._render_latex_to_image(latex_eq, '/test')
        
        # Load expected image
        expected_image = fixtures_dir / 'expected_equations' / f'{hash(latex_eq)}.png'
        
        # Compare images (allowing for small differences)
        if expected_image.exists():
            similarity = compare_images(test_image, expected_image)
            assert similarity > 0.95, f"Equation rendering differs for: {latex_eq}"
```

## 4. Integration Tests
Test full pipeline from LaTeX to PowerPoint:

```python
def test_equation_integration(self, converter):
    """Test full LaTeX to PowerPoint conversion with equations."""
    tex_content = r"""
    \documentclass{beamer}
    \begin{document}
    \begin{frame}{Equations}
        Einstein's famous equation: $E = mc^2$
        
        And the Gaussian integral:
        \begin{equation}
            \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
        \end{equation}
    \end{frame}
    \end{document}
    """
    
    # Convert to PowerPoint
    pptx_path = converter.convert_string(tex_content, 'test.pptx', 'latex')
    
    # Verify PowerPoint was created
    assert pptx_path.exists()
    
    # Verify it contains equation images
    from pptx import Presentation
    prs = Presentation(pptx_path)
    
    equation_images = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.shape_type == 13:  # Picture
                equation_images.append(shape)
    
    assert len(equation_images) >= 2, "Should have at least 2 equation images"
```

## 5. Performance Tests
Test equation rendering performance:

```python
def test_equation_rendering_performance(self, builder):
    """Test that equation rendering is reasonably fast."""
    import time
    
    complex_equations = [
        r'\int_{0}^{\infty} x^n e^{-x} dx = n!',
        r'\sum_{k=0}^{\infty} \frac{x^k}{k!} = e^x',
        r'\prod_{i=1}^{n} \left(1 + \frac{1}{i}\right) = n+1'
    ]
    
    start_time = time.time()
    
    for eq in complex_equations:
        builder._render_latex_to_image(eq, '/test')
    
    end_time = time.time()
    
    # Should render all equations in under 10 seconds
    assert end_time - start_time < 10.0, "Equation rendering too slow"
```

## Equation Rendering Tools

### Option 1: LaTeX + dvipng (Recommended)
```python
import subprocess
import tempfile
from pathlib import Path

def render_latex_to_image(latex_content: str, output_dir: Path) -> Path:
    """Render LaTeX equation to PNG using dvipng."""
    
    # Create temporary LaTeX document
    tex_doc = f"""
    \\documentclass[preview]{{standalone}}
    \\usepackage{{amsmath}}
    \\begin{{document}}
    \\[{latex_content}\\]
    \\end{{document}}
    """
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
        f.write(tex_doc)
        tex_path = Path(f.name)
    
    try:
        # Compile LaTeX to DVI
        subprocess.run(['latex', '-output-directory=' + str(output_dir), str(tex_path)], 
                      check=True, capture_output=True)
        
        # Convert DVI to PNG
        dvi_path = output_dir / tex_path.stem
        png_path = output_dir / f"{tex_path.stem}.png"
        
        subprocess.run(['dvipng', '-T', 'tight', '-D', '120', str(dvi_path), str(png_path)], 
                      check=True, capture_output=True)
        
        return png_path
    finally:
        # Cleanup temporary files
        tex_path.unlink(missing_ok=True)
        (output_dir / f"{tex_path.stem}.dvi").unlink(missing_ok=True)
        (output_dir / f"{tex_path.stem}.log").unlink(missing_ok=True)
```

### Option 2: MathJax + Node.js
```python
def render_mathjax_to_image(latex_content: str, output_path: Path):
    """Render LaTeX using MathJax and Node.js."""
    
    js_code = f"""
    const mathjax = require('mathjax-full/js/mathjax.js');
    const adapt = require('mathjax-full/js/adaptors/documentAdaptor.js').documentAdaptor;
    const tex2mml = require('mathjax-full/js/input/tex.js').tex2mml;
    const mml2svg = require('mathjax-full/js/output/svg.js').mml2svg;
    
    const math = '{latex_content}';
    const html = mathjax.document('', {}, {{
        input: tex2mml,
        output: mml2svg
    }}, math);
    
    console.log(html);
    """
    
    # Use Node.js to render
    result = subprocess.run(['node', '-e', js_code], capture_output=True, text=True)
    svg_content = result.stdout
    
    # Save SVG
    with open(output_path, 'w') as f:
        f.write(svg_content)
```

## Test Fixtures

### Sample LaTeX Files with Equations
```latex
% tests/fixtures/latex/equations/simple_equations.tex
\begin{frame}{Simple Equations}
    Inline math: $x^2 + y^2 = z^2$
    
    Display equation:
    \begin{equation}
        f(x) = \int_{-\infty}^{\infty} \hat{f}(\xi) e^{2\pi i \xi x} d\xi
    \end{equation}
\end{frame}
```

### Expected JSON Structure
```json
{
  "frames": [{
    "elements": [
      {
        "element_type": "text",
        "content": "Inline math: x^2 + y^2 = z^2"
      },
      {
        "element_type": "equation", 
        "content": {
          "latex": "x^2 + y^2 = z^2",
          "type": "inline"
        }
      },
      {
        "element_type": "equation",
        "content": {
          "latex": "f(x) = \\int_{-\\infty}^{\\infty} \\hat{f}(\\xi) e^{2\\pi i \\xi x} d\\xi",
          "type": "display"
        }
      }
    ]
  }]
}
```

## Benefits of This Approach

1. **Comprehensive**: Tests parsing, rendering, and integration
2. **Visual verification**: Ensures equations look correct
3. **Performance monitoring**: Tracks rendering speed
4. **Regression prevention**: Catches visual changes
5. **Real-world scenarios**: Uses actual LaTeX syntax
