@echo off
title HTML TO EXE CONVERTER - Developed by BALAVIGNESH A
color 0B

echo.
echo  =========================================================
echo    HTML TO EXE CONVERTER  ^|  Developed by BALAVIGNESH A
echo  =========================================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python is not installed or not in PATH.
    echo  Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo  [*] Python found.

:: Install dependencies silently
echo  [*] Checking dependencies...
python -m pip install pywebview pyinstaller --quiet --upgrade 2>nul
echo  [*] Dependencies ready.
echo.

:: Launch GUI
echo  [*] Launching HTML to EXE Converter...
python converter.py

pause
