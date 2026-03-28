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
#  DESCRIPTION : GUI — HTML to EXE Converter  (Two-column PC layout)
#  AUTHOR      : BEST_TEAM
#  VERSION     : 3.0
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
import json
import datetime

# ─────────────────────────────────────────────────────────────────────────────
#  APP INFO
# ─────────────────────────────────────────────────────────────────────────────
APP_NAME     = "HTML TO EXE CONVERTER"
APP_AUTHOR   = "BEST_TEAM"
APP_VERSION  = "v3.0"
APP_TITLE    = f"{APP_NAME}  ·  {APP_AUTHOR}  ·  {APP_VERSION}"
HISTORY_FILE = "build_history.json"

# ─────────────────────────────────────────────────────────────────────────────
#  THEME
# ─────────────────────────────────────────────────────────────────────────────
BG      = "#0d1117"
BG2     = "#161b22"
PANEL   = "#21262d"
PANEL2  = "#1c2128"
BORDER  = "#30363d"
ACCENT  = "#58a6ff"
GREEN   = "#3fb950"
ORANGE  = "#f78166"
YELLOW  = "#e3b341"
TEXT    = "#e6edf3"
MUTED   = "#8b949e"
WHITE   = "#ffffff"

MONO    = ("Courier New", 10)
MONO_SM = ("Courier New", 9)
MONO_MD = ("Courier New", 11, "bold")
MONO_LG = ("Courier New", 13, "bold")
MONO_XL = ("Courier New", 15, "bold")

# ─────────────────────────────────────────────────────────────────────────────
#  LAUNCHER TEMPLATE
# ─────────────────────────────────────────────────────────────────────────────
LAUNCHER_TEMPLATE = '''\
# ================================================================
#  HTML TO EXE CONVERTER — Auto-generated Launcher
#  Developed by BEST_TEAM  ·  v3.0
#  DO NOT EDIT — this file is generated automatically
# ================================================================
import sys, os, webview

def resource_path(rel):
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, rel)

html_file = resource_path("{html_filename}")
app_url   = "file:///" + html_file.replace("\\\\", "/")

webview.create_window(
    title            = "{app_name}",
    url              = app_url,
    width            = {width},
    height           = {height},
    resizable        = {resizable},
    fullscreen       = {fullscreen},
    min_size         = ({min_w}, {min_h}),
    background_color = "{bg_color}",
    on_top           = {on_top},
)
webview.start(debug=False)
'''

# ─────────────────────────────────────────────────────────────────────────────
#  DEPENDENCIES
# ─────────────────────────────────────────────────────────────────────────────
def pip_install_quiet(pkg):
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", pkg, "--quiet"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def ensure_dependencies():
    try:
        import webview       # noqa
    except ImportError:
        pip_install_quiet("pywebview")
    try:
        import PyInstaller   # noqa
    except ImportError:
        pip_install_quiet("pyinstaller")

# ─────────────────────────────────────────────────────────────────────────────
#  HISTORY
# ─────────────────────────────────────────────────────────────────────────────
def load_history():
    if os.path.isfile(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []

def save_history(records):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(records[-50:], f, indent=2)
    except Exception:
        pass

def add_history(record):
    records = load_history()
    records.append(record)
    save_history(records)

# ─────────────────────────────────────────────────────────────────────────────
#  BUILD ENGINE
# ─────────────────────────────────────────────────────────────────────────────
def run_build(params, log_cb, done_cb):
    html_path  = params["html_path"]
    app_name   = params["app_name"]
    width      = params["width"]
    height     = params["height"]
    min_w      = params["min_w"]
    min_h      = params["min_h"]
    icon_path  = params["icon_path"]
    out_dir    = params["out_dir"]
    fullscreen = params["fullscreen"]
    resizable  = params["resizable"]
    on_top     = params["on_top"]
    bg_color   = params["bg_color"]
    one_file   = params["one_file"]

    try:
        log_cb("\n" + "=" * 54 + "\n")
        log_cb(f"  {APP_NAME}  ·  {APP_AUTHOR}  ·  {APP_VERSION}\n")
        log_cb("=" * 54 + "\n")
        log_cb(f"\n  Target  ›  {app_name}.exe\n\n")

        if not os.path.isfile(html_path):
            log_cb(f"[ERROR]  File not found: {html_path}\n")
            done_cb(False, None); return

        html_path     = os.path.abspath(html_path)
        html_filename = os.path.basename(html_path)
        html_src_dir  = os.path.dirname(html_path)
        script_dir    = os.path.dirname(os.path.abspath(__file__))

        log_cb("[1/4]  Checking dependencies...\n")
        ensure_dependencies()
        log_cb("       pywebview     ✓\n")
        log_cb("       pyinstaller   ✓\n\n")

        log_cb("[2/4]  Preparing build directory...\n")
        build_dir = os.path.join(script_dir, "_build_tmp")
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)
        os.makedirs(build_dir)

        html_dst = os.path.join(build_dir, html_filename)
        shutil.copy2(html_path, html_dst)
        log_cb(f"       Copied  {html_filename}\n")

        ASSET_FOLDERS = ["css","js","assets","images","img",
                         "fonts","media","static","lib","libs"]
        extra_data_args = []
        for folder in ASSET_FOLDERS:
            src = os.path.join(html_src_dir, folder)
            if os.path.isdir(src):
                dst = os.path.join(build_dir, folder)
                shutil.copytree(src, dst)
                extra_data_args.append((dst, folder))
                log_cb(f"       Copied  {folder}/\n")
        log_cb("\n")

        log_cb("[3/4]  Writing launcher script...\n")
        launcher_code = LAUNCHER_TEMPLATE.format(
            html_filename=html_filename, app_name=app_name,
            width=int(width), height=int(height),
            min_w=int(min_w), min_h=int(min_h),
            resizable=resizable, fullscreen=fullscreen,
            on_top=on_top, bg_color=bg_color)
        launcher_path = os.path.join(build_dir, f"_{app_name}_launcher.py")
        with open(launcher_path, "w", encoding="utf-8") as f:
            f.write(launcher_code)
        log_cb(f"       _{app_name}_launcher.py  ✓\n\n")

        log_cb("[4/4]  Running PyInstaller  (1–3 minutes)...\n\n")
        dist_dir = out_dir if out_dir else os.path.join(script_dir, "dist")
        work_dir = os.path.join(build_dir, "work")
        os.makedirs(dist_dir, exist_ok=True)

        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--noconfirm", "--windowed",
            f"--name={app_name}",
            f"--distpath={dist_dir}",
            f"--workpath={work_dir}",
            f"--specpath={build_dir}",
            f"--add-data={html_dst}{os.pathsep}.",
            "--hidden-import=webview",
            "--hidden-import=webview.platforms.winforms",
            "--collect-submodules=webview",
            "--onefile" if one_file else "--onedir",
        ]
        for src_f, fn in extra_data_args:
            cmd.append(f"--add-data={src_f}{os.pathsep}{fn}")
        if icon_path and os.path.isfile(icon_path):
            cmd.append(f"--icon={icon_path}")
        cmd.append(launcher_path)

        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace",
            creationflags=(subprocess.CREATE_NO_WINDOW
                           if sys.platform == "win32" else 0))
        for line in proc.stdout:
            log_cb(line)
        proc.wait()

        exe_path = os.path.join(dist_dir, f"{app_name}.exe")
        log_cb("\n" + "=" * 54 + "\n")
        if proc.returncode == 0 and os.path.isfile(exe_path):
            log_cb("  BUILD SUCCESSFUL  ✓\n")
            log_cb(f"  OUTPUT  ›  {exe_path}\n")
            log_cb("=" * 54 + "\n")
            done_cb(True, exe_path)
        else:
            log_cb("  BUILD FAILED  ✗\n")
            log_cb("=" * 54 + "\n")
            done_cb(False, None)

    except Exception as exc:
        import traceback
        log_cb(f"\n[EXCEPTION]  {exc}\n{traceback.format_exc()}")
        done_cb(False, None)


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────────────────────────────────────
class HTMLtoEXEApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        # Start maximized for proper PC full-screen feel
        self.state("zoomed")
        self.minsize(1000, 680)
        self.configure(bg=BG)
        self._building = False
        self._init_vars()
        self._build_ui()

    # ─────────────────────────────────────────────────────────────────────
    #  Variables
    # ─────────────────────────────────────────────────────────────────────
    def _init_vars(self):
        self.var_html       = tk.StringVar()
        self.var_icon       = tk.StringVar()
        self.var_out_dir    = tk.StringVar()
        self.var_name       = tk.StringVar(value="MyApp")
        self.var_version    = tk.StringVar(value="1.0.0")
        self.var_author     = tk.StringVar(value="")
        self.var_width      = tk.StringVar(value="1280")
        self.var_height     = tk.StringVar(value="720")
        self.var_min_w      = tk.StringVar(value="400")
        self.var_min_h      = tk.StringVar(value="300")
        self.var_fullscreen = tk.BooleanVar(value=False)
        self.var_resizable  = tk.BooleanVar(value=True)
        self.var_on_top     = tk.BooleanVar(value=False)
        self.var_one_file   = tk.BooleanVar(value=True)
        self.var_bg_color   = tk.StringVar(value="#ffffff")

    # ─────────────────────────────────────────────────────────────────────
    #  Root UI shell
    # ─────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Top accent line
        tk.Frame(self, bg=ACCENT, height=4).pack(fill="x", side="top")

        # ── Header bar ────────────────────────────────────────────────────
        hdr = tk.Frame(self, bg=BG2, pady=14)
        hdr.pack(fill="x")

        # Left: title
        tk.Label(hdr, text="⚡  HTML  →  EXE  CONVERTER",
                 font=MONO_XL, bg=BG2, fg=ACCENT).pack(side="left", padx=24)

        # Right: author badge
        tk.Label(hdr,
                 text=f"{APP_AUTHOR}  ·  {APP_VERSION}  ·  Windows Desktop App Builder",
                 font=MONO_SM, bg=BG2, fg=MUTED).pack(side="right", padx=24)

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        # ── Tab bar ───────────────────────────────────────────────────────
        self._tabs  = {}
        self._pages = {}

        tab_bar = tk.Frame(self, bg=BG2)
        tab_bar.pack(fill="x")

        for icon_label, key in [
            ("🔨   BUILD",    "BUILD"),
            ("⚙️   SETUP",    "SETUP"),
            ("📋   HISTORY",  "HISTORY"),
        ]:
            btn = tk.Button(
                tab_bar, text=icon_label,
                font=("Courier New", 10, "bold"),
                bg=BG2, fg=MUTED,
                relief="flat", bd=0, cursor="hand2",
                padx=24, pady=11,
                command=lambda k=key: self._switch_tab(k))
            btn.pack(side="left")
            self._tabs[key] = btn

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        # ── Page container ────────────────────────────────────────────────
        self._container = tk.Frame(self, bg=BG)
        self._container.pack(fill="both", expand=True)

        self._build_page_build()
        self._build_page_setup()
        self._build_page_history()

        # Bottom accent line
        tk.Frame(self, bg=ORANGE, height=4).pack(fill="x", side="bottom")

        self._switch_tab("BUILD")

    # ─────────────────────────────────────────────────────────────────────
    #  Tab switching
    # ─────────────────────────────────────────────────────────────────────
    def _switch_tab(self, key):
        for k, btn in self._tabs.items():
            btn.configure(bg=BG if k == key else BG2,
                          fg=ACCENT if k == key else MUTED)
        for k, page in self._pages.items():
            (page.pack if k == key else page.pack_forget)(
                fill="both", expand=True) if k == key else page.pack_forget()
        if key == "HISTORY":
            self._refresh_history()

    # ═════════════════════════════════════════════════════════════════════
    #  PAGE 1 — BUILD  (two-column PC layout)
    # ═════════════════════════════════════════════════════════════════════
    def _build_page_build(self):
        page = tk.Frame(self._container, bg=BG)
        self._pages["BUILD"] = page

        # ── Two-column split ──────────────────────────────────────────────
        # LEFT  = settings panel (fixed width, scrollable)
        # RIGHT = build log (expands to fill remaining space)

        left_outer = tk.Frame(page, bg=BG2, width=420)
        left_outer.pack(side="left", fill="y")
        left_outer.pack_propagate(False)

        # Divider
        tk.Frame(page, bg=BORDER, width=1).pack(side="left", fill="y")

        right_panel = tk.Frame(page, bg=BG)
        right_panel.pack(side="left", fill="both", expand=True)

        # ── LEFT: scrollable settings ─────────────────────────────────────
        canvas = tk.Canvas(left_outer, bg=BG2, highlightthickness=0)
        sb = ttk.Scrollbar(left_outer, orient="vertical", command=canvas.yview)
        sf = tk.Frame(canvas, bg=BG2)
        sf.bind("<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sf, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>",
            lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        P = 18  # padding

        # ── SECTION: INPUT & OUTPUT ───────────────────────────────────────
        self._lsec(sf, "INPUT & OUTPUT", P)

        self._llbl(sf, "HTML File  *", P)
        fr = tk.Frame(sf, bg=BG2); fr.pack(fill="x", padx=P, pady=(2,8))
        self._entry(fr, self.var_html, ACCENT).pack(
            side="left", fill="x", expand=True, ipady=7, ipadx=6)
        self._btn(fr, "BROWSE", self._pick_html,
                  ACCENT, BG, px=10, py=7).pack(side="left", padx=(5,0))

        self._llbl(sf, "App Icon  (.ico  optional)", P)
        fi = tk.Frame(sf, bg=BG2); fi.pack(fill="x", padx=P, pady=(2,8))
        self._entry(fi, self.var_icon, MUTED).pack(
            side="left", fill="x", expand=True, ipady=7, ipadx=6)
        self._btn(fi, "BROWSE", self._pick_icon,
                  PANEL, MUTED, px=10, py=7).pack(side="left", padx=(5,0))

        self._llbl(sf, "Output Folder  (blank → dist/)", P)
        fo = tk.Frame(sf, bg=BG2); fo.pack(fill="x", padx=P, pady=(2,12))
        self._entry(fo, self.var_out_dir, MUTED).pack(
            side="left", fill="x", expand=True, ipady=7, ipadx=6)
        self._btn(fo, "BROWSE", self._pick_out_dir,
                  PANEL, MUTED, px=10, py=7).pack(side="left", padx=(5,0))

        # ── SECTION: APP IDENTITY ─────────────────────────────────────────
        self._lsec(sf, "APP IDENTITY", P)

        self._llbl(sf, "App Name  *", P)
        self._entry(sf, self.var_name, WHITE).pack(
            fill="x", padx=P, pady=(2,8), ipady=7, ipadx=6)

        row_vi = tk.Frame(sf, bg=BG2); row_vi.pack(fill="x", padx=P, pady=(0,12))
        ver_f = tk.Frame(row_vi, bg=BG2); ver_f.pack(side="left", fill="x", expand=True)
        self._llbl(ver_f, "Version", 0)
        self._entry(ver_f, self.var_version, WHITE, w=10).pack(
            fill="x", pady=(2,0), ipady=7, ipadx=6)
        auth_f = tk.Frame(row_vi, bg=BG2); auth_f.pack(side="left", fill="x", expand=True, padx=(8,0))
        self._llbl(auth_f, "Author", 0)
        self._entry(auth_f, self.var_author, WHITE).pack(
            fill="x", pady=(2,0), ipady=7, ipadx=6)

        # ── SECTION: WINDOW SIZE ──────────────────────────────────────────
        self._lsec(sf, "WINDOW SIZE", P)

        row_wh = tk.Frame(sf, bg=BG2); row_wh.pack(fill="x", padx=P, pady=(2,6))
        for lbl, var in [("Width (px)", self.var_width), ("Height (px)", self.var_height)]:
            f = tk.Frame(row_wh, bg=BG2); f.pack(side="left", fill="x", expand=True, padx=(0,6))
            self._llbl(f, lbl, 0)
            self._entry(f, var, WHITE, w=8).pack(fill="x", pady=(2,0), ipady=7, ipadx=6)

        row_mn = tk.Frame(sf, bg=BG2); row_mn.pack(fill="x", padx=P, pady=(0,6))
        for lbl, var in [("Min Width", self.var_min_w), ("Min Height", self.var_min_h)]:
            f = tk.Frame(row_mn, bg=BG2); f.pack(side="left", fill="x", expand=True, padx=(0,6))
            self._llbl(f, lbl, 0)
            self._entry(f, var, MUTED, w=8).pack(fill="x", pady=(2,0), ipady=7, ipadx=6)

        # Size presets
        self._llbl(sf, "Quick Presets", P)
        pr = tk.Frame(sf, bg=BG2); pr.pack(fill="x", padx=P, pady=(4,12))
        presets = [
            ("360×640",  360,  640),
            ("800×600",  800,  600),
            ("1280×720", 1280, 720),
            ("1920×1080",1920,1080),
            ("800×800",  800,  800),
        ]
        for i, (lbl, w, h) in enumerate(presets):
            self._btn(pr, lbl,
                      lambda ww=w, hh=h: self._apply_preset(ww, hh),
                      PANEL, MUTED, px=7, py=5
                      ).grid(row=i//3, column=i%3, padx=(0,4), pady=(0,4), sticky="ew")
        pr.columnconfigure((0,1,2), weight=1)

        # ── SECTION: WINDOW BEHAVIOUR ─────────────────────────────────────
        self._lsec(sf, "WINDOW BEHAVIOUR", P)

        cb1 = tk.Frame(sf, bg=BG2); cb1.pack(fill="x", padx=P, pady=(4,4))
        self._chk(cb1, "Fullscreen",     self.var_fullscreen)
        self._chk(cb1, "Resizable",      self.var_resizable)
        cb2 = tk.Frame(sf, bg=BG2); cb2.pack(fill="x", padx=P, pady=(0,12))
        self._chk(cb2, "Always on Top",  self.var_on_top)

        # ── SECTION: BUILD OPTIONS ────────────────────────────────────────
        self._lsec(sf, "BUILD OPTIONS", P)

        cbo = tk.Frame(sf, bg=BG2); cbo.pack(fill="x", padx=P, pady=(4,8))
        self._chk(cbo, "Single File  (--onefile)", self.var_one_file)

        self._llbl(sf, "Loading BG Color  (hex, e.g. #0d1117)", P)
        bgr = tk.Frame(sf, bg=BG2); bgr.pack(fill="x", padx=P, pady=(2,18))
        self._entry(bgr, self.var_bg_color, WHITE, w=12).pack(
            side="left", ipady=7, ipadx=6)

        # Spacer so scrollbar doesn't cut off last item
        tk.Frame(sf, bg=BG2, height=12).pack()

        # ── RIGHT: Build log + controls ───────────────────────────────────
        # Top action bar
        action_bar = tk.Frame(right_panel, bg=PANEL2, pady=12)
        action_bar.pack(fill="x", padx=0)

        self.btn_build = self._btn(
            action_bar, "  ▶   BUILD EXE  ",
            self._start_build, ACCENT, BG,
            font=MONO_LG, px=32, py=12)
        self.btn_build.pack(side="left", padx=(20,8))

        self._btn(action_bar, "  📂  Open dist/  ", self._open_dist,
                  PANEL, MUTED, px=14, py=12).pack(side="left", padx=(0,6))

        self._btn(action_bar, "  ✕  Clear Log  ", self._clear_log,
                  PANEL, MUTED, px=14, py=12).pack(side="left")

        # Status / progress bar
        s = ttk.Style()
        s.theme_use("default")
        s.configure("BT.Horizontal.TProgressbar",
                    troughcolor=PANEL, background=ACCENT,
                    thickness=5, borderwidth=0)
        self.progress = ttk.Progressbar(
            right_panel, style="BT.Horizontal.TProgressbar",
            mode="indeterminate")
        self.progress.pack(fill="x", padx=0, pady=0)

        # Log label
        log_hdr = tk.Frame(right_panel, bg=BG2, pady=8)
        log_hdr.pack(fill="x")
        tk.Label(log_hdr, text="  BUILD LOG",
                 font=("Courier New", 9, "bold"),
                 bg=BG2, fg=ACCENT).pack(side="left", padx=16)
        tk.Frame(log_hdr, bg=BORDER, height=1).pack(
            side="left", fill="x", expand=True, padx=(8,16), pady=4)

        # Log console — expands to fill all remaining space
        self.log = scrolledtext.ScrolledText(
            right_panel,
            font=("Courier New", 9),
            bg="#010409", fg=GREEN,
            insertbackground=GREEN,
            relief="flat", bd=0,
            highlightthickness=0,
            state="disabled")
        self.log.pack(fill="both", expand=True, padx=0, pady=0)
        self.log.tag_config("ok",  foreground=GREEN)
        self.log.tag_config("err", foreground=ORANGE)
        self.log.tag_config("hdr", foreground=ACCENT)
        self.log.tag_config("warn", foreground=YELLOW)

        self._log(
            f"  {APP_NAME}  ·  {APP_AUTHOR}  ·  {APP_VERSION}\n"
            f"  {'─'*48}\n"
            f"  Fill in the settings on the left, then click\n"
            f"  ▶ BUILD EXE to generate your desktop app.\n\n",
            tag="hdr")

    # ═════════════════════════════════════════════════════════════════════
    #  PAGE 2 — SETUP
    # ═════════════════════════════════════════════════════════════════════
    def _build_page_setup(self):
        page = tk.Frame(self._container, bg=BG)
        self._pages["SETUP"] = page

        # Scroll container
        canvas = tk.Canvas(page, bg=BG, highlightthickness=0)
        sb = ttk.Scrollbar(page, orient="vertical", command=canvas.yview)
        sf = tk.Frame(canvas, bg=BG)
        sf.bind("<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sf, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        body = tk.Frame(sf, bg=BG)
        body.pack(fill="both", expand=True, padx=40, pady=28)

        tk.Label(body, text="Project Setup & Information",
                 font=MONO_LG, bg=BG, fg=ACCENT).pack(anchor="w", pady=(0,20))

        # Two-column card grid for info cards
        cards_frame = tk.Frame(body, bg=BG)
        cards_frame.pack(fill="x", pady=(0,20))
        cards_frame.columnconfigure(0, weight=1)
        cards_frame.columnconfigure(1, weight=1)

        cards = [
            ("⚡  What This Tool Does",
             "HTML TO EXE CONVERTER packages any HTML/CSS/JS project\n"
             "into a standalone Windows .exe app.\n\n"
             "Uses PyWebView to render HTML in a native window and\n"
             "PyInstaller to bundle everything into a single .exe."),

            ("📦  Requirements",
             "• Python 3.8+  →  python.org/downloads\n"
             "• Windows 10 or Windows 11\n"
             "• pywebview 4.0+    (auto-installed)\n"
             "• pyinstaller 5.13+  (auto-installed)"),

            ("📁  Project Structure",
             "html-to-exe/\n"
             "├── converter.py     ← this GUI tool\n"
             "├── build_cli.py     ← CLI alternative\n"
             "├── build.bat        ← double-click launcher\n"
             "├── setup.py         ← first-time installer\n"
             "├── cleanup.py       ← remove temp files\n"
             "├── input/\n"
             "│   └── index.html   ← your HTML here\n"
             "└── dist/\n"
             "    └── MyApp.exe    ← output"),

            ("📂  Auto-Bundled Folders",
             "These folders are detected and bundled\n"
             "automatically if next to your HTML file:\n\n"
             "  css/    js/     assets/\n"
             "  images/ img/    fonts/\n"
             "  media/  static/ lib/   libs/"),

            ("💡  Tips",
             "• Inline CSS/JS for smallest single-file builds\n"
             "• Convert PNG → .ico at convertico.com\n"
             "• Build takes 1–3 minutes — this is normal\n"
             "• Run cleanup.py after building\n"
             "• Test HTML in a browser first\n"
             "• Spaces in app names → underscores"),

            ("🛠  Built With",
             "PyWebView 4.0+\n"
             "  → renders HTML inside native window\n\n"
             "PyInstaller 5.13+\n"
             "  → packages everything into .exe\n\n"
             "Tkinter  (built-in)\n"
             "  → GUI framework for this tool"),
        ]

        for i, (title, text) in enumerate(cards):
            card = tk.Frame(cards_frame, bg=PANEL, padx=18, pady=16)
            card.grid(row=i//2, column=i%2, sticky="nsew",
                      padx=(0 if i%2 else 0, 8 if i%2==0 else 0),
                      pady=(0,10))
            tk.Label(card, text=title,
                     font=("Courier New", 10, "bold"),
                     bg=PANEL, fg=ACCENT).pack(anchor="w", pady=(0,10))
            tk.Label(card, text=text, font=MONO_SM,
                     bg=PANEL, fg=TEXT, justify="left").pack(anchor="w")

        # Padding between columns
        for i in range(len(cards)//2 + 1):
            cards_frame.rowconfigure(i, weight=0)

        # Install button
        tk.Frame(body, bg=BORDER, height=1).pack(fill="x", pady=(8,20))
        ir = tk.Frame(body, bg=BG)
        ir.pack(fill="x")
        self._btn(ir, "  ⬇   Install / Update Dependencies  ",
                  self._run_setup, GREEN, BG,
                  font=MONO_MD, px=24, py=12).pack(side="left")
        tk.Label(ir, text="  Installs pywebview + pyinstaller via pip",
                 font=MONO_SM, bg=BG, fg=MUTED).pack(side="left", padx=12)

        self.setup_status = tk.Label(body, text="",
                                     font=MONO_SM, bg=BG, fg=GREEN)
        self.setup_status.pack(anchor="w", pady=(10,0))

    # ═════════════════════════════════════════════════════════════════════
    #  PAGE 3 — HISTORY
    # ═════════════════════════════════════════════════════════════════════
    def _build_page_history(self):
        page = tk.Frame(self._container, bg=BG)
        self._pages["HISTORY"] = page

        hrow = tk.Frame(page, bg=BG)
        hrow.pack(fill="x", padx=28, pady=(20,10))
        tk.Label(hrow, text="Convert History",
                 font=MONO_LG, bg=BG, fg=ACCENT).pack(side="left")
        self._btn(hrow, "  🗑  Clear History  ", self._clear_history,
                  PANEL, ORANGE, px=12, py=6).pack(side="right")

        tk.Frame(page, bg=BORDER, height=1).pack(fill="x", padx=28)

        # Column headers
        COL_WIDTHS = [("#",4),("App Name",18),("Size",12),
                      ("Status",8),("Date & Time",22),("Output",0)]
        hcols = tk.Frame(page, bg=PANEL2)
        hcols.pack(fill="x", padx=28, pady=(0,1))
        for txt, w in COL_WIDTHS:
            kw = dict(font=("Courier New",8,"bold"), bg=PANEL2, fg=MUTED,
                      anchor="w", padx=8, pady=7)
            if w: kw["width"] = w
            tk.Label(hcols, text=txt, **kw).pack(side="left")

        # Scrollable rows
        lf = tk.Frame(page, bg=BG)
        lf.pack(fill="both", expand=True, padx=28)
        self.hist_canvas = tk.Canvas(lf, bg=BG, highlightthickness=0)
        hsb = ttk.Scrollbar(lf, orient="vertical",
                            command=self.hist_canvas.yview)
        self.hist_inner = tk.Frame(self.hist_canvas, bg=BG)
        self.hist_inner.bind("<Configure>",
            lambda e: self.hist_canvas.configure(
                scrollregion=self.hist_canvas.bbox("all")))
        self.hist_canvas.create_window((0,0), window=self.hist_inner,
                                        anchor="nw")
        self.hist_canvas.configure(yscrollcommand=hsb.set)
        self.hist_canvas.pack(side="left", fill="both", expand=True)
        hsb.pack(side="right", fill="y")

        tk.Frame(page, bg=BORDER, height=1).pack(fill="x", padx=28, pady=(4,0))
        self.hist_count = tk.Label(page, text="",
                                   font=MONO_SM, bg=BG, fg=MUTED)
        self.hist_count.pack(anchor="w", padx=28, pady=(6,12))

    def _refresh_history(self):
        for w in self.hist_inner.winfo_children():
            w.destroy()
        records = list(reversed(load_history()))
        total   = len(load_history())

        if not records:
            tk.Label(self.hist_inner,
                text="\n  No builds yet. Build your first EXE to see history.\n",
                font=MONO_SM, bg=BG, fg=MUTED).pack(anchor="w", padx=16)
            self.hist_count.configure(text="0 builds")
            return

        for i, rec in enumerate(records):
            bg_row = BG if i % 2 == 0 else PANEL2
            row = tk.Frame(self.hist_inner, bg=bg_row)
            row.pack(fill="x")

            ok  = rec.get("success", False)
            sc  = GREEN if ok else ORANGE
            st  = "✓  OK" if ok else "✗  FAIL"
            wh  = f"{rec.get('width','-')}×{rec.get('height','-')}"

            for txt, width in [
                (str(total - i),             4),
                (rec.get("app_name","-"),   18),
                (wh,                        12),
                (st,                         8),
                (rec.get("timestamp","-"),  22),
            ]:
                tk.Label(row, text=txt,
                         font=MONO_SM, bg=bg_row,
                         fg=sc if txt == st else TEXT,
                         width=width, anchor="w",
                         padx=8, pady=8).pack(side="left")

            path = rec.get("exe_path", "-")
            tk.Label(row, text=path, font=MONO_SM,
                     bg=bg_row, fg=MUTED,
                     anchor="w", padx=4).pack(side="left", fill="x", expand=True)

            if ok and path and os.path.isfile(path):
                self._btn(row, " Open ", lambda p=path: os.startfile(p),
                          PANEL, ACCENT, px=8, py=4).pack(
                    side="right", padx=8, pady=4)

        self.hist_count.configure(text=f"{total} build(s) recorded")

    def _clear_history(self):
        if messagebox.askyesno("Clear History",
                               "Delete all build history records?"):
            save_history([])
            self._refresh_history()

    # ─────────────────────────────────────────────────────────────────────
    #  Setup page
    # ─────────────────────────────────────────────────────────────────────
    def _run_setup(self):
        self.setup_status.configure(text="Installing…", fg=YELLOW)
        self.update()
        try:
            ensure_dependencies()
            self.setup_status.configure(
                text="✓  pywebview and pyinstaller are ready!", fg=GREEN)
        except Exception as e:
            self.setup_status.configure(text=f"✗  {e}", fg=ORANGE)

    # ─────────────────────────────────────────────────────────────────────
    #  Widget helpers
    # ─────────────────────────────────────────────────────────────────────
    def _lsec(self, parent, title, px=18):
        """Section header for left panel."""
        f = tk.Frame(parent, bg=BG2)
        f.pack(fill="x", padx=px, pady=(14, 6))
        tk.Label(f, text=title,
                 font=("Courier New", 8, "bold"),
                 bg=BG2, fg=ACCENT).pack(side="left")
        tk.Frame(f, bg=BORDER, height=1).pack(
            side="left", fill="x", expand=True, padx=(10,0), pady=4)

    def _llbl(self, parent, text, px=0):
        """Small label for left panel."""
        tk.Label(parent, text=f"  {text}",
                 font=MONO_SM, bg=BG2, fg=MUTED).pack(
            anchor="w", padx=px if isinstance(px, int) else 0)

    def _entry(self, parent, var, fg, w=None):
        kw = dict(textvariable=var, font=MONO,
                  bg=PANEL, fg=fg, insertbackground=fg,
                  relief="flat", bd=0,
                  highlightthickness=1,
                  highlightbackground=BORDER,
                  highlightcolor=ACCENT)
        if w: kw["width"] = w
        return tk.Entry(parent, **kw)

    def _btn(self, parent, text, cmd, bg, fg,
             font=None, px=12, py=8):
        return tk.Button(parent, text=text, command=cmd,
                         font=font or MONO_SM,
                         bg=bg, fg=fg,
                         activebackground=BORDER,
                         activeforeground=WHITE,
                         relief="flat", bd=0,
                         cursor="hand2", padx=px, pady=py)

    def _chk(self, parent, label, var):
        tk.Checkbutton(parent, text=f"  {label}", variable=var,
                       font=MONO_SM, bg=BG2, fg=TEXT,
                       selectcolor=PANEL,
                       activebackground=BG2,
                       activeforeground=ACCENT,
                       cursor="hand2").pack(side="left", padx=(0,16))

    # ─────────────────────────────────────────────────────────────────────
    #  File pickers
    # ─────────────────────────────────────────────────────────────────────
    def _pick_html(self):
        p = filedialog.askopenfilename(
            title="Select HTML file",
            filetypes=[("HTML", "*.html *.htm"), ("All", "*.*")])
        if p:
            self.var_html.set(p)
            self._log(f"  [INPUT]   {p}\n")
            base = os.path.splitext(os.path.basename(p))[0]
            if self.var_name.get() == "MyApp":
                self.var_name.set(base.replace(" ", "_"))

    def _pick_icon(self):
        p = filedialog.askopenfilename(
            title="Select icon (.ico)",
            filetypes=[("ICO", "*.ico"), ("All", "*.*")])
        if p:
            self.var_icon.set(p)
            self._log(f"  [ICON]    {p}\n")

    def _pick_out_dir(self):
        p = filedialog.askdirectory(title="Select output folder")
        if p:
            self.var_out_dir.set(p)
            self._log(f"  [OUTPUT]  {p}\n")

    def _apply_preset(self, w, h):
        self.var_width.set(str(w))
        self.var_height.set(str(h))
        self._log(f"  [PRESET]  {w}×{h}\n")

    # ─────────────────────────────────────────────────────────────────────
    #  Log helpers
    # ─────────────────────────────────────────────────────────────────────
    def _log(self, msg, tag=None):
        self.log.configure(state="normal")
        if tag:
            self.log.insert("end", msg, tag)
        else:
            self.log.insert("end", msg)
        self.log.see("end")
        self.log.configure(state="disabled")

    def _clear_log(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def _open_dist(self):
        d = self.var_out_dir.get().strip() or \
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
        os.makedirs(d, exist_ok=True)
        if sys.platform == "win32":
            os.startfile(d)
        else:
            subprocess.Popen(["xdg-open", d])

    # ─────────────────────────────────────────────────────────────────────
    #  Start build
    # ─────────────────────────────────────────────────────────────────────
    def _start_build(self):
        if self._building:
            return

        html = self.var_html.get().strip()
        if not html or not os.path.isfile(html):
            messagebox.showerror("No HTML File",
                "Please select a valid HTML file.\nClick BROWSE on the left.")
            return

        name = (self.var_name.get().strip() or "MyApp").replace(" ", "_")

        try:
            width  = int(self.var_width.get())
            height = int(self.var_height.get())
            min_w  = int(self.var_min_w.get())
            min_h  = int(self.var_min_h.get())
        except ValueError:
            messagebox.showerror("Invalid Value",
                "Width / Height / Min Width / Min Height must be numbers.")
            return

        params = {
            "html_path":  html,
            "app_name":   name,
            "width":      width,
            "height":     height,
            "min_w":      min_w,
            "min_h":      min_h,
            "icon_path":  self.var_icon.get().strip(),
            "out_dir":    self.var_out_dir.get().strip(),
            "fullscreen": self.var_fullscreen.get(),
            "resizable":  self.var_resizable.get(),
            "on_top":     self.var_on_top.get(),
            "one_file":   self.var_one_file.get(),
            "bg_color":   self.var_bg_color.get().strip() or "#ffffff",
        }
        self._current_params = params
        self._building = True
        self.btn_build.configure(state="disabled",
                                 text="  ⏳   BUILDING…  ", bg=MUTED)
        self.progress.start(10)

        threading.Thread(target=run_build,
                         args=(params, self._t_log, self._t_done),
                         daemon=True).start()

    # ─────────────────────────────────────────────────────────────────────
    #  Thread callbacks
    # ─────────────────────────────────────────────────────────────────────
    def _t_log(self, msg):
        tag = None
        m = msg.lower()
        if any(w in m for w in ("error","failed","exception","✗")):
            tag = "err"
        elif any(w in m for w in ("success","✓","[ok]")):
            tag = "ok"
        self.after(0, lambda: self._log(msg, tag))

    def _t_done(self, success, exe_path):
        def _cb():
            self._building = False
            self.progress.stop()
            self.btn_build.configure(
                state="normal",
                text="  ▶   BUILD EXE  ",
                bg=ACCENT)

            p = self._current_params
            add_history({
                "app_name":  p["app_name"],
                "width":     p["width"],
                "height":    p["height"],
                "success":   success,
                "exe_path":  exe_path or "",
                "timestamp": datetime.datetime.now().strftime(
                    "%Y-%m-%d  %H:%M:%S"),
            })

            if success:
                messagebox.showinfo("Build Successful  ✓",
                    f"Your EXE is ready!\n\n📁  {exe_path}\n\n"
                    f"Double-click it to launch your app.\n\n— {APP_AUTHOR}")
            else:
                messagebox.showerror("Build Failed  ✗",
                    "Build failed. Check the log on the right.\n\n"
                    "Common fixes:\n"
                    "  • SETUP tab → Install Dependencies\n"
                    "  • Verify your HTML file is valid\n"
                    f"\n— {APP_AUTHOR}")
        self.after(0, _cb)


# ─────────────────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = HTMLtoEXEApp()
    app.mainloop()
