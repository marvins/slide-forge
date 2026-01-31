# Testing Guidelines

## Rule: Add Test Cases for Edge Cases and Weird Situations

Whenever you encounter a weird situation, edge case, or unexpected behavior during development, **immediately create a corresponding unit test case** to capture that scenario.

### Why This Matters

1. **Prevent Regression**: Tests ensure that once we fix a weird issue, it doesn't come back later
2. **Documentation**: Tests serve as living documentation of how the system should behave
3. **Confidence**: Comprehensive test coverage gives us confidence to make changes safely
4. **Knowledge Sharing**: Tests help other developers understand edge cases and expected behavior

### When to Add Tests

Add a test case whenever you:

- **Fix a bug** that was caused by an edge case
- **Encounter unexpected input** that the system handles poorly
- **Find malformed data** that should be handled gracefully
- **Discover performance issues** with specific input patterns
- **Handle special characters** or Unicode content
- **Deal with malformed LaTeX** or other structured data
- **Experience parsing failures** with specific content patterns

### How to Add Tests

1. **Data-Driven Tests**: For LaTeX parsing and similar scenarios, use the data-driven test structure:
   ```
   tests/parsers/test_data/
   ├── edge_cases/
   │   ├── malformed_latex.tex
   │   ├── special_characters.tex
   │   └── unicode_content.tex
   ```

2. **Update Manifest**: Add the new test case to `test_manifest.json`:
   ```json
   {
     "file": "weird_situation.tex",
     "description": "Brief description of the weird situation",
     "expected_elements": {"text": 2},
     "should_parse": true
   }
   ```

3. **Specific Tests**: For non-data-driven scenarios, add focused unit tests:
   ```python
   def test_weird_situation_handling(self, parser):
       """Test handling of [specific weird situation]."""
       weird_input = "..."
       result = parser.parse_string(weird_input)
       assert result.is_valid  # Or whatever the expected behavior is
   ```

### Test Case Examples

#### LaTeX Parsing Edge Cases
- Malformed LaTeX syntax
- Unclosed environments
- Special characters in math mode
- Unicode characters in text
- Empty or whitespace-only content
- Nested environments with errors

#### General Edge Cases
- Empty input files
- Extremely large files
- Files with mixed encodings
- Network timeouts during processing
- Invalid file permissions

### Best Practices

1. **Be Specific**: Test the exact weird situation you encountered
2. **Document Intent**: Use clear test names and descriptions
3. **Test Both Success and Failure**: Test both the happy path and error conditions
4. **Keep Tests Isolated**: Each test should be independent
5. **Use Real Data**: Use actual problematic input when possible

### Examples of Good Test Names

```python
def test_malformed_latex_unclosed_environment(self):
def test_unicode_characters_in_math_mode(self):
def test_empty_frame_with_only_whitespace(self):
def test_nested_itemize_with_malformed_syntax(self):
```

### Review Checklist

Before considering a weird situation "handled", ask:

- [ ] Have I added a test case that reproduces the issue?
- [ ] Does the test clearly document the expected behavior?
- [ ] Will this test prevent regression if the code changes?
- [ ] Is the test added to the appropriate test suite?
- [ ] Does the test have a clear, descriptive name?

### Remember

> "If it's weird enough to make you pause, it's weird enough to need a test."

Every edge case you encounter today is someone else's production bug tomorrow. Test it now, thank yourself later.
