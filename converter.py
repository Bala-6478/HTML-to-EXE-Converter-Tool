"""
HTML to EXE Converter
Developed by BALAVIGNESH A

Entry point — launches the GUI converter.
Run:  python converter.py
"""

import sys
import os
import subprocess
from pathlib import Path


def check_and_install(package, import_name=None):
    imp = import_name or package
    try:
        __import__(imp)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.run([sys.executable, "-m", "pip", "install", package, "--quiet"],
                       check=True)


def main():
    # Auto-install tkinter is usually built-in; just ensure it exists
    try:
        import tkinter
    except ImportError:
        print("ERROR: tkinter is not available. Please install Python with Tk support.")
        sys.exit(1)

    # Change working dir to script location so relative paths work
    os.chdir(Path(__file__).parent)

    # Ensure logs dir exists
    Path("logs").mkdir(exist_ok=True)

    import tkinter as tk
    from gui import ConverterGUI

    root = tk.Tk()
    app = ConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
