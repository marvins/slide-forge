#!/bin/bash

# Development Setup Script for Slide Forge
# This script sets up the development environment with pre-commit hooks

set -e

echo "🚀 Setting up Slide Forge development environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check for existing virtual environment
if [ -d "venv" ]; then
    echo "📁 Found existing virtual environment 'venv'"
    echo "🔌 Activating virtual environment..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "📁 Found existing virtual environment '.venv'"
    echo "🔌 Activating virtual environment..."
    source .venv/bin/activate
else
    echo "ℹ️  No virtual environment found. Using system Python."
    echo "💡 Consider creating a virtual environment: python3 -m venv venv"
fi

# Check if pip is available
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip is required but not installed. Please install pip first."
    exit 1
fi

# Use pip if available, otherwise pip3
PIP_CMD="pip3"
if command -v pip &> /dev/null; then
    PIP_CMD="pip"
fi

# Install the package in development mode with dev dependencies
echo "📦 Installing slide-forge with development dependencies..."
$PIP_CMD install -e ".[dev]"

# Install pre-commit hooks
echo "🔧 Installing pre-commit hooks..."
pre-commit install

# Run pre-commit on all files to check current status
echo "🔍 Running pre-commit checks on all files..."
pre-commit run --all-files

echo ""
echo "✅ Development environment setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Fix any issues reported by pre-commit above"
echo "   2. Start developing your changes"
echo "   3. Pre-commit hooks will automatically run before each commit"
echo ""
echo "🔧 Useful commands:"
echo "   - Activate venv: source venv/bin/activate (if you created one)"
echo "   - Run tests: pytest"
echo "   - Format code: black src/ tests/"
echo "   - Check linting: flake8 src/ tests/"
echo "   - Type checking: mypy src/"
echo "   - Run all checks: pre-commit run --all-files"
echo ""
echo "💡 Virtual Environment:"
if [ -d "venv" ] || [ -d ".venv" ]; then
    echo "   ✅ Virtual environment is active and ready"
else
    echo "   ℹ️  No virtual environment found. Consider creating one:"
    echo "       python3 -m venv venv && source venv/bin/activate"
fi
echo ""
echo "📖 For more information, see README.md"
