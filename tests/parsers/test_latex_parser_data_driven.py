#!/usr/bin/env python3

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

"""
Data-driven tests for LaTeX parser using test manifest.
"""

import json
import pytest
from pathlib import Path

from slideforge.parsers.latex_parser import LaTeX_Parser
from slideforge.models.universal import Element_Type


class TestLaTeXParserDataDriven:
    """Data-driven tests for LaTeX parser."""

    @pytest.fixture
    def parser(self):
        """Create LaTeX parser instance."""
        return LaTeX_Parser()

    @pytest.fixture
    def test_manifest(self):
        """Load test manifest."""
        manifest_path = Path(__file__).parent / "test_data" / "test_manifest.json"
        with open(manifest_path, 'r') as f:
            return json.load(f)

    @pytest.fixture
    def test_data_dir(self):
        """Get test data directory."""
        return Path(__file__).parent / "test_data"

    def test_manifest_structure(self, test_manifest):
        """Test that manifest has valid structure."""
        assert isinstance(test_manifest, dict)
        required_categories = ["basic", "equations", "formatting", "complex", "edge_cases"]
        
        for category in required_categories:
            assert category in test_manifest
            assert isinstance(test_manifest[category], list)
            
            for test_case in test_manifest[category]:
                assert "file" in test_case
                assert "description" in test_case
                assert "expected_elements" in test_case

    @pytest.mark.parametrize("category", ["basic", "equations", "formatting", "complex", "edge_cases"])
    def test_parse_category(self, parser, test_manifest, test_data_dir, category):
        """Test parsing all files in a category."""
        if category not in test_manifest:
            pytest.skip(f"Category {category} not found in manifest")
            
        for test_case in test_manifest[category]:
            test_file = test_data_dir / category / test_case["file"]
            
            if not test_file.exists():
                pytest.skip(f"Test file {test_file} does not exist")
                
            # Read LaTeX content
            with open(test_file, 'r', encoding='utf-8') as f:
                latex_content = f.read()
            
            # Parse the content
            try:
                document = parser.parse_string(latex_content, source_path=str(test_file))
            except Exception as e:
                if test_case.get("should_parse", True):
                    pytest.fail(f"Failed to parse {test_file}: {e}")
                else:
                    # Expected to fail, so this is okay
                    continue
            
            # Validate basic structure
            assert document is not None
            assert document.source_format == 'latex'
            
            # Check expected number of frames
            if "expected_frames" in test_case:
                assert len(document.frames) == test_case["expected_frames"], \
                    f"Expected {test_case['expected_frames']} frames, got {len(document.frames)} for {test_file}"
            
            # Check frame title if specified
            if "expected_title" in test_case:
                assert document.frames[0].title == test_case["expected_title"], \
                    f"Expected title '{test_case['expected_title']}', got '{document.frames[0].title}' for {test_file}"
            
            # Count elements by type
            element_counts = {}
            equation_types = []
            
            for frame in document.frames:
                for element in frame.elements:
                    element_type = element.element_type.value
                    element_counts[element_type] = element_counts.get(element_type, 0) + 1
                    
                    if element_type == "equation":
                        eq_type = element.content.get('type', 'unknown')
                        equation_types.append(eq_type)
            
            # Check expected element counts
            expected_elements = test_case["expected_elements"]
            for element_type, expected_count in expected_elements.items():
                actual_count = element_counts.get(element_type, 0)
                assert actual_count == expected_count, \
                    f"Expected {expected_count} {element_type} elements, got {actual_count} for {test_file}"
            
            # Check equation types if specified
            if "equation_types" in test_case:
                assert equation_types == test_case["equation_types"], \
                    f"Expected equation types {test_case['equation_types']}, got {equation_types} for {test_file}"

    def test_all_test_files_exist(self, test_manifest, test_data_dir):
        """Test that all files referenced in manifest actually exist."""
        missing_files = []
        
        for category, test_cases in test_manifest.items():
            for test_case in test_cases:
                test_file = test_data_dir / category / test_case["file"]
                if not test_file.exists():
                    missing_files.append(str(test_file))
        
        if missing_files:
            pytest.fail(f"Missing test files: {missing_files}")

    def test_edge_case_handling(self, parser, test_data_dir):
        """Test that edge cases are handled gracefully."""
        edge_case_files = [
            "edge_cases/malformed_latex.tex",
            "edge_cases/special_characters.tex",
            "edge_cases/unicode_content.tex"
        ]
        
        for file_path in edge_case_files:
            full_path = test_data_dir / file_path
            if not full_path.exists():
                continue
                
            with open(full_path, 'r', encoding='utf-8') as f:
                latex_content = f.read()
            
            # Should not raise exceptions even for malformed content
            try:
                document = parser.parse_string(latex_content, source_path=str(full_path))
                assert document is not None
                assert document.source_format == 'latex'
            except Exception as e:
                pytest.fail(f"Edge case {file_path} should not raise exceptions: {e}")
