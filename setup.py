# =============================================================================
#  FILE        : setup.py
#  DESCRIPTION : First-time setup — installs all dependencies
#  AUTHOR      : BEST_TEAM
#  VERSION     : 3.0
#  USAGE       : python setup.py
# =============================================================================

# ─────────────────────────────────────────────────────────────────────────────
#  IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
import subprocess
import sys
import os

# ─────────────────────────────────────────────────────────────────────────────
#  APP INFO
# ─────────────────────────────────────────────────────────────────────────────
APP_NAME    = "HTML TO EXE CONVERTER"
APP_AUTHOR  = "BEST_TEAM"
APP_VERSION = "v2.0"

# ─────────────────────────────────────────────────────────────────────────────
#  TERMINAL COLORS
# ─────────────────────────────────────────────────────────────────────────────
CY  = "\033[96m"
GR  = "\033[92m"
YL  = "\033[93m"
RD  = "\033[91m"
WH  = "\033[97m"
DIM = "\033[90m"
BLD = "\033[1m"
RST = "\033[0m"

# ─────────────────────────────────────────────────────────────────────────────
#  REQUIRED DEPENDENCIES
# ─────────────────────────────────────────────────────────────────────────────
DEPENDENCIES = [
    ("webview",       "pywebview"),    # (import_name, pip_name)
    ("PyInstaller",   "pyinstaller"),
]

# ─────────────────────────────────────────────────────────────────────────────
#  REQUIRED FOLDERS
# ─────────────────────────────────────────────────────────────────────────────
REQUIRED_FOLDERS = ["input", "dist"]

# ─────────────────────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def log_ok(msg):    print(f"  {DIM}[{RST}{GR}{BLD} OK {RST}{DIM}]{RST}  {msg}")
def log_err(msg):   print(f"  {DIM}[{RST}{RD}{BLD}FAIL{RST}{DIM}]{RST}  {msg}")
def log_info(msg):  print(f"  {DIM}[{RST}{CY}{BLD}INFO{RST}{DIM}]{RST}  {msg}")
def log_warn(msg):  print(f"  {DIM}[{RST}{YL}{BLD}WARN{RST}{DIM}]{RST}  {msg}")

# ─────────────────────────────────────────────────────────────────────────────
#  MAIN SETUP
# ─────────────────────────────────────────────────────────────────────────────
def main():

    # ── Banner ────────────────────────────────────────────────────────────
    print(f"""
{CY}{BLD}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║      ⚡  HTML TO EXE CONVERTER  ·  SETUP  ·  v2.0       ║
║                                                          ║
║              Developed by  BEST_TEAM                     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{RST}
""")

    # ── Python Version Check ──────────────────────────────────────────────
    print(f"{BLD}Checking Python version...{RST}")
    maj, mn = sys.version_info.major, sys.version_info.minor
    if maj < 3 or (maj == 3 and mn < 8):
        log_err(f"Python 3.8+ required. Found: {maj}.{mn}")
        log_info("Download: https://www.python.org/downloads/")
        sys.exit(1)
    log_ok(f"Python {maj}.{mn}  ✓")

    # ── Install Dependencies ──────────────────────────────────────────────
    print(f"\n{BLD}Installing dependencies...{RST}")
    for import_name, pip_name in DEPENDENCIES:
        try:
            __import__(import_name)
            log_ok(f"{pip_name}  already installed.")
        except ImportError:
            log_warn(f"Installing {pip_name}...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", pip_name, "--quiet"],
                capture_output=True, text=True,
            )
            if result.returncode == 0:
                log_ok(f"{pip_name}  installed  ✓")
            else:
                log_err(f"Failed to install {pip_name}.")
                print(f"  {RD}{result.stderr.strip()}{RST}")
                sys.exit(1)

    # ── Create Folders ────────────────────────────────────────────────────
    print(f"\n{BLD}Creating project folders...{RST}")
    for folder in REQUIRED_FOLDERS:
        if not os.path.exists(folder):
            os.makedirs(folder)
            log_ok(f"Created  {folder}/")
        else:
            log_ok(f"{folder}/  exists.")

    # ── Done ──────────────────────────────────────────────────────────────
    print(f"""
  {DIM}{'─' * 54}{RST}
  {GR}{BLD}[ ✓  SETUP COMPLETE ]{RST}

  You can now run the converter:

    {CY}build.bat{RST}                              ← double-click  (GUI)
    {CY}python converter.py{RST}                   ← GUI mode
    {CY}python build_cli.py input/index.html{RST}  ← CLI mode

  {DIM}Developed by {APP_AUTHOR}  ·  {APP_VERSION}{RST}
""")

# ─────────────────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
