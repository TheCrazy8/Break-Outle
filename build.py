"""
Build script for creating executables with PyInstaller
"""
import PyInstaller.__main__
import sys
import os

def build():
    """Build the executable using PyInstaller"""
    
    # PyInstaller options
    options = [
        'main.py',  # Main script
        '--name=Break-Outle',  # Name of the executable
        '--onefile',  # Create a single executable file
        '--windowed',  # Don't show console window (GUI app)
        '--icon=NONE',  # No icon for now
        '--clean',  # Clean PyInstaller cache before building
        '--noconfirm',  # Replace output directory without asking
        # Add game package
        '--add-data=game:game',
        # Optimize
        '--optimize=2',
    ]
    
    print("Building Break-Outle executable...")
    print(f"Platform: {sys.platform}")
    print(f"Python version: {sys.version}")
    print("-" * 50)
    
    try:
        PyInstaller.__main__.run(options)
        print("-" * 50)
        print("Build completed successfully!")
        print(f"Executable location: dist/Break-Outle{'.exe' if sys.platform == 'win32' else ''}")
        return True
    except Exception as e:
        print(f"Build failed: {e}")
        return False

if __name__ == "__main__":
    success = build()
    sys.exit(0 if success else 1)
