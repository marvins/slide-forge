#!/bin/bash

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
