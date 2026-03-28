@echo off
:: =============================================================================
::  FILE        : build.bat
::  DESCRIPTION : Windows launcher — opens the HTML TO EXE CONVERTER GUI
::  AUTHOR      : BEST_TEAM
::  VERSION     : 3.0
::  USAGE       : Double-click this file to launch the converter
:: =============================================================================
chcp 65001 >nul 2>&1
color 0B
cls

echo.
echo  ╔══════════════════════════════════════════════════════════╗
echo  ║                                                          ║
echo  ║      ⚡  HTML TO EXE CONVERTER  ·  v3.0                 ║
echo  ║                                                          ║
echo  ║              Developed by  BEST_TEAM                     ║
echo  ║                                                          ║
echo  ╚══════════════════════════════════════════════════════════╝
echo.

:: ─────────────────────────────────────────────────────────────────────────────
::  CHECK PYTHON
:: ─────────────────────────────────────────────────────────────────────────────
where python >nul 2>&1
IF ERRORLEVEL 1 (
    echo  [ERROR]  Python not found on this system.
    echo.
    echo  Please install Python 3.8 or higher:
    echo  https://www.python.org/downloads/
    echo.
    echo  IMPORTANT: Check "Add Python to PATH" during install.
    echo.
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo  [OK]     Python %PYVER% found.

:: ─────────────────────────────────────────────────────────────────────────────
::  AUTO-INSTALL DEPENDENCIES
:: ─────────────────────────────────────────────────────────────────────────────
echo  [...]    Checking pywebview...
python -c "import webview" >nul 2>&1
IF ERRORLEVEL 1 (
    echo  [...]    Installing pywebview...
    python -m pip install pywebview --quiet
    IF ERRORLEVEL 1 (
        echo  [ERROR]  Failed to install pywebview.
        echo           Run manually: pip install pywebview
        pause
        exit /b 1
    )
    echo  [OK]     pywebview installed.
) ELSE (
    echo  [OK]     pywebview ready.
)

echo  [...]    Checking pyinstaller...
python -c "import PyInstaller" >nul 2>&1
IF ERRORLEVEL 1 (
    echo  [...]    Installing pyinstaller...
    python -m pip install pyinstaller --quiet
    IF ERRORLEVEL 1 (
        echo  [ERROR]  Failed to install pyinstaller.
        echo           Run manually: pip install pyinstaller
        pause
        exit /b 1
    )
    echo  [OK]     pyinstaller installed.
) ELSE (
    echo  [OK]     pyinstaller ready.
)

:: ─────────────────────────────────────────────────────────────────────────────
::  CREATE REQUIRED FOLDERS
:: ─────────────────────────────────────────────────────────────────────────────
IF NOT EXIST "input\" (
    mkdir input
    echo  [OK]     Created input\ folder.
    echo  [INFO]   Place your HTML file inside the input\ folder.
)
IF NOT EXIST "dist\" mkdir dist

:: ─────────────────────────────────────────────────────────────────────────────
::  LAUNCH GUI
:: ─────────────────────────────────────────────────────────────────────────────
echo.
echo  [START]  Launching HTML TO EXE CONVERTER GUI...
echo  [INFO]   Developed by BEST_TEAM  ·  v2.0
echo.

python converter.py

IF ERRORLEVEL 1 (
    echo.
    echo  [ERROR]  GUI failed to launch. Running diagnostics...
    echo.
    python -c "import webview; print('  pywebview   OK')" 2>&1
    python -c "import PyInstaller; print('  pyinstaller OK')" 2>&1
    echo.
    echo  If errors appear above, run:  python setup.py
    echo.
    pause
)
