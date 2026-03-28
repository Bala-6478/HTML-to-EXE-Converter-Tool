# ⚡ HTML TO EXE CONVERTER

> Convert any HTML / CSS / JavaScript project into a standalone Windows `.exe` desktop app.

**Developed by BEST_TEAM · v3.0 · Windows 10/11 · Python 3.8+**

---

## 📁 Project Structure

```
html-to-exe/
├── converter.py        ← GUI app — main tool  (3 tabs: Build, Setup, History)
├── build_cli.py        ← CLI tool
├── build.bat           ← Double-click launcher
├── setup.py            ← First-time setup
├── cleanup.py          ← Remove temp files
├── requirements.txt    ← Dependencies
├── build_history.json  ← Auto-created build history log
├── input/
│   └── index.html      ← Put your HTML here
└── dist/
    └── MyApp.exe       ← Output appears here
```

---

## 🚀 Quick Start

**1. Setup — run once**
```bash
python setup.py
```

**2. Launch**
```bash
build.bat               # double-click — opens GUI
python converter.py     # or run directly
```

**3. Select your HTML → configure → click ▶ BUILD EXE**

---

## 🖥️ GUI — 3 Tabs

### 🔨 BUILD Tab
All settings and the build log on one scrollable page.

| Section | Fields |
|---------|--------|
| **A · Input & Output** | HTML file, Icon (.ico), Custom output folder |
| **B · App Identity** | App Name, Version, Author |
| **C · Window Size** | Width, Height, Min Width, Min Height + size presets |
| **D · Window Behaviour** | Fullscreen, Resizable, Always on Top |
| **E · Build Options** | Single File (--onefile), Loading BG Color |

**Window Size Presets:**
`Mobile 360×640` · `SD 800×600` · `HD 1280×720` · `FHD 1920×1080` · `Square 800×800`

### ⚙️ SETUP Tab
- Project structure reference
- Requirements and tips
- **Install / Update Dependencies** button — installs `pywebview` + `pyinstaller` with one click

### 📋 HISTORY Tab
- Full log of every build attempt
- Shows: App Name, Window Size, Status (✓ / ✗), Date & Time, Output Path
- **Open** button to launch the built `.exe` directly
- **Clear History** button

---

## ⚙️ CLI Options

```bash
python build_cli.py input/index.html --name MyApp --width 1280 --height 720
python build_cli.py input/index.html --name MyApp --icon app.ico --fullscreen
python build_cli.py input/index.html --name MyApp --no-resize
```

| Flag | Default | Description |
|------|---------|-------------|
| `--name` | `MyApp` | EXE name |
| `--width` | `1280` | Window width (px) |
| `--height` | `720` | Window height (px) |
| `--icon` | — | Path to `.ico` file |
| `--fullscreen` | off | Launch fullscreen |
| `--no-resize` | off | Fixed window size |

---

## 📦 Requirements

- Python 3.8+ — [python.org/downloads](https://www.python.org/downloads/)
- Windows 10 / 11
- `pywebview` and `pyinstaller` — **auto-installed**

---

## 💡 Tips

- Asset folders (`css/`, `js/`, `assets/`, `images/`, `fonts/`) are **auto-bundled**
- Convert PNG → `.ico` free at [convertico.com](https://convertico.com)
- Build takes **1–3 minutes** — this is normal
- Run `cleanup.py` after building to remove temp files

---

## 🛠 Built With

| | |
|---|---|
| [PyWebView](https://pywebview.flowrl.com/) | Renders HTML in a native window |
| [PyInstaller](https://pyinstaller.org/) | Packages everything into `.exe` |
| Tkinter | GUI framework |

---

*⚡ Developed by **BEST_TEAM** · v3.0*
