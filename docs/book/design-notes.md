# Design Notes

This page contains the original design documentation and architectural decisions for Slide Forge, along with insights from implementation.

## Overview

Slide Forge is a Python library for creating PowerPoint presentations. It is a wrapper around the python-pptx library, and provides a simple interface for creating presentations.

## Design Decisions

1. Use python-pptx for PowerPoint creation
2. Input is a Tex file, with Beamer class.

## Questions for Cascade

1. What's the best workflow for LaTeX → PowerPoint conversion?
2. Should we use AST-like parsing or template-based approach?
3. How do we handle complex LaTeX structures?

## Current Workflow

### Phase 1: LaTeX Parsing ✅ COMPLETED
```
LaTeX Beamer → Universal_Document → PowerPoint API
```

**Implemented Approach**: AST-like parsing with regex-based extraction
- Parse LaTeX into hierarchical Universal_Document structure
- Extract frames, environments, and content
- Build semantic understanding of document structure
- Create format-agnostic data models

### Phase 2: Content Mapping ✅ COMPLETED
```
Universal_Document → Positioned Universal_Document
```

**Implemented Features**:
- Layout-aware positioning calculations
- Semantic element mapping (frames → slides, itemize → bullets, etc.)
- Position assignment based on slide layout types
- Image path resolution with source context

### Phase 3: PowerPoint Generation ✅ COMPLETED
```
Positioned Universal_Document → python-pptx API → .pptx File
```

**Implemented Features**:
- Native PowerPoint placeholder usage
- Smart text box positioning with fallbacks
- Font size handling with proper Pt() units
- Image embedding and path resolution
- Theme system with multiple PowerPoint themes

## Next Phase Workflow

### Phase 4: Advanced Features 🔄 IN PROGRESS
```
Enhanced LaTeX → Extended Universal_Document → Advanced PowerPoint
```

**Planned Enhancements**:
- Math equation rendering (as images/text)
- TikZ diagram conversion
- Custom LaTeX command support
- Beamer overlay specifications
- Advanced table formatting

### Phase 5: Multi-Format Support 📋 PLANNED
```
Universal_Document → Multiple Output Formats
```

**Target Formats**:
- PowerPoint → LaTeX (round-trip conversion)
- Markdown → PowerPoint
- HTML/Web presentations
- PDF export

### Phase 6: Production Features 📋 PLANNED
```
Enhanced System → Enterprise-Ready Solution
```

**Enterprise Features**:
- Template system with custom designs
- Plugin architecture for extensibility
- Performance optimizations
- Batch processing capabilities
- API for integration

## Implementation Insights & Lessons Learned

### 1. Positioning Architecture

**Initial Problem**: All elements were overlapping because they were positioned at the same coordinates.

**Solution**: Implemented a two-layer positioning system:
- **Content Mapper**: Calculates semantic positions based on layout type
- **PowerPoint Builder**: Renders elements at calculated positions

**Key Insight**: Separation of concerns is crucial. The mapper handles "what goes where" while the builder handles "how to render."

### 2. Native PowerPoint Placeholder Usage

**Initial Problem**: Content was dumped into text boxes, causing "dashed boxes" (PowerPoint's default placeholders) to remain unused.

**Solution**: Smart placeholder usage:
```python
# Use native content placeholder for first element
if not content_placeholder_used and slide_obj.placeholders:
    content_placeholder_used = self._add_text_to_placeholder(slide_obj, element, config, preserve_colors)
else:
    self._add_text_element(slide_obj, element, config, preserve_colors)
```

**Key Insight**: PowerPoint layouts work best when you respect their native structure. Use placeholders first, fall back to positioned text boxes.

### 3. Font Size Handling

**Problem**: Raw integers caused "value must be in range" errors with python-pptx.

**Solution**: Use proper Pt() units:
```python
from pptx.util import Pt
p.font.size = Pt(font_size)  # Instead of p.font.size = font_size
```

**Key Insight**: python-pptx has specific unit requirements. Always use the provided utility functions.

### 4. Image Path Resolution

**Problem**: Images were looked for in the wrong directory (project root instead of LaTeX file directory).

**Solution**: Pass source path through the conversion chain:
```python
# Core passes source path to builder
build_options = {**options.custom_settings, 'source_path': document.source_path}
success = builder.build_presentation(slide_structures, output_path, **build_options)
```

**Key Insight**: Context matters. The builder needs to know where the source file was located to resolve relative paths.

### 5. Layout System Design

**Implementation**: Content mapper calculates positions based on layout constants:
```python
MARGIN_LEFT = 1.0
MARGIN_TOP = 2.5  # Below title
ELEMENT_SPACING = 0.4
CONTENT_WIDTH = SLIDE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
```

**Key Insight**: Layout calculations should be format-agnostic in the mapper, with format-specific rendering in the builder.

## Architecture Refinements

### Current Data Flow (Revised)
```
presentation.tex
    ↓
LaTeXParser.parse()
    ↓
Universal_Document {
  metadata: {...},
  frames: [Universal_Frame {
    title: "Slide Title",
    elements: [Universal_Element {
      element_type: Element_Type.TEXT,
      content: "content",
      position: Position {x: 1.0, y: 2.5, width: 8.0, height: 0.5}
    }]
  }]
}
    ↓
ContentMapper.map()  # ← NEW: Adds positioning
    ↓
Positioned Universal_Document
    ↓
PowerPointBuilder.build()  # ← ENHANCED: Uses placeholders + positioning
    ↓
presentation.pptx
```

### Key Architectural Principles

1. **Universal Models**: Format-agnostic data structures
2. **Smart Positioning**: Layout calculations in mapper, rendering in builder
3. **Native Integration**: Respect target format's native structures (placeholders)
4. **Context Awareness**: Pass source context through the conversion chain
5. **Graceful Degradation**: Fallbacks when ideal approaches fail

## Performance Considerations

### Current Bottlenecks
1. **LaTeX Parsing**: Complex regex operations
2. **Image Processing**: File I/O for each image
3. **Position Calculations**: Per-element computations

### Optimization Opportunities
1. **Caching**: Cache parsed documents and position calculations
2. **Batch Processing**: Process multiple images in parallel
3. **Lazy Loading**: Load images only when needed

## Future Enhancements

### Phase 2: Advanced Features
- **Math Equations**: Render LaTeX math as images or text
- **TikZ Diagrams**: Convert to raster images
- **Custom Commands**: User-defined LaTeX command support
- **Overlays**: Handle Beamer overlay specifications

### Phase 3: Multi-Format Support
- **PowerPoint → LaTeX**: Round-trip conversion
- **Markdown Support**: MD to PowerPoint conversion
- **HTML Export**: Web-based presentation formats

### Phase 4: Advanced Features
- **Template System**: Custom PowerPoint templates
- **Animation Support**: PowerPoint animations from LaTeX overlays
- **Plugin Architecture**: Extensible parser/builder system

## Testing Strategy

### Current Testing Gaps
1. **Integration Tests**: End-to-end conversion testing
2. **Edge Cases**: Complex LaTeX structures
3. **Performance Tests**: Large presentation handling

### Recommended Test Structure
```
tests/
├── unit/
│   ├── test_parser.py
│   ├── test_mapper.py
│   └── test_builder.py
├── integration/
│   ├── test_simple_conversion.py
│   ├── test_complex_conversion.py
│   └── test_error_handling.py
├── fixtures/
│   ├── latex/
│   └── expected/
└── performance/
    └── test_large_files.py
```

## Conclusion

The current architecture has proven effective for basic LaTeX to PowerPoint conversion. The key success factors are:

1. **Clean Separation**: Parser → Mapper → Builder pipeline
2. **Universal Models**: Format-agnostic data structures
3. **Smart Positioning**: Layout-aware content placement
4. **Native Integration**: Respect for PowerPoint's structure
5. **Robust Error Handling**: Graceful degradation when things go wrong

The system is now ready for Phase 2 enhancements while maintaining the solid foundation established in Phase 1.
