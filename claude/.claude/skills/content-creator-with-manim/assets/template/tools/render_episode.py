"""Render an episode, stitch its scenes, and normalize narration loudness.

    .venv/bin/python tools/render_episode.py ep01          # 1080p60
    .venv/bin/python tools/render_episode.py ep01 -ql      # quick preview

Scene order comes from narration.EPISODES; scene files from SCENE_FILES.
Writes output/<episode>_<res>.mp4.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from explainer_kit.narration import EPISODES, SCENE_FILES  # noqa: E402

RES = {"-ql": "480p15", "-qm": "720p30", "-qh": "1080p60", "-qk": "2160p60"}


def main(episode: str, quality: str = "-qh"):
    scenes = EPISODES[episode]
    manim = ROOT / ".venv" / "bin" / "manim"
    by_file: dict = {}
    for scene in scenes:
        by_file.setdefault(SCENE_FILES[scene], []).append(scene)
    for module, group in by_file.items():
        subprocess.run([str(manim), quality, "--verbosity", "WARNING", f"scenes/{module}.py", *group], cwd=ROOT, check=True)

    res = RES[quality]
    parts = [ROOT / "media" / "videos" / SCENE_FILES[s] / res / f"{s}.mp4" for s in scenes]
    missing = [p for p in parts if not p.exists()]
    if missing:
        sys.exit(f"missing renders: {missing}")
    (ROOT / "output").mkdir(exist_ok=True)
    out = ROOT / "output" / f"{episode}_{res}.mp4"
    with tempfile.TemporaryDirectory() as tmp:
        lst = Path(tmp) / "list.txt"
        lst.write_text("".join(f"file '{p}'\n" for p in parts))
        stitched = Path(tmp) / "stitched.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                        "-i", str(lst), "-c", "copy", str(stitched)], check=True)
        # TTS audio is often ~-27 dB; normalize to -16 LUFS (standard for online video).
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(stitched), "-c:v", "copy",
                        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k",
                        str(out)], check=True)
    print(out)


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in EPISODES:
        sys.exit(f"usage: render_episode.py <episode> [-ql|-qm|-qh|-qk]; episodes: {', '.join(EPISODES)}")
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "-qh")
