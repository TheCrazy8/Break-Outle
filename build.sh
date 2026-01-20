#!/bin/bash
# Build script for Linux/Mac

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Building executable..."
python build.py

echo "Done! Executable is in the dist/ directory"
