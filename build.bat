@echo off
REM Build script for Windows

echo Installing dependencies...
pip install -r requirements.txt

echo Building executable...
python build.py

echo Done! Executable is in the dist\ directory
pause
