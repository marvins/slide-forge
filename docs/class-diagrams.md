# Slide Forge Class Diagrams

## Core Architecture

```mermaid
classDiagram
    class Slide_Forge {
        -parser: latex_parser
        -mapper: content_mapper
        -builder: powerpoint_builder
        +convert_file(latex_file: str, output_file: str) bool
        +convert_string(latex_content: str, output_file: str) bool
    }

    class LaTeX_Parser {
        +parse_file(filepath: str) Document
        +parse_string(content: str) Document
        -_extract_preamble(content: str) Metadata
        -_extract_frames(content: str) List[Frame]
        -_parse_frame(frame_content: str) Frame
    }

    class Content_Mapper {
        +map_document(document: Document) List[Slide_Structure]
        +map_frame(frame: Frame) Slide_Structure
        +map_element(element: Element) Slide_Element
        -_determine_layout(elements: List[Element]) Layout_Type
    }

    class PowerPoint_Builder {
        -presentation: Presentation
        +build_presentation(slides: List[Slide_Structure])
        +add_slide(slide: Slide_Structure)
        +save(filepath: str)
        -_create_title_slide(slide: Slide_Structure)
        -_create_content_slide(slide: Slide_Structure)
    }

    Slide_Forge --> LaTeX_Parser
    Slide_Forge --> Content_Mapper
    Slide_Forge --> PowerPoint_Builder
```

## Data Model

```mermaid
classDiagram
    class Document {
        +metadata: Metadata
        +frames: List[Frame]
    }

    class Metadata {
        +title: str
        +author: str
        +date: str
        +documentclass: str
    }

    class Frame {
        +number: int
        +title: str
        +elements: List[Element]
    }

    class Element {
        <<abstract>>
        +type: Element_Type
    }

    class Text_Element {
        +text: str
        +formatting: Formatting
    }

    class Itemize_Element {
        +content: List[Item]
    }

    class Block_Element {
        +title: str
        +content: List[Text]
    }

    class Image_Element {
        +path: str
        +caption: str
    }

    Element <|-- Text_Element
    Element <|-- Itemize_Element
    Element <|-- Block_Element
    Element <|-- Image_Element

    Document *-- Metadata
    Document *-- Frame
    Frame *-- Element
```

## PowerPoint Output Model

```mermaid
classDiagram
    class Slide_Structure {
        +layout: Layout_Type
        +title: str
        +elements: List[Slide_Element]
    }

    class Slide_Element {
        <<abstract>>
        +type: Slide_Element_Type
    }

    class Title_Element {
        +text: str
        +style: Title_Style
    }

    class Bullet_Element {
        +text: str
        +level: int
        +style: Bullet_Style
    }

    class Text_Box_Element {
        +text: str
        +position: Position
        +style: Text_Style
    }

    class Image_Element {
        +path: str
        +position: Position
        +size: Size
    }

    Slide_Element <|-- Title_Element
    Slide_Element <|-- Bullet_Element
    Slide_Element <|-- Text_Box_Element
    Slide_Element <|-- Image_Element

    Slide_Structure *-- Slide_Element
```

## CLI Application

```mermaid
classDiagram
    class CLI {
        +main() None
        +parse_args() Namespace
        +convert_file(args: Namespace) int
        -_print_usage()
        -_validate_inputs(input: str, output: str) bool
    }

    class ConversionConfig {
        +input_file: str
        +output_file: str
        +theme: str
        +preserve_colors: bool
        +include_images: bool
        +verbose: bool
    }

    CLI --> ConversionConfig
    CLI --> Slide_Forge
```

## Component Interactions

```mermaid
sequenceDiagram
    participant CLI
    participant Slide_Forge
    participant LaTeX_Parser
    participant Content_Mapper
    participant PowerPoint_Builder

    CLI->>Slide_Forge: convert_file(input, output)
    Slide_Forge->>LaTeX_Parser: parse_file(input)
    LaTeX_Parser-->>Slide_Forge: Document
    Slide_Forge->>Content_Mapper: map_document(document)
    Content_Mapper-->>Slide_Forge: List[Slide_Structure]
    Slide_Forge->>PowerPoint_Builder: build_presentation(slides)
    PowerPoint_Builder->>PowerPoint_Builder: add_slide() for each slide
    PowerPointBuilder-->>SlideForge: save(output)
    SlideForge-->>CLI: success/failure
```

## Error Handling

```mermaid
classDiagram
    class Slide_Forge_Error {
        <<abstract>>
        +message: str
    }

    class Parse_Error {
        +line_number: int
        +latex_snippet: str
    }

    class Mapping_Error {
        +element_type: str
        +reason: str
    }

    class Builder_Error {
        +slide_number: int
        +operation: str
    }

    Slide_Forge_Error <|-- Parse_Error
    Slide_Forge_Error <|-- Mapping_Error
    Slide_Forge_Error <|-- Builder_Error
```

## Enums and Types

```mermaid
classDiagram
    class Element_Type {
        <<enumeration>>
        text
        itemize
        block
        image
        table
        math
    }

    class Layout_Type {
        <<enumeration>>
        title_slide
        title_and_content
        section_header
        two_column
        blank
    }

    class Formatting {
        <<enumeration>>
        bold
        italic
        underline
        normal
    }

    class Slide_Element_Type {
        <<enumeration>>
        title
        bullet
        text_box
        image
        shape
        chart
    }
```
