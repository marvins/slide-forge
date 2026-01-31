# Sequence Diagrams

This page contains sequence diagrams that illustrate the flow of operations within Slide Forge.

## Conversion Flow Diagram

```mermaid
sequenceDiagram
    participant User
    participant Core as Slide_Forge
    participant Parser as LaTeX_Parser
    participant Mapper as Content_Mapper
    participant Builder as PowerPoint_Builder
    participant File as File System

    User->>Core: convert_file(input.tex, output.pptx)
    Core->>Core: detect_format(input.tex)
    Core->>Core: detect_format(output.pptx)
    
    Note over Core: Parsing Phase
    Core->>Parser: parse_file(input.tex)
    Parser->>File: read input.tex
    File-->>Parser: LaTeX content
    Parser->>Parser: parse LaTeX structure
    Parser-->>Core: Universal_Document
    
    Note over Core: Mapping Phase
    Core->>Mapper: map_document(document, 'pptx')
    Mapper->>Mapper: _position_frame_elements()
    loop For each frame
        Mapper->>Mapper: _position_element()
        Mapper->>Mapper: calculate layout
    end
    Mapper-->>Core: Positioned frames
    
    Note over Core: Building Phase
    Core->>Builder: build_presentation(frames, output.pptx)
    Builder->>Builder: create PowerPoint presentation
    loop For each frame
        Builder->>Builder: _add_elements_to_slide()
        loop For each element
            alt Element has position
                Builder->>Builder: use element.position
            else No position
                Builder->>Builder: use fallback positioning
            end
            Builder->>Builder: render element
        end
    end
    Builder->>File: save output.pptx
    File-->>Builder: success
    Builder-->>Core: True
    Core-->>User: Conversion successful
```

## Component Initialization Diagram

```mermaid
sequenceDiagram
    participant Core as Slide_Forge
    participant Parser as LaTeX_Parser
    participant Builder as PowerPoint_Builder
    participant Mapper as Content_Mapper
    participant Detector as Format_Detector

    Core->>Core: __init__()
    Core->>Core: _initialize_components()
    
    Note over Core: Parser Registration
    Core->>Parser: try import LaTeX_Parser
    Parser-->>Core: LaTeX_Parser instance
    Core->>Core: register_parser('latex', parser)
    
    Note over Core: Builder Registration  
    Core->>Builder: try import PowerPoint_Builder
    Builder-->>Core: PowerPoint_Builder instance
    Core->>Core: register_builder('pptx', builder)
    
    Note over Core: Mapper Registration
    Core->>Mapper: try import Content_Mapper
    Mapper-->>Core: Content_Mapper instance
    Core->>Core: register_mapper(mapper)
    
    Note over Core: Format Detector
    Core->>Detector: Format_Detector()
    Detector-->>Core: detector instance
```

## Image Path Resolution Diagram

```mermaid
sequenceDiagram
    participant Builder as PowerPoint_Builder
    participant Element as Universal_Element
    participant Path as pathlib.Path
    participant File as File System

    Builder->>Element: _add_image_element()
    Element-->>Builder: image_path (relative)
    
    Builder->>Path: Path(image_path).is_absolute()
    alt Absolute path
        Path-->>Builder: True
        Builder->>File: Path(image_path).exists()
    else Relative path
        Path-->>Builder: False
        Builder->>Path: source_dir = Path(source_path).parent
        Builder->>Path: image_path = source_dir / image_path
        Builder->>File: image_path.exists()
    end
    
    alt File exists
        File-->>Builder: True
        Builder->>Builder: slide_obj.shapes.add_picture()
        Note over Builder: Image successfully added
    else File not found
        File-->>Builder: False
        Builder->>Builder: logger.warning("Image file not found")
        Note over Builder: Image skipped with warning
    end
```

## Error Handling Flow

```mermaid
sequenceDiagram
    participant User
    participant Core as Slide_Forge
    participant Parser as LaTeX_Parser
    participant Builder as PowerPoint_Builder
    participant Logger as logging

    User->>Core: convert_file()
    
    alt Parser error
        Core->>Parser: parse_file()
        Parser-->>Core: ParseError
        Core->>Logger: error("Parse failed")
        Core->>User: raise Slide_Forge_Error
    else Mapping error
        Core->>Mapper: map_document()
        Mapper-->>Core: MappingError
        Core->>Logger: error("Mapping failed")
        Core->>User: raise Slide_Forge_Error
    else Builder error
        Core->>Builder: build_presentation()
        Builder->>Builder: element processing
        Builder->>Logger: warning("Failed to add element")
        Note over Builder: Continue with other elements
        Builder-->>Core: False (build failed)
        Core->>Logger: error("Build failed")
        Core->>User: raise BuilderError
    else Success
        Core->>Builder: build_presentation()
        Builder-->>Core: True
        Core->>Logger: info("Successfully built")
        Core-->>User: True (success)
    end
```

## Layout Positioning Flow

```mermaid
sequenceDiagram
    participant Mapper as Content_Mapper
    participant Frame as Universal_Frame
    participant Element as Universal_Element
    participant Position as Position

    Mapper->>Frame: _position_frame_elements()
    Note over Mapper: Initialize layout constants
    Mapper->>Mapper: current_y = MARGIN_TOP
    
    loop For each element in frame
        Mapper->>Element: _position_element()
        Note over Element: Calculate element height
        alt TEXT element
            Element->>Element: _estimate_text_height()
        else ITEMIZE element
            Element->>Element: _estimate_itemize_height()
        else IMAGE element
            Element->>Element: height = 4.0
        else Other element
            Element->>Element: height = 0.5
        end
        
        Element->>Position: Position(x, y, width, height)
        Position-->>Element: position object
        Element->>Element: Universal_Element with position
        Element-->>Mapper: positioned_element
        
        Mapper->>Mapper: current_y += height + ELEMENT_SPACING
    end
    
    Mapper->>Mapper: return positioned_frame
```

## Font Size Handling Flow

```mermaid
sequenceDiagram
    participant Builder as PowerPoint_Builder
    participant Config as Theme_Config
    participant Pt as pptx.util.Pt
    participant Font as Font Object

    Builder->>Config: get('content_font_size', 18)
    Config-->>Builder: font_size (integer)
    
    Builder->>Builder: if font_size > 0
    alt Valid font size
        Builder->>Pt: Pt(font_size)
        Pt-->>Builder: Pt object (e.g., 228600)
        Builder->>Font: font.size = Pt_object
        Note over Builder: Font size set correctly
    else Invalid font size (0)
        Builder->>Builder: skip font.size assignment
        Note over Builder: Uses PowerPoint default
    end
    
    Note over Builder: Same pattern for title_font_size
```

These sequence diagrams illustrate the key flows and interactions within the Slide Forge system, helping developers understand the architecture and data flow.
