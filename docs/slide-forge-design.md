# Slide Forge Design

## Overview

Slide Forge is a Python library for creating PowerPoint presentations. It is a wrapper around the python-pptx library, and provides a simple interface for creating presentations.

## Design Decisions

1. Use python-pptx for PowerPoint creation
2. Input is a Tex file, with Beamer class.

## Questions for Cascade

1. What's the best workflow for LaTeX → PowerPoint conversion?
2. Should we use AST-like parsing or template-based approach?
3. How do we handle complex LaTeX structures?

## Proposed Workflow

### Phase 1: LaTeX Parsing
```
LaTeX Beamer → Structured Data → PowerPoint API
```

**Option A: AST-like Parsing (Recommended)**
- Parse LaTeX into hierarchical structure
- Extract frames, environments, content
- Build semantic understanding

**Option B: Template-based**
- Use regex patterns to extract content
- Map to predefined PowerPoint templates
- Limited flexibility

### Phase 2: Content Mapping
```
Frame → Slide
Itemize → Bullet Points
Block → Formatted Text
Columns → Layout
Images → Picture Shapes
```

### Phase 3: PowerPoint Generation
```
Structured Data → python-pptx API → .pptx File
```

## Architecture Design

### Core Components

1. **LaTeX Parser** (`slideforge.parser`)
   - Tokenize LaTeX source
   - Build document tree
   - Extract metadata and frames

2. **Content Mapper** (`slideforge.mapper`)
   - Map LaTeX elements to PowerPoint elements
   - Handle layout decisions
   - Manage styling rules

3. **PowerPoint Builder** (`slideforge.builder`)
   - Use python-pptx to create slides
   - Apply formatting and positioning
   - Handle charts, shapes, tables

4. **Style Engine** (`slideforge.styles`)
   - Convert LaTeX themes to PowerPoint themes
   - Handle colors, fonts, layouts
   - Custom styling rules

### Data Flow

```
presentation.tex
    ↓
LaTeXParser.parse()
    ↓
DocumentTree {
  metadata: {...},
  frames: [
    {
      title: "Slide Title",
      elements: [...]
    }
  ]
}
    ↓
ContentMapper.map()
    ↓
SlideStructure {
  layout: "title_and_content",
  title: "Slide Title",
  content: [...]
}
    ↓
PowerPointBuilder.build()
    ↓
presentation.pptx
```

## Key Design Questions

### 1. AST vs Template?

**AST-like approach (Recommended):**
- Handles complex nested structures
- Preserves semantic meaning
- Extensible to new LaTeX features
- More complex to implement

**Template approach:**
- Simpler to start
- Predictable results
- Limited flexibility
- Breaks with complex LaTeX

### 2. How to handle LaTeX complexity?

**Hierarchical parsing:**
```python
class Document:
    def __init__(self):
        self.metadata = {}
        self.frames = []

class Frame:
    def __init__(self):
        self.title = ""
        self.elements = []

class Element:
    # Base class for text, itemize, block, etc.
    pass
```

### 3. What about LaTeX features?

**Supported in Phase 1:**
- Basic text and formatting
- Itemize/enumerate lists
- Block environments
- Images and figures
- Simple tables

**Future phases:**
- Math equations (as images/text)
- TikZ diagrams (as images)
- Complex overlays
- Custom commands

## Implementation Strategy

### Step 1: Core Parser
Start with the enhanced parser we built - it works well!

### Step 2: Mapping Layer
Create clean separation between parsing and PowerPoint generation.

### Step 3: Builder API
Design a fluent API for PowerPoint creation:
```python
builder = SlideForge()
builder.add_title_slide(title, author)
builder.add_content_slide(title, content)
builder.add_chart_slide(title, data)
builder.save("output.pptx")
```

## Next Steps

1. **Refactor existing code** into modular components
2. **Design the API** interface
3. **Create test cases** with different LaTeX structures
4. **Build the core parser** based on our working version