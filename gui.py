"""
HTML to EXE Converter - GUI
Developed by BALAVIGNESH A
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys
import subprocess
from pathlib import Path
from builder import BuildEngine


# ── Color Palette ──────────────────────────────────────────
BG_DARK    = "#0D0D0F"
BG_PANEL   = "#141418"
BG_CARD    = "#1A1A20"
BG_FIELD   = "#0F0F14"
ACCENT     = "#00E5FF"
ACCENT2    = "#7B2FFF"
GREEN      = "#00FF88"
RED        = "#FF4757"
YELLOW     = "#FFD700"
TEXT_WHITE = "#EAEAF0"
TEXT_MUTED = "#6B6B80"
TEXT_DIM   = "#3A3A4A"
BORDER     = "#252530"


class HoverButton(tk.Button):
    def __init__(self, master, **kwargs):
        self.default_bg = kwargs.get("bg", BG_CARD)
        self.hover_bg   = kwargs.pop("hover_bg", ACCENT2)
        super().__init__(master, **kwargs)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, e):
        self.config(bg=self.hover_bg)

    def _on_leave(self, e):
        self.config(bg=self.default_bg)


class ConverterGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("HTML TO EXE CONVERTER  |  Developed by BALAVIGNESH A")
        self.root.geometry("900x700")
        self.root.minsize(760, 580)
        self.root.configure(bg=BG_DARK)
        self.root.resizable(True, True)

        # Set icon if present
        ico = Path(__file__).parent / "app.ico"
        if ico.exists():
            try:
                self.root.iconbitmap(str(ico))
            except Exception:
                pass

        self.html_path    = tk.StringVar()
        self.icon_path    = tk.StringVar()
        self.app_name     = tk.StringVar(value="MyApp")
        self.win_width    = tk.IntVar(value=1200)
        self.win_height   = tk.IntVar(value=800)
        self.fullscreen   = tk.BooleanVar(value=False)
        self.resizable_v  = tk.BooleanVar(value=True)
        self.on_top       = tk.BooleanVar(value=False)
        self.status_text  = tk.StringVar(value="Ready — Select an HTML file to begin")
        self.progress_val = tk.DoubleVar(value=0)

        self._build_ui()
        self._center_window()

    # ─── Layout ───────────────────────────────────────────────
    def _build_ui(self):
        self._make_header()
        main = tk.Frame(self.root, bg=BG_DARK)
        main.pack(fill="both", expand=True, padx=20, pady=(0, 16))
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(1, weight=1)

        self._make_input_panel(main)
        self._make_settings_panel(main)
        self._make_log_panel(main)
        self._make_footer(main)

    def _make_header(self):
        hdr = tk.Frame(self.root, bg=ACCENT2, height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        grd = tk.Frame(hdr, bg=ACCENT2)
        grd.place(relx=0, rely=0, relwidth=1, relheight=1)

        tk.Label(grd, text="⚡ HTML TO EXE CONVERTER",
                 font=("Consolas", 18, "bold"),
                 fg=TEXT_WHITE, bg=ACCENT2).pack(side="left", padx=20, pady=12)

        tk.Label(grd, text="Developed by  BALAVIGNESH A",
                 font=("Consolas", 9),
                 fg="#C0A0FF", bg=ACCENT2).pack(side="right", padx=20)

    def _section(self, parent, title, row, col, colspan=1, rowspan=1):
        frame = tk.Frame(parent, bg=BG_CARD,
                         highlightthickness=1, highlightbackground=BORDER)
        frame.grid(row=row, column=col, columnspan=colspan, rowspan=rowspan,
                   sticky="nsew", padx=6, pady=6)

        tk.Label(frame, text=f"  {title}  ",
                 font=("Consolas", 10, "bold"),
                 fg=ACCENT, bg=BG_CARD,
                 anchor="w").pack(fill="x", pady=(10, 2), padx=12)

        sep = tk.Frame(frame, bg=ACCENT2, height=1)
        sep.pack(fill="x", padx=12, pady=(0, 10))
        return frame

    def _label(self, parent, text):
        tk.Label(parent, text=text,
                 font=("Consolas", 9),
                 fg=TEXT_MUTED, bg=BG_CARD,
                 anchor="w").pack(fill="x", padx=14, pady=(4, 1))

    def _entry_row(self, parent, var, btn_text=None, btn_cmd=None):
        row = tk.Frame(parent, bg=BG_CARD)
        row.pack(fill="x", padx=14, pady=(0, 8))

        e = tk.Entry(row, textvariable=var,
                     font=("Consolas", 9),
                     bg=BG_FIELD, fg=TEXT_WHITE,
                     insertbackground=ACCENT,
                     relief="flat", bd=4,
                     highlightthickness=1, highlightbackground=BORDER,
                     highlightcolor=ACCENT)
        e.pack(side="left", fill="x", expand=True, ipady=5)

        if btn_text:
            HoverButton(row, text=btn_text, command=btn_cmd,
                        font=("Consolas", 8, "bold"),
                        bg=BG_PANEL, fg=ACCENT,
                        hover_bg=ACCENT2,
                        relief="flat", bd=0,
                        padx=10, cursor="hand2"
                        ).pack(side="left", padx=(4, 0), ipady=5)

    def _make_input_panel(self, parent):
        sec = self._section(parent, "📁  INPUT FILE", 0, 0)

        self._label(sec, "HTML File Path")
        self._entry_row(sec, self.html_path, "Browse…", self._browse_html)

        self._label(sec, "App Icon (.ico)  [optional]")
        self._entry_row(sec, self.icon_path, "Browse…", self._browse_icon)

        self._label(sec, "Output App Name")
        self._entry_row(sec, self.app_name)

        # Convert button
        self.btn_convert = HoverButton(
            sec,
            text="  🚀  CONVERT TO EXE  ",
            command=self._start_build,
            font=("Consolas", 12, "bold"),
            bg=ACCENT2, fg=TEXT_WHITE,
            hover_bg="#5B1FDF",
            relief="flat", bd=0,
            padx=20, pady=10,
            cursor="hand2"
        )
        self.btn_convert.pack(padx=14, pady=(12, 8), fill="x")

        # Open dist button
        HoverButton(
            sec,
            text="📂  Open Output Folder",
            command=self._open_dist,
            font=("Consolas", 9),
            bg=BG_FIELD, fg=TEXT_MUTED,
            hover_bg=BG_PANEL,
            relief="flat", bd=0,
            padx=12, pady=6,
            cursor="hand2"
        ).pack(padx=14, pady=(0, 12), fill="x")

    def _make_settings_panel(self, parent):
        sec = self._section(parent, "⚙️  WINDOW SETTINGS", 0, 1)

        # Width / Height
        dims = tk.Frame(sec, bg=BG_CARD)
        dims.pack(fill="x", padx=14, pady=(0, 8))

        for label, var in [("Width (px)", self.win_width), ("Height (px)", self.win_height)]:
            col = tk.Frame(dims, bg=BG_CARD)
            col.pack(side="left", expand=True, fill="x", padx=(0, 6))
            tk.Label(col, text=label, font=("Consolas", 8), fg=TEXT_MUTED,
                     bg=BG_CARD, anchor="w").pack(fill="x")
            tk.Entry(col, textvariable=var,
                     font=("Consolas", 9),
                     bg=BG_FIELD, fg=TEXT_WHITE,
                     insertbackground=ACCENT,
                     relief="flat", bd=4,
                     width=8,
                     highlightthickness=1,
                     highlightbackground=BORDER,
                     highlightcolor=ACCENT
                     ).pack(fill="x", ipady=5)

        def chk(parent, text, var):
            f = tk.Frame(parent, bg=BG_CARD)
            f.pack(fill="x", padx=14, pady=2)
            c = tk.Checkbutton(f, text=text, variable=var,
                                font=("Consolas", 9),
                                fg=TEXT_WHITE, bg=BG_CARD,
                                activeforeground=ACCENT,
                                activebackground=BG_CARD,
                                selectcolor=BG_FIELD,
                                relief="flat", bd=0,
                                cursor="hand2")
            c.pack(side="left")

        chk(sec, "Fullscreen on launch",    self.fullscreen)
        chk(sec, "Window resizable",         self.resizable_v)
        chk(sec, "Always on top",            self.on_top)

    def _make_log_panel(self, parent):
        sec = self._section(parent, "📋  BUILD LOG", 1, 0, colspan=2)
        sec.rowconfigure(1, weight=1)

        # Status bar
        status_row = tk.Frame(sec, bg=BG_PANEL)
        status_row.pack(fill="x", padx=14, pady=(0, 6))

        tk.Label(status_row, text="Status:",
                 font=("Consolas", 9, "bold"),
                 fg=TEXT_MUTED, bg=BG_PANEL).pack(side="left")
        self.status_lbl = tk.Label(status_row,
                                   textvariable=self.status_text,
                                   font=("Consolas", 9),
                                   fg=ACCENT, bg=BG_PANEL,
                                   anchor="w")
        self.status_lbl.pack(side="left", padx=8)

        # Progress bar (custom)
        pb_bg = tk.Frame(sec, bg=BG_FIELD, height=6)
        pb_bg.pack(fill="x", padx=14, pady=(0, 8))
        pb_bg.pack_propagate(False)

        self.pb_fill = tk.Frame(pb_bg, bg=ACCENT2, width=0, height=6)
        self.pb_fill.place(x=0, y=0, relheight=1, width=0)

        def update_pb(val):
            self.pb_fill.update_idletasks()
            total = pb_bg.winfo_width()
            fill_w = int(total * val / 100)
            self.pb_fill.place(x=0, y=0, relheight=1, width=fill_w)
            color = GREEN if val >= 100 else ACCENT2
            self.pb_fill.config(bg=color)

        self._update_pb = update_pb

        # Log text area
        log_frame = tk.Frame(sec, bg=BG_CARD)
        log_frame.pack(fill="both", expand=True, padx=14, pady=(0, 10))

        self.log_text = tk.Text(
            log_frame,
            font=("Consolas", 8),
            bg=BG_FIELD, fg=TEXT_WHITE,
            insertbackground=ACCENT,
            relief="flat", bd=0,
            padx=10, pady=8,
            wrap="word",
            state="disabled",
            highlightthickness=1,
            highlightbackground=BORDER
        )
        self.log_text.pack(side="left", fill="both", expand=True)

        sb = tk.Scrollbar(log_frame, command=self.log_text.yview,
                          bg=BG_PANEL, relief="flat")
        sb.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=sb.set)

        # Tag colors
        self.log_text.tag_config("INFO",  foreground=TEXT_WHITE)
        self.log_text.tag_config("WARN",  foreground=YELLOW)
        self.log_text.tag_config("ERROR", foreground=RED)
        self.log_text.tag_config("OK",    foreground=GREEN)

        # Clear button
        HoverButton(sec, text="🗑  Clear Log",
                    command=self._clear_log,
                    font=("Consolas", 8),
                    bg=BG_FIELD, fg=TEXT_MUTED,
                    hover_bg=BG_PANEL,
                    relief="flat", bd=0,
                    padx=10, pady=4,
                    cursor="hand2"
                    ).pack(padx=14, pady=(0, 10), anchor="e")

    def _make_footer(self, parent):
        foot = tk.Frame(self.root, bg=BG_DARK)
        foot.pack(fill="x", pady=(0, 8))
        tk.Label(foot,
                 text="HTML TO EXE CONVERTER  •  Developed by BALAVIGNESH A •  v1.0",
                 font=("Consolas", 8),
                 fg=TEXT_DIM, bg=BG_DARK).pack()

    # ─── Helpers ──────────────────────────────────────────────
    def _center_window(self):
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _browse_html(self):
        p = filedialog.askopenfilename(
            title="Select HTML File",
            filetypes=[("HTML Files", "*.html *.htm"), ("All Files", "*.*")]
        )
        if p:
            self.html_path.set(p)
            stem = Path(p).stem.replace(" ", "_")
            self.app_name.set(stem or "MyApp")
            self._append_log(f"[INFO] Selected: {p}", "INFO")

    def _browse_icon(self):
        p = filedialog.askopenfilename(
            title="Select Icon File",
            filetypes=[("Icon Files", "*.ico"), ("All Files", "*.*")]
        )
        if p:
            self.icon_path.set(p)

    def _open_dist(self):
        dist = Path(__file__).parent / "dist"
        dist.mkdir(exist_ok=True)
        if sys.platform == "win32":
            os.startfile(str(dist))
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(dist)])
        else:
            subprocess.Popen(["xdg-open", str(dist)])

    def _append_log(self, text: str, level="INFO"):
        self.log_text.config(state="normal")
        tag = level if level in ("INFO", "WARN", "ERROR", "OK") else "INFO"
        self.log_text.insert("end", text + "\n", tag)
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def _clear_log(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")

    def _set_status(self, msg: str):
        self.status_text.set(msg)
        tag = "OK" if "✅" in msg else ("ERROR" if "❌" in msg else "INFO")
        self.status_lbl.config(fg=GREEN if "✅" in msg else RED if "❌" in msg else ACCENT)

    def _set_progress(self, val: float):
        self.progress_val.set(val)
        self.root.after(0, lambda: self._update_pb(val))

    # ─── Build ────────────────────────────────────────────────
    def _start_build(self):
        html = self.html_path.get().strip()
        if not html:
            messagebox.showwarning("No File Selected",
                                   "Please select an HTML file first.")
            return

        self.btn_convert.config(state="disabled", text="  ⏳  Building…  ")
        self._clear_log()
        self._set_progress(0)
        self._set_status("Starting build…")

        def run():
            engine = BuildEngine(
                log_callback=lambda msg: self.root.after(0, self._append_log, msg,
                                                          "WARN" if "WARN" in msg
                                                          else "ERROR" if "ERROR" in msg
                                                          else "OK" if "SUCCESS" in msg or "✓" in msg
                                                          else "INFO"),
                progress_callback=self._set_progress,
                status_callback=lambda s: self.root.after(0, self._set_status, s)
            )
            success = engine.build(
                html_path_str=html,
                app_name=self.app_name.get().strip() or "MyApp",
                icon_path=self.icon_path.get().strip() or None,
                fullscreen=self.fullscreen.get(),
                width=self.win_width.get(),
                height=self.win_height.get(),
                resizable=self.resizable_v.get(),
                on_top=self.on_top.get()
            )
            self.root.after(0, self._build_done, success)

        threading.Thread(target=run, daemon=True).start()

    def _build_done(self, success: bool):
        self.btn_convert.config(state="normal", text="  🚀  CONVERT TO EXE  ")
        if success:
            messagebox.showinfo(
                "Build Successful",
                f"✅ EXE created successfully!\n\nLocation: dist/{self.app_name.get()}.exe\n\nDeveloped by BALAVIGNESH A"
            )
        else:
            messagebox.showerror(
                "Build Failed",
                "❌ Build failed. Please check the log window for details."
            )
