# Slide Forge Development Rules

This directory contains development rules and guidelines for the Slide Forge project.

## Available Rules

### Core Development Standards

1. **[Python File Naming](./python-file-naming.md)**
   - Snake_case naming convention for Python files
   - File-to-class mapping guidelines
   - Package structure recommendations

2. **[License Header](./license-header.md)**
   - Mandatory license header for all Python files
   - Header format and placement guidelines
   - Enforcement and maintenance procedures

3. **[One Class Per File](./one-class-per-file.md)**
   - Optional but recommended convention
   - Guidelines for class organization
   - When to combine vs. separate classes

## Usage

### For New Development
1. Read the relevant rules before creating new files
2. Follow the naming conventions when creating Python files
3. Include the license header in all new Python files
4. Consider the one-class-per-file convention for better organization

### For Code Review
1. Check that new files follow the naming conventions
2. Verify license headers are present and correct
3. Review class organization and file structure
4. Suggest improvements based on these guidelines

### For Maintenance
1. Update existing files to follow these conventions when possible
2. Add headers to files that are missing them
3. Consider refactoring large files during major updates
4. Keep these rules updated as the project evolves

## Integration with Development Workflow

### Pre-commit Hooks
- Check for license header presence
- Verify file naming conventions
- Flag potential organizational issues

### IDE Configuration
- Set up file templates with license headers
- Configure naming convention suggestions
- Enable code organization tools

### CI/CD Pipeline
- Automated checks for rule compliance
- Generate reports on code quality
- Prevent merges that violate core rules

## Contributing to Rules

1. Propose changes to existing rules through issues
2. Suggest new rules for better development practices
3. Update rules when project requirements change
4. Ensure all rules are documented and actionable

## Rule Priority

### High Priority (Must Follow)
- License header inclusion
- Basic file naming conventions

### Medium Priority (Should Follow)
- One class per file convention
- Package structure guidelines

### Low Priority (Nice to Have)
- Advanced organizational patterns
- Optional formatting suggestions

## Tools and Automation

### Recommended Tools
- Pre-commit hooks for automated checking
- IDE plugins for real-time feedback
- Linting rules for convention enforcement

### Custom Scripts
- License header insertion/updating
- File naming validation
- Code organization analysis

## Documentation

These rules are part of the broader project documentation:
- [Class Diagrams](../docs/class-diagrams.md)
- [Architecture Overview](../docs/architecture.md)
- [Contributing Guidelines](../CONTRIBUTING.md)

---

**Note**: These rules are designed to evolve with the project. Regular reviews and updates are encouraged to ensure they remain relevant and helpful.
