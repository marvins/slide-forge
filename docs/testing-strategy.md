# LaTeX Parser Testing Strategy

## Overview
Test the LaTeX parser by comparing real `.tex` files against expected Universal_Document structures.

## Test Structure

### Test Files Organization
```
tests/
├── fixtures/
│   ├── latex/
│   │   ├── simple/
│   │   │   ├── basic_frame.tex
│   │   │   ├── title_only.tex
│   │   │   └── text_content.tex
│   │   ├── complex/
│   │   │   ├── multiple_frames.tex
│   │   │   ├── itemize_lists.tex
│   │   │   ├── images.tex
│   │   │   └── mixed_content.tex
│   │   └── edge_cases/
│   │       ├── malformed_latex.tex
│   │       ├── empty_frame.tex
│   │       └── special_characters.tex
│   └── expected/
│       ├── simple/
│       │   ├── basic_frame.json
│       │   ├── title_only.json
│       │   └── text_content.json
│       ├── complex/
│       │   ├── multiple_frames.json
│       │   ├── itemize_lists.json
│       │   ├── images.json
│       │   └── mixed_content.json
│       └── edge_cases/
│           ├── malformed_latex.json
│           ├── empty_frame.json
│           └── special_characters.json
├── unit/
│   └── test_latex_parser.py
└── conftest.py
```

## Test Categories

### 1. Basic Functionality Tests
- **Single frame parsing**
- **Title extraction**
- **Simple text content**
- **Basic itemize lists**

### 2. Complex Structure Tests
- **Multiple frames**
- **Nested itemize**
- **Mixed content types**
- **Image references**

### 3. Edge Case Tests
- **Malformed LaTeX**
- **Empty frames**
- **Special characters**
- **Unicode content**

### 4. Integration Tests
- **End-to-end parsing**
- **Error handling**
- **Performance with large files**

## Sample Test Implementation

### Test Data Format
Expected results should be stored as JSON representing the Universal_Document structure:

```json
{
  "metadata": {
    "title": "Test Presentation",
    "author": "Test Author",
    "date": "2026-01-30"
  },
  "frames": [
    {
      "frame_number": 1,
      "title": "Test Frame",
      "layout": "title_and_content",
      "elements": [
        {
          "element_type": "text",
          "content": "This is test content",
          "position": null,
          "level": 0
        }
      ]
    }
  ]
}
```

### pytest Implementation
```python
import pytest
import json
from pathlib import Path
from slideforge.parsers.latex_parser import LaTeX_Parser
from slideforge.models.universal import Universal_Document

class TestLaTeXParser:
    @pytest.fixture
    def parser(self):
        return LaTeX_Parser()
    
    @pytest.fixture
    def fixtures_dir(self):
        return Path(__file__).parent.parent / "fixtures"
    
    def test_basic_frame_parsing(self, parser, fixtures_dir):
        """Test parsing of a basic frame with title and content."""
        tex_file = fixtures_dir / "latex" / "simple" / "basic_frame.tex"
        expected_file = fixtures_dir / "expected" / "simple" / "basic_frame.json"
        
        # Parse the LaTeX file
        document = parser.parse_file(tex_file)
        
        # Load expected result
        with open(expected_file, 'r') as f:
            expected = json.load(f)
        
        # Compare structures
        assert document.metadata.title == expected["metadata"]["title"]
        assert len(document.frames) == len(expected["frames"])
        
        # Compare first frame
        frame = document.frames[0]
        expected_frame = expected["frames"][0]
        
        assert frame.frame_number == expected_frame["frame_number"]
        assert frame.title == expected_frame["title"]
        assert frame.layout.value == expected_frame["layout"]
        
        # Compare elements
        assert len(frame.elements) == len(expected_frame["elements"])
        for i, element in enumerate(frame.elements):
            expected_element = expected_frame["elements"][i]
            assert element.element_type.value == expected_element["element_type"]
            assert element.content == expected_element["content"]
    
    @pytest.mark.parametrize("test_name", [
        "basic_frame",
        "title_only", 
        "text_content",
        "multiple_frames",
        "itemize_lists",
        "images"
    ])
    def test_parsing_fixtures(self, parser, fixtures_dir, test_name):
        """Parameterized test for all fixture files."""
        tex_file = fixtures_dir / "latex" / test_name.split('_')[0] / f"{test_name}.tex"
        expected_file = fixtures_dir / "expected" / test_name.split('_')[0] / f"{test_name}.json"
        
        if not tex_file.exists():
            pytest.skip(f"Test file {tex_file} not found")
        
        document = parser.parse_file(tex_file)
        
        with open(expected_file, 'r') as f:
            expected = json.load(f)
        
        # Basic structure validation
        assert document.source_format == "latex"
        assert len(document.frames) == len(expected["frames"])
```

## Test Data Generation

### Helper Script to Generate Expected JSON
```python
#!/usr/bin/env python3
"""
Generate expected JSON files from LaTeX files for testing.
Run this once to create the baseline expected results.
"""

import json
from pathlib import Path
from slideforge.parsers.latex_parser import LaTeX_Parser

def generate_expected_json():
    parser = LaTeX_Parser()
    fixtures_dir = Path("tests/fixtures")
    
    for tex_file in fixtures_dir.glob("latex/**/*.tex"):
        # Parse the LaTeX file
        document = parser.parse_file(tex_file)
        
        # Convert to JSON-serializable format
        doc_dict = {
            "metadata": {
                "title": document.metadata.title,
                "author": document.metadata.author,
                "date": document.metadata.date
            },
            "frames": []
        }
        
        for frame in document.frames:
            frame_dict = {
                "frame_number": frame.frame_number,
                "title": frame.title,
                "layout": frame.layout.value if frame.layout else None,
                "elements": []
            }
            
            for element in frame.elements:
                element_dict = {
                    "element_type": element.element_type.value,
                    "content": element.content,
                    "position": {
                        "x": element.position.x,
                        "y": element.position.y,
                        "width": element.position.width,
                        "height": element.position.height
                    } if element.position else None,
                    "level": element.level
                }
                frame_dict["elements"].append(element_dict)
            
            doc_dict["frames"].append(frame_dict)
        
        # Determine output path
        relative_path = tex_file.relative_to(fixtures_dir / "latex")
        output_path = fixtures_dir / "expected" / relative_path.with_suffix('.json')
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write JSON file
        with open(output_path, 'w') as f:
            json.dump(doc_dict, f, indent=2)
        
        print(f"Generated: {output_path}")

if __name__ == "__main__":
    generate_expected_json()
```

## Running Tests

### Command Line
```bash
# Run all parser tests
pytest tests/unit/test_latex_parser.py -v

# Run specific test category
pytest tests/unit/test_latex_parser.py::TestLaTeXParser::test_basic_frame_parsing -v

# Run with coverage
pytest tests/unit/test_latex_parser.py --cov=slideforge.parsers --cov-report=html

# Generate coverage report
coverage html
```

## Benefits of This Approach

1. **Real-world testing**: Uses actual LaTeX syntax
2. **Regression prevention**: Changes that break existing files will be caught
3. **Easy to extend**: Add new .tex files and corresponding .json expectations
4. **Clear documentation**: Test files serve as examples of supported features
5. **Performance baseline**: Can track parsing performance over time

## Next Steps

1. Create the test directory structure
2. Generate initial fixture files from your sample presentations
3. Run the generation script to create expected JSON files
4. Implement the pytest test class
5. Add tests to CI/CD pipeline
