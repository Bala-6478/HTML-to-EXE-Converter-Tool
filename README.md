# ⚡ HTML TO EXE CONVERTER

> Convert any HTML / CSS / JavaScript project into a standalone Windows `.exe` desktop app.

**Developed by BEST_TEAM · v2.0 · Windows 10/11 · Python 3.8+**

---

## 📁 Project Structure

```
html-to-exe/
├── converter.py        ← GUI app (main tool)
├── build_cli.py        ← CLI tool
├── build.bat           ← Double-click launcher
├── setup.py            ← First-time setup
├── cleanup.py          ← Remove temp files
├── requirements.txt    ← Dependencies
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
# GUI (recommended)
build.bat

# CLI
python build_cli.py input/index.html --name MyApp --width 1280 --height 720
```

**3. Find your `.exe` in `dist/` and double-click to run!**

---

## ⚙️ CLI Options

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
- `pywebview` and `pyinstaller` — **auto-installed** by `setup.py`

---

## 💡 Tips

- Put CSS, JS, images in `css/`, `js/`, `assets/` folders next to your HTML — they bundle automatically
- Use `.ico` format for icons
- Build takes **1–3 minutes** — this is normal
- Run `cleanup.py` after building to remove temp files

---

## 🛠 Built With

| | |
|---|---|
| [PyWebView](https://pywebview.flowrl.com/) | Renders HTML in a native window |
| [PyInstaller](https://pyinstaller.org/) | Packages everything into `.exe` |
| Tkinter | GUI framework for the converter |

---


### 📸 Preview

![Image Alt]()

---
*⚡ Developed by **BEST_TEAM** · v2.0*
