"""Render an episode's scenes at preview quality and report pacing problems.

    .venv/bin/python tools/pacing_report.py ep01
    .venv/bin/python tools/pacing_report.py ep01 KeyOrdering Batching   # only these

Reports, per beat:
  OVERRUN  the animation runs longer than its narration (picture lags voice)
  HOLD     the picture is still for > 4 s while narration continues

Fix overruns always. Fix mid-scene holds over ~5.5 s by adding a second motion
timed to the words that refer to it. Holds on closing takeaway cards are fine.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from explainer_kit.narration import EPISODES, SCENE_FILES  # noqa: E402


def main(episode: str, only: list[str]):
    scenes = [s for s in EPISODES[episode] if not only or s in only]
    by_file: dict = {}
    for s in scenes:
        by_file.setdefault(SCENE_FILES[s], []).append(s)
    manim = ROOT / ".venv" / "bin" / "manim"
    log = ""
    for module, group in by_file.items():
        r = subprocess.run([str(manim), "-ql", f"scenes/{module}.py", *group], cwd=ROOT,
                           capture_output=True, text=True)
        log += r.stdout + r.stderr
        if r.returncode:
            print(log[-3000:])
            sys.exit(f"render failed in scenes/{module}.py")
    flat = re.sub(r"\s+", " ", log)
    holds = re.findall(r"HOLD beat '([\w]+)': ([\d.]+)s", flat)
    overruns = re.findall(r"beat '([\w]+)': animation ([\d.]+)s runs ([\d.]+)s", flat)
    silent = re.findall(r"(\w+): no narration found", flat)
    for b, a, over in overruns:
        print(f"OVERRUN {b:<20} animation {a}s, {over}s past narration")
    for b, h in holds:
        mark = "  <- fix" if float(h) > 5.5 else ""
        print(f"HOLD    {b:<20} {h}s still{mark}")
    for s in silent:
        print(f"SILENT  {s:<20} no audio manifest; timing is estimated")
    if not (holds or overruns):
        print("pacing OK")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in EPISODES:
        sys.exit(f"usage: pacing_report.py <episode> [Scene ...]; episodes: {', '.join(EPISODES)}")
    main(sys.argv[1], sys.argv[2:])
