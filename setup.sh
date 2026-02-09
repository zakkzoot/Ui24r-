#!/bin/bash

# Automated setup script for ui24rsc on Linux/macOS
# This script sets up the development environment and installs dependencies

set -e

echo "=========================================="
echo "UI24RSC Setup Script for Linux/macOS"
echo "=========================================="
echo ""

# Check if Python 3.9+ is installed
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed. Please install Python 3.9.1 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Found Python $PYTHON_VERSION"

if [[ $(python3 -c 'import sys; print(sys.version_info >= (3, 9))') != "True" ]]; then
    echo "ERROR: Python 3.9.1 or higher is required. Found Python $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

# Install package in editable mode with dependencies
echo ""
echo "Installing ui24rsc in editable mode..."
python3 -m pip install -e .

# Install development dependencies
echo ""
echo "Installing development dependencies..."
python3 -m pip install pytest

echo ""
echo "=========================================="
echo "✓ Setup completed successfully!"
echo "=========================================="
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run tests:"
echo "  pytest test"
echo ""
echo "To use the CLI tool:"
echo "  ui24rsc --help"
echo ""