"""
HTML to EXE Converter - CLI Mode
Developed by BALAVIGNESH A

Usage:
    python build_cli.py input/index.html
    python build_cli.py input/index.html --name MyApp --width 1280 --height 720
    python build_cli.py input/index.html --fullscreen --icon app.ico
"""

import argparse
import sys
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="HTML to EXE Converter CLI — Developed by BALAVIGNESH A",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("html", help="Path to the HTML file")
    parser.add_argument("--name",       default="MyApp",    help="Output EXE name (default: MyApp)")
    parser.add_argument("--icon",       default=None,       help="Path to .ico icon file")
    parser.add_argument("--width",      type=int, default=1200, help="Window width (default: 1200)")
    parser.add_argument("--height",     type=int, default=800,  help="Window height (default: 800)")
    parser.add_argument("--fullscreen", action="store_true",    help="Launch in fullscreen")
    parser.add_argument("--no-resize",  action="store_true",    help="Disable window resize")
    parser.add_argument("--on-top",     action="store_true",    help="Always on top")

    args = parser.parse_args()

    os.chdir(Path(__file__).parent)
    Path("logs").mkdir(exist_ok=True)

    from builder import BuildEngine

    print("\n" + "=" * 55)
    print("  HTML TO EXE CONVERTER  |  Developed by BALAVIGNESH A")
    print("=" * 55 + "\n")

    engine = BuildEngine()
    success = engine.build(
        html_path_str=args.html,
        app_name=args.name,
        icon_path=args.icon,
        fullscreen=args.fullscreen,
        width=args.width,
        height=args.height,
        resizable=not args.no_resize,
        on_top=args.on_top
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
