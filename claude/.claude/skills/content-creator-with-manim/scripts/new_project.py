"""Scaffold a new narrated-explainer project from the skill's template.

    python <skill>/scripts/new_project.py <target_dir> --series "Streaming Systems" --tag 101

Copies assets/template/ to <target_dir>, sets the series name, creates a
virtualenv and installs Manim into it (skip with --no-venv). Refuses to
overwrite a non-empty directory.
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parents[1] / "assets" / "template"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--series", default="Series Name")
    ap.add_argument("--tag", default="101")
    ap.add_argument("--no-venv", action="store_true")
    a = ap.parse_args()

    dst = Path(a.target).resolve()
    if dst.exists() and any(dst.iterdir()):
        sys.exit(f"{dst} exists and is not empty")
    shutil.copytree(TEMPLATE, dst, dirs_exist_ok=True)
    for p in (dst / "tools").glob("*.sh"):
        p.chmod(0o755)

    style = dst / "explainer_kit" / "style.py"
    s = style.read_text()
    s = s.replace('SERIES_NAME = "Series Name"', f'SERIES_NAME = {a.series!r}')
    s = s.replace('SERIES_TAG = "101"', f'SERIES_TAG = {a.tag!r}')
    style.write_text(s)

    if not a.no_venv:
        # A venv avoids old system setuptools breaking Manim's `srt` dependency.
        subprocess.run([sys.executable, "-m", "venv", str(dst / ".venv")], check=True)
        pip = dst / ".venv" / "bin" / "pip"
        subprocess.run([str(pip), "install", "-q", "--upgrade", "pip", "setuptools", "wheel"], check=True)
        r = subprocess.run([str(pip), "install", "-q", "-r", str(dst / "requirements.txt")])
        if r.returncode:
            print("Manim install failed. Usually missing system packages: "
                  "libcairo2-dev libpango1.0-dev pkg-config ffmpeg (see references/setup.md).")
            sys.exit(1)
    print(f"project ready: {dst}")


if __name__ == "__main__":
    main()
