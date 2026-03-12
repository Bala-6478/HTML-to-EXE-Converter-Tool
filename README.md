# ⚡ HTML TO EXE CONVERTER
### Developed by BALAVIGNESH A

Convert any HTML project into a native Windows desktop `.exe` application.

---  

## 🚀 Quick Start  

### Option 1 — GUI (Recommended)
```
Double-click build.bat
```
or
```
python converter.py
```

### Option 2 — CLI (Advanced)
```
python build_cli.py input/index.html
python build_cli.py input/index.html --name MyApp --width 1280 --height 720
python build_cli.py input/index.html --fullscreen --icon app.ico
```

---

## 📁 Folder Structure

```
HTML_TO_EXE_CONVERTER/
│
├── converter.py        ← Launch GUI
├── gui.py              ← GUI interface
├── builder.py          ← Build engine
├── build_cli.py        ← Command-line mode
├── build.bat           ← Windows launcher (double-click)
│
├── input/
│   └── index.html      ← Place your HTML file here
│
├── temp/               ← Build workspace (auto-created)
├── dist/               ← Output EXE goes here
└── logs/
    └── build_logs.txt  ← Build logs
```

---

## ⚙️ Requirements

- **Python 3.8+** — [python.org](https://python.org)
- **Windows 10/11** (for EXE output)

Dependencies are auto-installed on first run:
- `pywebview` — browser engine
- `pyinstaller` — EXE builder

---

## 🎨 GUI Features

| Feature | Description |
|---|---|
| Select HTML File | Browse to any `.html` file |
| App Icon | Add a custom `.ico` icon |
| App Name | Set the output EXE name |
| Window Size | Set width & height |
| Fullscreen | Launch fullscreen |
| Resizable | Toggle resize |
| Always on Top | Window stays on top |
| Build Log | Real-time logs |
| Progress Bar | Visual build progress |
| Open Output | Quick access to `dist/` |

---

## 📦 HTML Feature Support

| Feature | Supported |
|---|---|
| HTML5 / CSS3 / JavaScript | ✅ |
| Canvas / SVG / WebGL | ✅ |
| Internet access / API calls | ✅ |
| External CDN libraries | ✅ |
| Images / Videos / Audio | ✅ |
| Fonts / Icons | ✅ |
| Drag & Drop / File input | ✅ |
| localStorage / sessionStorage | ✅ |
| IndexedDB | ✅ |
| iframes | ✅ |
| Animations | ✅ |
| YouTube / embeds | ✅ |

---

## 🔧 CLI Options

```
python build_cli.py [HTML_FILE] [OPTIONS]

Options:
  --name       Output EXE name (default: MyApp)
  --icon       Path to .ico file
  --width      Window width in px (default: 1200)
  --height     Window height in px (default: 800)
  --fullscreen Launch in fullscreen mode
  --no-resize  Disable window resizing
  --on-top     Always on top
```

---

## 📂 Asset Detection

The converter **automatically detects and bundles**:

- `./images/`, `./img/` — image folders
- `./assets/` — general assets
- `./scripts/`, `./js/` — JavaScript files
- `./css/` — stylesheets
- `./fonts/` — custom fonts
- `./media/`, `./videos/`, `./audio/` — media files
- `./static/`, `./icons/` — static resources

All files referenced via `src=`, `href=`, or `url()` in your HTML are auto-included.

---

## 💡 Tips

1. **Single-file HTML works best** — embed CSS and JS inline
2. **External resources** (CDN links) work if internet is available
3. Add `app.ico` to the project root for a custom EXE icon
4. Check `logs/build_logs.txt` if a build fails

---

## 📌 About

Built with:
- **PyWebView** — Chromium-based embedded browser
- **PyInstaller** — Python to EXE packaging
- **Tkinter** — GUI framework

---

*Developed by BALAVIGNESH A— HTML TO EXE CONVERTER v1.0*



### 📸 Preview

![3D Model Viewer Screenshot]()
