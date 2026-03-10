"""
HTML to EXE Converter - Builder Engine
Developed by BALAVIGNESH A
"""

import os
import sys
import shutil
import subprocess
import threading
import re
import json
import base64
from pathlib import Path
from datetime import datetime


class BuildEngine:
    def __init__(self, log_callback=None, progress_callback=None, status_callback=None):
        self.log_callback = log_callback or print
        self.progress_callback = progress_callback or (lambda v: None)
        self.status_callback = status_callback or print
        self.base_dir = Path(__file__).parent
        self.temp_dir = self.base_dir / "temp"
        self.dist_dir = self.base_dir / "dist"
        self.logs_dir = self.base_dir / "logs"
        self.log_file = self.logs_dir / "build_logs.txt"

    def log(self, msg, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] [{level}] {msg}"
        self.log_callback(line)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def set_status(self, msg):
        self.status_callback(msg)

    def set_progress(self, val):
        self.progress_callback(val)

    def ensure_dependencies(self):
        self.log("Checking required dependencies...")
        packages = ["pywebview", "pyinstaller"]
        for pkg in packages:
            try:
                if pkg == "pywebview":
                    import webview
                elif pkg == "pyinstaller":
                    result = subprocess.run(
                        [sys.executable, "-m", "PyInstaller", "--version"],
                        capture_output=True, text=True
                    )
                    if result.returncode != 0:
                        raise ImportError
                self.log(f"  ✓ {pkg} is available")
            except (ImportError, Exception):
                self.log(f"  ↓ Installing {pkg}...", "WARN")
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", pkg, "--quiet"],
                    check=True
                )
                self.log(f"  ✓ {pkg} installed successfully")

    def scan_html_assets(self, html_path: Path):
        """Scan HTML for referenced assets."""
        self.log("Scanning HTML for assets...")
        html_content = html_path.read_text(encoding="utf-8", errors="ignore")
        html_dir = html_path.parent

        assets = []
        patterns = [
            r'src=["\']([^"\'http][^"\']*)["\']',
            r'href=["\']([^"\'http][^"\'#?][^"\']*\.(css|js|ico|png|jpg|jpeg|gif|svg|woff|woff2|ttf|eot))["\']',
            r'url\(["\']?([^"\'http)][^"\')\s]*)["\']?\)',
        ]
        for pattern in patterns:
            matches = re.findall(pattern, html_content)
            for m in matches:
                asset = m if isinstance(m, str) else m[0]
                if asset and not asset.startswith(("http", "data:", "#", "javascript")):
                    asset_path = html_dir / asset
                    if asset_path.exists():
                        assets.append((asset, asset_path))
                        self.log(f"  Found asset: {asset}")

        return assets, html_content

    def build(self, html_path_str: str, app_name: str = "MyApp",
              icon_path: str = None, fullscreen: bool = False,
              width: int = 1200, height: int = 800,
              resizable: bool = True, on_top: bool = False):
        """Main build pipeline."""
        try:
            self.log("=" * 50)
            self.log(f"HTML TO EXE CONVERTER - Developed by BALAVIGNESH A")
            self.log("=" * 50)

            # --- Step 1: Validate ---
            self.set_status("Validating input...")
            self.set_progress(5)
            html_path = Path(html_path_str)
            if not html_path.exists():
                self.log(f"ERROR: HTML file not found: {html_path}", "ERROR")
                return False

            self.log(f"Input HTML: {html_path}")

            # --- Step 2: Dependencies ---
            self.set_status("Checking dependencies...")
            self.set_progress(10)
            self.ensure_dependencies()

            # --- Step 3: Prepare temp ---
            self.set_status("Preparing workspace...")
            self.set_progress(20)
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
            self.temp_dir.mkdir(parents=True, exist_ok=True)
            self.dist_dir.mkdir(parents=True, exist_ok=True)
            self.logs_dir.mkdir(parents=True, exist_ok=True)

            # --- Step 4: Copy assets ---
            self.set_status("Copying assets...")
            self.set_progress(30)
            assets, html_content = self.scan_html_assets(html_path)

            # Copy HTML
            dest_html = self.temp_dir / "index.html"
            shutil.copy2(html_path, dest_html)

            # Copy assets
            for asset_rel, asset_abs in assets:
                dest = self.temp_dir / asset_rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(asset_abs, dest)

            # Copy sibling folders (assets, images, scripts, css, js, etc.)
            html_dir = html_path.parent
            common_dirs = ["assets", "images", "img", "scripts", "js", "css",
                           "fonts", "icons", "media", "videos", "audio", "static"]
            for d in common_dirs:
                src = html_dir / d
                if src.exists() and src.is_dir():
                    dst = self.temp_dir / d
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                    self.log(f"  Copied folder: {d}/")

            self.log(f"  Total assets copied: {len(assets)}")

            # --- Step 5: Generate wrapper ---
            self.set_status("Generating app wrapper...")
            self.set_progress(50)
            self._generate_main_py(
                app_name=app_name,
                fullscreen=fullscreen,
                width=width,
                height=height,
                resizable=resizable,
                on_top=on_top
            )

            # --- Step 6: Build EXE ---
            self.set_status("Building EXE with PyInstaller...")
            self.set_progress(65)
            success = self._run_pyinstaller(app_name, icon_path)
            if not success:
                return False

            # --- Step 7: Copy EXE to dist ---
            self.set_status("Finalizing output...")
            self.set_progress(90)
            exe_src = self.temp_dir / "dist" / f"{app_name}.exe"
            if not exe_src.exists():
                # Try alternate path
                exe_src = self.temp_dir / "dist" / "main.exe"

            if exe_src.exists():
                exe_dst = self.dist_dir / f"{app_name}.exe"
                shutil.copy2(exe_src, exe_dst)
                self.log(f"  Output EXE: {exe_dst}")
            else:
                self.log("WARNING: EXE not found in expected path. Check dist/ folder.", "WARN")

            self.set_progress(100)
            self.set_status(f"✅ Build Complete! → dist/{app_name}.exe")
            self.log("=" * 50)
            self.log(f"BUILD SUCCESSFUL → dist/{app_name}.exe")
            self.log("=" * 50)
            return True

        except Exception as e:
            self.log(f"BUILD FAILED: {e}", "ERROR")
            self.set_status(f"❌ Build failed: {e}")
            import traceback
            self.log(traceback.format_exc(), "ERROR")
            return False

    def _generate_main_py(self, app_name, fullscreen, width, height, resizable, on_top):
        """Generate the PyWebView launcher script."""
        html_index = self.temp_dir / "index.html"
        html_abs = str(html_index).replace("\\", "/")

        script = f'''"""
{app_name} - Desktop Application
Developed by BALAVIGNESH A | HTML TO EXE CONVERTER
"""
import sys
import os
import webview

def get_html_path():
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "index.html")

def main():
    html_path = get_html_path()
    file_url = "file:///" + html_path.replace("\\\\", "/")

    window = webview.create_window(
        title="{app_name} | Developed by BALAVIGNESH A",
        url=file_url,
        width={width},
        height={height},
        resizable={resizable},
        fullscreen={fullscreen},
        on_top={on_top},
        min_size=(400, 300),
    )
    webview.start(debug=False)

if __name__ == "__main__":
    main()
'''
        main_py = self.temp_dir / "main.py"
        main_py.write_text(script, encoding="utf-8")
        self.log("  Generated main.py wrapper")

    def _run_pyinstaller(self, app_name: str, icon_path: str = None) -> bool:
        """Run PyInstaller to create the EXE."""
        main_py = self.temp_dir / "main.py"
        index_html = self.temp_dir / "index.html"

        # Build add-data list
        add_data_args = []

        # Add index.html
        add_data_args += ["--add-data", f"{index_html};."]

        # Add all other files/folders in temp
        for item in self.temp_dir.iterdir():
            if item.name in ("main.py", "index.html", "dist", "build", "__pycache__"):
                continue
            if item.is_dir():
                add_data_args += ["--add-data", f"{item};{item.name}"]
            elif item.is_file() and item.suffix not in (".py", ".spec"):
                add_data_args += ["--add-data", f"{item};."]

        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--noconsole",
            "--name", app_name,
            "--distpath", str(self.temp_dir / "dist"),
            "--workpath", str(self.temp_dir / "build"),
            "--specpath", str(self.temp_dir),
            "--hidden-import", "webview",
            "--hidden-import", "webview.platforms.winforms",
            "--hidden-import", "clr",
        ] + add_data_args

        if icon_path and Path(icon_path).exists():
            cmd += ["--icon", icon_path]
            self.log(f"  Using icon: {icon_path}")

        cmd.append(str(main_py))

        self.log(f"  Running PyInstaller...")
        self.log(f"  Command: {' '.join(cmd[:6])} ...")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(self.temp_dir)
        )

        if result.stdout:
            for line in result.stdout.splitlines()[-20:]:
                if line.strip():
                    self.log(f"  {line}")

        if result.returncode != 0:
            self.log("PyInstaller FAILED:", "ERROR")
            for line in result.stderr.splitlines()[-30:]:
                if line.strip():
                    self.log(f"  {line}", "ERROR")
            return False

        self.log("  PyInstaller build completed successfully")
        return True
