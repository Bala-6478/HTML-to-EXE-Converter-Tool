# =============================================================================
#
#   ██╗  ██╗████████╗███╗   ███╗██╗         ████████╗ ██████╗
#   ██║  ██║╚══██╔══╝████╗ ████║██║         ╚══██╔══╝██╔═══██╗
#   ███████║   ██║   ██╔████╔██║██║            ██║   ██║   ██║
#   ██╔══██║   ██║   ██║╚██╔╝██║██║            ██║   ██║   ██║
#   ██║  ██║   ██║   ██║ ╚═╝ ██║███████╗       ██║   ╚██████╔╝
#   ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝╚══════╝       ╚═╝    ╚═════╝
#
#   ███████╗██╗  ██╗███████╗     ██████╗ ██████╗ ███╗   ██╗██╗   ██╗███████╗██████╗ ████████╗███████╗██████╗
#   ██╔════╝╚██╗██╔╝██╔════╝    ██╔════╝██╔═══██╗████╗  ██║██║   ██║██╔════╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
#   █████╗   ╚███╔╝ █████╗      ██║     ██║   ██║██╔██╗ ██║██║   ██║█████╗  ██████╔╝   ██║   █████╗  ██████╔╝
#   ██╔══╝   ██╔██╗ ██╔══╝      ██║     ██║   ██║██║╚██╗██║╚██╗ ██╔╝██╔══╝  ██╔══██╗   ██║   ██╔══╝  ██╔══██╗
#   ███████╗██╔╝ ██╗███████╗    ╚██████╗╚██████╔╝██║ ╚████║ ╚████╔╝ ███████╗██║  ██║   ██║   ███████╗██║  ██║
#   ╚══════╝╚═╝  ╚═╝╚══════╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
#
# =============================================================================
#  FILE        : converter.py
#  DESCRIPTION : GUI application — Convert HTML projects to Windows .exe
#  AUTHOR      : BEST_TEAM
#  VERSION     : 2.0
#  PLATFORM    : Windows 10 / 11
#  PYTHON      : 3.8+
#  USAGE       : python converter.py
# =============================================================================

# ─────────────────────────────────────────────────────────────────────────────
#  IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import subprocess
import sys
import os
import shutil

# ─────────────────────────────────────────────────────────────────────────────
#  APP INFO
# ─────────────────────────────────────────────────────────────────────────────
APP_NAME    = "HTML TO EXE CONVERTER"
APP_AUTHOR  = "BEST_TEAM"
APP_VERSION = "v2.0"
APP_TITLE   = f"{APP_NAME}  ·  {APP_AUTHOR}  ·  {APP_VERSION}"

# ─────────────────────────────────────────────────────────────────────────────
#  THEME — Colors
# ─────────────────────────────────────────────────────────────────────────────
BG      = "#0d1117"   # main background
BG2     = "#161b22"   # header background
PANEL   = "#21262d"   # card / input background
BORDER  = "#30363d"   # border lines
ACCENT  = "#58a6ff"   # primary blue accent
GREEN   = "#3fb950"   # success green
ORANGE  = "#f78166"   # error / bottom stripe
YELLOW  = "#e3b341"   # warning
TEXT    = "#e6edf3"   # primary text
MUTED   = "#8b949e"   # secondary / muted text
WHITE   = "#ffffff"   # white

# ─────────────────────────────────────────────────────────────────────────────
#  THEME — Fonts
# ─────────────────────────────────────────────────────────────────────────────
MONO    = ("Courier New", 10)
MONO_SM = ("Courier New", 9)
MONO_MD = ("Courier New", 11, "bold")
MONO_LG = ("Courier New", 13, "bold")
MONO_XL = ("Courier New", 15, "bold")

# ─────────────────────────────────────────────────────────────────────────────
#  LAUNCHER TEMPLATE
#  This script is written to disk and wrapped by PyInstaller into the .exe.
#  It resolves the embedded HTML path and opens it in a pywebview window.
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
    Return the absolute path to a bundled resource.
    Works both when running as a plain .py and as a frozen .exe.
    """
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS          # PyInstaller extraction folder
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative_path)

# Resolve the HTML file and build a file:/// URL
html_file = resource_path("{html_filename}")
app_url   = "file:///" + html_file.replace("\\\\", "/")

# Launch the desktop window
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
#  DEPENDENCY MANAGEMENT
# ─────────────────────────────────────────────────────────────────────────────
def pip_install_quiet(package):
    """Install a pip package silently."""
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", package, "--quiet"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def ensure_dependencies():
    """Auto-install pywebview and pyinstaller if not already present."""
    try:
        import webview       # noqa: F401
    except ImportError:
        pip_install_quiet("pywebview")

    try:
        import PyInstaller   # noqa: F401
    except ImportError:
        pip_install_quiet("pyinstaller")

# ─────────────────────────────────────────────────────────────────────────────
#  BUILD ENGINE  (runs in background thread)
# ─────────────────────────────────────────────────────────────────────────────
def run_build(html_path, app_name, width, height,
              icon_path, fullscreen, resizable, log_cb, done_cb):
    """
    Full build pipeline:
      1. Validate the HTML input file
      2. Ensure dependencies are installed
      3. Copy HTML + adjacent asset folders to a temp build directory
      4. Write the pywebview launcher script
      5. Run PyInstaller to produce a single .exe
      6. Report success or failure via callbacks
    """
    try:
        # ── Build Header ──────────────────────────────────────────────────
        log_cb("\n")
        log_cb("=" * 58 + "\n")
        log_cb(f"  {APP_NAME}\n")
        log_cb(f"  Developed by {APP_AUTHOR}  ·  {APP_VERSION}\n")
        log_cb("=" * 58 + "\n")
        log_cb(f"\n  Target  ›  {app_name}.exe\n\n")

        # ── 1. Validate ───────────────────────────────────────────────────
        if not os.path.isfile(html_path):
            log_cb(f"[ERROR]  HTML file not found:\n         {html_path}\n")
            done_cb(False)
            return

        html_path     = os.path.abspath(html_path)
        html_filename = os.path.basename(html_path)
        html_src_dir  = os.path.dirname(html_path)
        script_dir    = os.path.dirname(os.path.abspath(__file__))

        # ── 2. Dependencies ───────────────────────────────────────────────
        log_cb("[1/4]  Checking dependencies...\n")
        ensure_dependencies()
        log_cb("       pywebview     ✓\n")
        log_cb("       pyinstaller   ✓\n\n")

        # ── 3. Prepare build directory ────────────────────────────────────
        log_cb("[2/4]  Preparing build directory...\n")

        build_dir = os.path.join(script_dir, "_build_tmp")
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)
        os.makedirs(build_dir)

        # Copy the HTML file
        html_dst = os.path.join(build_dir, html_filename)
        shutil.copy2(html_path, html_dst)
        log_cb(f"       Copied  {html_filename}\n")

        # Copy common asset folders that sit next to the HTML file
        ASSET_FOLDERS = [
            "css", "js", "assets", "images", "img",
            "fonts", "media", "static", "lib", "libs",
        ]
        extra_data_args = []
        for folder in ASSET_FOLDERS:
            src = os.path.join(html_src_dir, folder)
            if os.path.isdir(src):
                dst = os.path.join(build_dir, folder)
                shutil.copytree(src, dst)
                extra_data_args.append((dst, folder))
                log_cb(f"       Copied  {folder}/\n")

        log_cb("\n")

        # ── 4. Write launcher script ──────────────────────────────────────
        log_cb("[3/4]  Writing launcher script...\n")

        launcher_code = LAUNCHER_TEMPLATE.format(
            html_filename = html_filename,
            app_name      = app_name,
            width         = int(width),
            height        = int(height),
            resizable     = resizable,
            fullscreen    = fullscreen,
        )
        launcher_path = os.path.join(build_dir, f"_{app_name}_launcher.py")
        with open(launcher_path, "w", encoding="utf-8") as f:
            f.write(launcher_code)
        log_cb(f"       _{app_name}_launcher.py  ✓\n\n")

        # ── 5. Run PyInstaller ────────────────────────────────────────────
        log_cb("[4/4]  Running PyInstaller  (1–3 minutes)...\n\n")

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
            f"--add-data={html_dst}{os.pathsep}.",     # embed HTML at root
            "--hidden-import=webview",
            "--hidden-import=webview.platforms.winforms",
            "--collect-submodules=webview",
        ]

        # Embed each asset folder
        for (src_folder, folder_name) in extra_data_args:
            cmd.append(f"--add-data={src_folder}{os.pathsep}{folder_name}")

        # Optional custom icon
        if icon_path and os.path.isfile(icon_path):
            cmd.append(f"--icon={icon_path}")

        cmd.append(launcher_path)

        # Stream PyInstaller stdout to the log in real time
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            creationflags=(subprocess.CREATE_NO_WINDOW
                           if sys.platform == "win32" else 0),
        )
        for line in proc.stdout:
            log_cb(line)
        proc.wait()

        # ── 6. Result ─────────────────────────────────────────────────────
        exe_path = os.path.join(dist_dir, f"{app_name}.exe")
        log_cb("\n" + "=" * 58 + "\n")

        if proc.returncode == 0 and os.path.isfile(exe_path):
            log_cb(f"  BUILD SUCCESSFUL  ✓\n")
            log_cb(f"  OUTPUT  ›  {exe_path}\n")
            log_cb("=" * 58 + "\n")
            log_cb(f"\n  Developed by {APP_AUTHOR}  ·  {APP_VERSION}\n\n")
            done_cb(True, exe_path)
        else:
            log_cb(f"  BUILD FAILED  ✗\n")
            log_cb("  Check the log above for error details.\n")
            log_cb("=" * 58 + "\n")
            done_cb(False)

    except Exception as exc:
        import traceback
        log_cb(f"\n[EXCEPTION]  {exc}\n")
        log_cb(traceback.format_exc())
        done_cb(False)

# ─────────────────────────────────────────────────────────────────────────────
#  MAIN WINDOW
# ─────────────────────────────────────────────────────────────────────────────
class HTMLtoEXEApp(tk.Tk):
    """
    HTML TO EXE CONVERTER — Main GUI Window
    Developed by BEST_TEAM
    """

    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("880x750")
        self.minsize(720, 640)
        self.configure(bg=BG)
        self._building = False
        self._init_variables()
        self._build_ui()

    # ─────────────────────────────────────────────────────────────────────
    #  Variables
    # ─────────────────────────────────────────────────────────────────────
    def _init_variables(self):
        self.var_html       = tk.StringVar()
        self.var_icon       = tk.StringVar()
        self.var_name       = tk.StringVar(value="MyApp")
        self.var_width      = tk.StringVar(value="1280")
        self.var_height     = tk.StringVar(value="720")
        self.var_fullscreen = tk.BooleanVar(value=False)
        self.var_resizable  = tk.BooleanVar(value=True)

    # ─────────────────────────────────────────────────────────────────────
    #  Build the full UI
    # ─────────────────────────────────────────────────────────────────────
    def _build_ui(self):

        # ── Top stripe ───────────────────────────────────────────────────
        tk.Frame(self, bg=ACCENT, height=4).pack(fill="x", side="top")

        # ── Header ───────────────────────────────────────────────────────
        hdr = tk.Frame(self, bg=BG2, pady=18)
        hdr.pack(fill="x")
        tk.Label(hdr, text="⚡  HTML  →  EXE  CONVERTER",
                 font=MONO_XL, bg=BG2, fg=ACCENT).pack()
        tk.Label(hdr,
                 text=f"Developed by {APP_AUTHOR}  ·  {APP_VERSION}  ·  Windows Desktop App Builder",
                 font=MONO_SM, bg=BG2, fg=MUTED).pack(pady=(5, 0))

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        # ── Body ──────────────────────────────────────────────────────────
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=32, pady=22)

        # ┌─ SECTION 01 — Input File ────────────────────────────────────┐
        self._section(body, "01  ·  INPUT HTML FILE")
        r = tk.Frame(body, bg=BG)
        r.pack(fill="x", pady=(4, 16))
        self._entry(r, self.var_html, ACCENT).pack(
            side="left", fill="x", expand=True, ipady=9, ipadx=10)
        self._btn(r, "  BROWSE  ", self._pick_html, ACCENT, BG).pack(
            side="left", padx=(8, 0))

        # ┌─ SECTION 02 — App Settings ──────────────────────────────────┐
        self._section(body, "02  ·  APP SETTINGS")
        g = tk.Frame(body, bg=BG)
        g.pack(fill="x", pady=(4, 4))
        g.columnconfigure(1, weight=3)
        g.columnconfigure(3, weight=1)
        g.columnconfigure(5, weight=1)

        #  Name  |  Width  |  Height
        self._lbl(g, "App Name",    0, 0)
        self._entry(g, self.var_name,   WHITE, w=22).grid(
            row=0, column=1, sticky="ew", padx=(4,20), pady=5, ipady=7)
        self._lbl(g, "Width (px)",  0, 2)
        self._entry(g, self.var_width,  WHITE, w=8).grid(
            row=0, column=3, sticky="ew", padx=(4,20), pady=5, ipady=7)
        self._lbl(g, "Height (px)", 0, 4)
        self._entry(g, self.var_height, WHITE, w=8).grid(
            row=0, column=5, sticky="ew", padx=(4,0),  pady=5, ipady=7)

        #  Icon
        self._lbl(g, "Icon (.ico)", 1, 0)
        icon_row = tk.Frame(g, bg=BG)
        icon_row.grid(row=1, column=1, columnspan=5, sticky="ew", pady=6)
        self._entry(icon_row, self.var_icon, MUTED).pack(
            side="left", fill="x", expand=True, ipady=7, ipadx=10)
        self._btn(icon_row, "  BROWSE  ", self._pick_icon, PANEL, MUTED).pack(
            side="left", padx=(8, 0))

        #  Checkboxes
        cb = tk.Frame(body, bg=BG)
        cb.pack(fill="x", pady=(10, 16))
        self._chk(cb, "Fullscreen Mode",  self.var_fullscreen)
        self._chk(cb, "Resizable Window", self.var_resizable)

        # ┌─ SECTION 03 — Output ────────────────────────────────────────┐
        self._section(body, "03  ·  OUTPUT")
        out = tk.Frame(body, bg=PANEL, padx=16, pady=13)
        out.pack(fill="x", pady=(4, 18))
        tk.Label(out, text="dist/",
                 font=MONO_MD, bg=PANEL, fg=GREEN).pack(side="left")
        tk.Label(out,
                 text="  ←  your  .exe  will be saved here after build",
                 font=MONO_SM, bg=PANEL, fg=MUTED).pack(side="left")

        # ── Action Buttons ─────────────────────────────────────────────
        br = tk.Frame(body, bg=BG)
        br.pack(fill="x", pady=(0, 10))

        self.btn_build = self._btn(
            br, "▶   BUILD EXE", self._start_build,
            ACCENT, BG, font=MONO_LG, px=36, py=14)
        self.btn_build.pack(side="left", fill="x", expand=True)

        self._btn(br, "  📂 Open dist/  ", self._open_dist,
                  PANEL, MUTED, px=14, py=14).pack(side="left", padx=(8, 0))
        self._btn(br, "  ✕ Clear Log  ",  self._clear_log,
                  PANEL, MUTED, px=14, py=14).pack(side="left", padx=(6, 0))

        # ── Progress Bar ───────────────────────────────────────────────
        s = ttk.Style()
        s.theme_use("default")
        s.configure("BT.Horizontal.TProgressbar",
                    troughcolor=PANEL, background=ACCENT,
                    thickness=4, borderwidth=0)
        self.progress = ttk.Progressbar(
            body, style="BT.Horizontal.TProgressbar", mode="indeterminate")
        self.progress.pack(fill="x", pady=(0, 12))

        # ┌─ SECTION 04 — Log ───────────────────────────────────────────┐
        self._section(body, "04  ·  BUILD LOG")
        self.log = scrolledtext.ScrolledText(
            body, font=("Courier New", 9),
            bg="#010409", fg=GREEN, insertbackground=GREEN,
            relief="flat", bd=0,
            highlightthickness=1, highlightbackground=BORDER,
            state="disabled", height=13)
        self.log.pack(fill="both", expand=True, pady=(4, 0))
        self.log.tag_config("ok",     foreground=GREEN)
        self.log.tag_config("err",    foreground=ORANGE)
        self.log.tag_config("hdr",    foreground=ACCENT)
        self.log.tag_config("muted",  foreground=MUTED)

        # Welcome message in log
        self._log(
            f"  {APP_NAME}\n"
            f"  Developed by {APP_AUTHOR}  ·  {APP_VERSION}\n"
            f"  {'─' * 50}\n"
            f"  Ready. Select an HTML file and click  ▶ BUILD EXE.\n\n",
            tag="hdr")

        # ── Bottom stripe ──────────────────────────────────────────────
        tk.Frame(self, bg=ORANGE, height=4).pack(fill="x", side="bottom")

    # ─────────────────────────────────────────────────────────────────────
    #  Widget Helpers
    # ─────────────────────────────────────────────────────────────────────
    def _section(self, parent, title):
        f = tk.Frame(parent, bg=BG)
        f.pack(fill="x", pady=(8, 4))
        tk.Label(f, text=f"  {title}",
                 font=("Courier New", 9, "bold"), bg=BG, fg=ACCENT).pack(side="left")
        tk.Frame(f, bg=BORDER, height=1).pack(
            side="left", fill="x", expand=True, padx=(12, 0), pady=5)

    def _lbl(self, parent, text, row, col):
        tk.Label(parent, text=text, font=MONO_SM,
                 bg=BG, fg=MUTED).grid(row=row, column=col,
                                        sticky="w", padx=(0, 4), pady=5)

    def _entry(self, parent, var, fg, w=None):
        kw = dict(textvariable=var, font=MONO,
                  bg=PANEL, fg=fg, insertbackground=fg,
                  relief="flat", bd=0,
                  highlightthickness=1,
                  highlightbackground=BORDER,
                  highlightcolor=ACCENT)
        if w:
            kw["width"] = w
        return tk.Entry(parent, **kw)

    def _btn(self, parent, text, cmd, bg, fg,
             font=None, px=12, py=9):
        return tk.Button(parent, text=text, command=cmd,
                         font=font or MONO_SM,
                         bg=bg, fg=fg,
                         activebackground=BORDER, activeforeground=WHITE,
                         relief="flat", bd=0, cursor="hand2",
                         padx=px, pady=py)

    def _chk(self, parent, label, var):
        tk.Checkbutton(parent, text=f"  {label}", variable=var,
                       font=MONO_SM, bg=BG, fg=TEXT,
                       selectcolor=PANEL,
                       activebackground=BG, activeforeground=ACCENT,
                       cursor="hand2").pack(side="left", padx=(0, 24))

    # ─────────────────────────────────────────────────────────────────────
    #  File Pickers
    # ─────────────────────────────────────────────────────────────────────
    def _pick_html(self):
        p = filedialog.askopenfilename(
            title="Select HTML file",
            filetypes=[("HTML Files", "*.html *.htm"), ("All Files", "*.*")])
        if p:
            self.var_html.set(p)
            self._log(f"  [INPUT]   {p}\n")
            base = os.path.splitext(os.path.basename(p))[0]
            if self.var_name.get() == "MyApp":
                self.var_name.set(base.replace(" ", "_"))

    def _pick_icon(self):
        p = filedialog.askopenfilename(
            title="Select icon file (.ico)",
            filetypes=[("ICO Files", "*.ico"), ("All Files", "*.*")])
        if p:
            self.var_icon.set(p)
            self._log(f"  [ICON]    {p}\n")

    # ─────────────────────────────────────────────────────────────────────
    #  Log
    # ─────────────────────────────────────────────────────────────────────
    def _log(self, msg, tag=None):
        self.log.configure(state="normal")
        self.log.insert("end", msg, tag) if tag else self.log.insert("end", msg)
        self.log.see("end")
        self.log.configure(state="disabled")

    def _clear_log(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    # ─────────────────────────────────────────────────────────────────────
    #  Open dist/ folder
    # ─────────────────────────────────────────────────────────────────────
    def _open_dist(self):
        dist = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
        os.makedirs(dist, exist_ok=True)
        if sys.platform == "win32":
            os.startfile(dist)
        else:
            subprocess.Popen(["xdg-open", dist])

    # ─────────────────────────────────────────────────────────────────────
    #  Start Build
    # ─────────────────────────────────────────────────────────────────────
    def _start_build(self):
        if self._building:
            return

        html = self.var_html.get().strip()
        if not html or not os.path.isfile(html):
            messagebox.showerror("No HTML File",
                "Please select a valid HTML file first.\n\n"
                "Click BROWSE to choose your file.")
            return

        name = self.var_name.get().strip() or "MyApp"
        name = name.replace(" ", "_")

        try:
            width  = int(self.var_width.get())
            height = int(self.var_height.get())
        except ValueError:
            messagebox.showerror("Invalid Size",
                "Width and Height must be whole numbers.")
            return

        icon       = self.var_icon.get().strip()
        fullscreen = self.var_fullscreen.get()
        resizable  = self.var_resizable.get()

        self._building = True
        self.btn_build.configure(state="disabled",
                                 text="⏳   BUILDING…", bg=MUTED)
        self.progress.start(10)

        threading.Thread(
            target=run_build,
            args=(html, name, width, height, icon,
                  fullscreen, resizable,
                  self._t_log, self._t_done),
            daemon=True,
        ).start()

    # ─────────────────────────────────────────────────────────────────────
    #  Thread-safe Callbacks
    # ─────────────────────────────────────────────────────────────────────
    def _t_log(self, msg):
        tag = None
        m = msg.lower()
        if any(w in m for w in ("error", "failed", "exception", "✗")):
            tag = "err"
        elif any(w in m for w in ("success", "✓", "[ok]")):
            tag = "ok"
        self.after(0, lambda: self._log(msg, tag))

    def _t_done(self, success, exe_path=None):
        def _cb():
            self._building = False
            self.progress.stop()
            self.btn_build.configure(state="normal",
                                     text="▶   BUILD EXE", bg=ACCENT)
            if success:
                messagebox.showinfo("Build Successful  ✓",
                    f"Your EXE is ready!\n\n"
                    f"📁  {exe_path}\n\n"
                    f"Double-click it to launch your app.\n\n"
                    f"— {APP_AUTHOR}")
            else:
                messagebox.showerror("Build Failed  ✗",
                    "Build failed. Check the log for details.\n\n"
                    "Common fixes:\n"
                    "  • Run  python setup.py  first\n"
                    "  • Ensure your HTML file is valid\n"
                    "  • pip install pywebview pyinstaller\n\n"
                    f"— {APP_AUTHOR}")
        self.after(0, _cb)

# ─────────────────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = HTMLtoEXEApp()
    app.mainloop()
