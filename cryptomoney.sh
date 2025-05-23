#!/bin/bash
if ! command -v py &> /dev/null; then
    echo "Python is not found in your system."
    echo "Please do one of the following:"
    echo "1. Install Python from https://www.python.org/downloads/ (recommended)"
    echo "   - Make sure to check 'Add Python to PATH' during installation"
    echo "2. Or install Python from Microsoft Store"
    echo "   - Open Microsoft Store and search for 'Python'"
    echo "   - Install the latest version"
    exit 1
fi

# Use py command since we confirmed it exists
py cmoney.py $@