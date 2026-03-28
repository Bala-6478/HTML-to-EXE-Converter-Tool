# =============================================================================
#  FILE        : build_cli.py
#  DESCRIPTION : CLI Mode — Build HTML to EXE from the command line
#  AUTHOR      : BEST_TEAM
#  VERSION     : 3.0
#  PLATFORM    : Windows 10 / 11
#  PYTHON      : 3.8+
#
#  USAGE:
#    python build_cli.py input/index.html
#    python build_cli.py input/index.html --name MyApp --width 1280 --height 720
#    python build_cli.py input/index.html --name MyApp --icon app.ico --fullscreen
#    python build_cli.py input/index.html --name MyApp --no-resize
# =============================================================================

# ─────────────────────────────────────────────────────────────────────────────
#  IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
import argparse
import os
import sys
import shutil
import subprocess
import textwrap

# ─────────────────────────────────────────────────────────────────────────────
#  APP INFO
# ─────────────────────────────────────────────────────────────────────────────
APP_NAME    = "HTML TO EXE CONVERTER"
APP_AUTHOR  = "BEST_TEAM"
APP_VERSION = "v3.0"

# ─────────────────────────────────────────────────────────────────────────────
#  TERMINAL COLORS  (ANSI)
# ─────────────────────────────────────────────────────────────────────────────
CY  = "\033[96m"    # cyan
GR  = "\033[92m"    # green
YL  = "\033[93m"    # yellow
RD  = "\033[91m"    # red
WH  = "\033[97m"    # white
DIM = "\033[90m"    # dim / grey
BLD = "\033[1m"     # bold
RST = "\033[0m"     # reset

def colored(color, text):
    return f"{color}{text}{RST}"

# ─────────────────────────────────────────────────────────────────────────────
#  LAUNCHER TEMPLATE
#  Generated and passed to PyInstaller — becomes the .exe entrypoint
# ─────────────────────────────────────────────────────────────────────────────
LAUNCHER_TEMPLATE = '''\
# ================================================================
#  HTML TO EXE CONVERTER — Auto-generated Launcher
#  Developed by BEST_TEAM  ·  v2.0
#  DO NOT EDIT — this file is generated automatically
# ================================================================
import sys
import os
import webview

def resource_path(relative_path):
    """
    Resolve embedded file path.
    Works both as plain .py and as a PyInstaller frozen .exe.
    """
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative_path)

html_file = resource_path("{html_filename}")
app_url   = "file:///" + html_file.replace("\\\\", "/")

webview.create_window(
    title      = "{app_name}",
    url        = app_url,
    width      = {width},
    height     = {height},
    resizable  = {resizable},
    fullscreen = {fullscreen},
    min_size   = (400, 300),
)
webview.start(debug=False)
'''

# ─────────────────────────────────────────────────────────────────────────────
#  BANNER
# ─────────────────────────────────────────────────────────────────────────────
def print_banner():
    print(f"""
{CY}{BLD}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║      ⚡  HTML TO EXE CONVERTER  ·  CLI  ·  v3.0         ║
║                                                         ║
║              Developed by  BEST_TEAM                     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{RST}
""")

# ─────────────────────────────────────────────────────────────────────────────
#  LOG HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def log_ok(msg):
    print(f"  {DIM}[{RST}{GR}{BLD} OK {RST}{DIM}]{RST}  {msg}")

def log_err(msg):
    print(f"  {DIM}[{RST}{RD}{BLD}FAIL{RST}{DIM}]{RST}  {msg}")

def log_info(msg):
    print(f"  {DIM}[{RST}{CY}{BLD}INFO{RST}{DIM}]{RST}  {msg}")

def log_warn(msg):
    print(f"  {DIM}[{RST}{YL}{BLD}WARN{RST}{DIM}]{RST}  {msg}")

def log_step(n, total, msg):
    print(f"\n{BLD}[{n}/{total}]  {msg}{RST}")

# ─────────────────────────────────────────────────────────────────────────────
#  DEPENDENCY INSTALLER
# ─────────────────────────────────────────────────────────────────────────────
def pip_install(package):
    log_warn(f"Installing {package}...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", package, "--quiet"],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        log_ok(f"{package} installed.")
    else:
        log_err(f"Failed to install {package}.")
        print(result.stderr)
        sys.exit(1)

def ensure_dependencies():
    try:
        import webview      # noqa: F401
        log_ok("pywebview  ready.")
    except ImportError:
        pip_install("pywebview")

    try:
        import PyInstaller  # noqa: F401
        log_ok("pyinstaller ready.")
    except ImportError:
        pip_install("pyinstaller")

# ─────────────────────────────────────────────────────────────────────────────
#  BUILD FUNCTION
# ─────────────────────────────────────────────────────────────────────────────
def build(html_path, app_name, width, height,
          icon_path, fullscreen, resizable):
    """
    Full CLI build pipeline.
    Converts an HTML file into a standalone Windows .exe using
    pywebview (browser engine) and PyInstaller (packager).
    """

    print_banner()

    # ── Config Summary ────────────────────────────────────────────────────
    print(f"  {DIM}{'─' * 54}{RST}")
    log_info(f"Input    :  {html_path}")
    log_info(f"App name :  {app_name}")
    log_info(f"Size     :  {width} × {height}  px")
    log_info(f"Icon     :  {icon_path if icon_path else '(default)'}")
    log_info(f"Options  :  fullscreen={fullscreen}  resizable={resizable}")
    print(f"  {DIM}{'─' * 54}{RST}\n")

    # ── Step 1 — Validate ─────────────────────────────────────────────────
    log_step(1, 4, "Validating input...")
    if not os.path.isfile(html_path):
        log_err(f"File not found:  {html_path}")
        sys.exit(1)

    html_path     = os.path.abspath(html_path)
    html_filename = os.path.basename(html_path)
    html_src_dir  = os.path.dirname(html_path)
    script_dir    = os.path.dirname(os.path.abspath(__file__))
    log_ok(f"Found:  {html_filename}")

    # ── Step 2 — Dependencies ─────────────────────────────────────────────
    log_step(2, 4, "Checking dependencies...")
    ensure_dependencies()

    # ── Step 3 — Copy Files ───────────────────────────────────────────────
    log_step(3, 4, "Preparing build directory...")

    build_dir = os.path.join(script_dir, "_build_tmp")
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.makedirs(build_dir)

    # Copy HTML
    html_dst = os.path.join(build_dir, html_filename)
    shutil.copy2(html_path, html_dst)
    log_ok(f"Copied  {html_filename}")

    # Copy asset folders
    ASSET_FOLDERS = [
        "css", "js", "assets", "images", "img",
        "fonts", "media", "static", "lib", "libs",
    ]
    extra_data = []
    for folder in ASSET_FOLDERS:
        src = os.path.join(html_src_dir, folder)
        if os.path.isdir(src):
            dst = os.path.join(build_dir, folder)
            shutil.copytree(src, dst)
            extra_data.append((dst, folder))
            log_ok(f"Copied  {folder}/")

    # Write launcher
    launcher_code = LAUNCHER_TEMPLATE.format(
        html_filename = html_filename,
        app_name      = app_name,
        width         = width,
        height        = height,
        resizable     = resizable,
        fullscreen    = fullscreen,
    )
    launcher_path = os.path.join(build_dir, f"_{app_name}_launcher.py")
    with open(launcher_path, "w", encoding="utf-8") as f:
        f.write(launcher_code)
    log_ok(f"Launcher  _{app_name}_launcher.py  written")

    # ── Step 4 — PyInstaller ──────────────────────────────────────────────
    log_step(4, 4, "Running PyInstaller  (1–3 minutes)...")
    print()

    dist_dir = os.path.join(script_dir, "dist")
    work_dir = os.path.join(build_dir,  "work")
    os.makedirs(dist_dir, exist_ok=True)

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        f"--name={app_name}",
        f"--distpath={dist_dir}",
        f"--workpath={work_dir}",
        f"--specpath={build_dir}",
        f"--add-data={html_dst}{os.pathsep}.",
        "--hidden-import=webview",
        "--hidden-import=webview.platforms.winforms",
        "--collect-submodules=webview",
    ]

    for (src_folder, folder_name) in extra_data:
        cmd.append(f"--add-data={src_folder}{os.pathsep}{folder_name}")

    if icon_path and os.path.isfile(icon_path):
        cmd.append(f"--icon={icon_path}")

    cmd.append(launcher_path)

    result = subprocess.run(cmd)

    # ── Result ────────────────────────────────────────────────────────────
    exe_path = os.path.join(dist_dir, f"{app_name}.exe")
    print(f"\n  {DIM}{'─' * 54}{RST}")

    if result.returncode == 0 and os.path.isfile(exe_path):
        print(f"  {GR}{BLD}[ ✓  BUILD SUCCESSFUL ]{RST}")
        log_ok(f"Output  ›  {exe_path}")
        print(f"  {DIM}{'─' * 54}{RST}")
        print(f"\n  Double-click  {CY}{BLD}{app_name}.exe{RST}  to launch your app!")
        print(f"  {DIM}Developed by {APP_AUTHOR}  ·  {APP_VERSION}{RST}\n")
    else:
        print(f"  {RD}{BLD}[ ✗  BUILD FAILED ]{RST}")
        log_warn("Run  python setup.py  first")
        log_warn("Or:  pip install pywebview pyinstaller")
        print(f"  {DIM}{'─' * 54}{RST}\n")
        sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
#  ARGUMENT PARSER
# ─────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        prog="build_cli.py",
        description=f"{APP_NAME} — CLI — {APP_AUTHOR} {APP_VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(f"""\
        Examples:
          python build_cli.py input/index.html
          python build_cli.py input/index.html --name Calculator --width 800 --height 600
          python build_cli.py input/index.html --name MyApp --icon app.ico --fullscreen
          python build_cli.py input/index.html --name MyApp --no-resize

        Developed by {APP_AUTHOR}  ·  {APP_VERSION}
        """),
    )

    parser.add_argument("html",
        help="Path to your HTML file  (e.g. input/index.html)")
    parser.add_argument("--name",       default="MyApp",
        help="Output EXE name  (default: MyApp)")
    parser.add_argument("--width",      default=1280, type=int,
        help="Window width in pixels  (default: 1280)")
    parser.add_argument("--height",     default=720,  type=int,
        help="Window height in pixels  (default: 720)")
    parser.add_argument("--icon",       default="",
        help="Path to .ico icon file  (optional)")
    parser.add_argument("--fullscreen", action="store_true",
        help="Launch in fullscreen mode")
    parser.add_argument("--no-resize",  action="store_true",
        help="Disable window resizing")

    args = parser.parse_args()

    build(
        html_path  = args.html,
        app_name   = args.name.replace(" ", "_"),
        width      = args.width,
        height     = args.height,
        icon_path  = args.icon,
        fullscreen = args.fullscreen,
        resizable  = not args.no_resize,
    )

# ─────────────────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
