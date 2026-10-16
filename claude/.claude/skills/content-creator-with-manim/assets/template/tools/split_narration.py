"""Split a narration take into one clip per beat.

Each take is generated with a long pause between beats (see
explainer_kit/narration.py). This finds every silence in the take,
picks the N-1 longest as beat boundaries (N = number of beats), cuts at the
middle of each, and writes:

    audio/<Scene>/<NN>_<beat_id>.wav
    audio/<Scene>/manifest.json      {beat_id: {"file": ..., "duration": ...}}

Picking the longest silences, rather than every silence over a threshold,
keeps natural mid-sentence pauses from splitting a beat.

A take covers one scene or a group of scenes (narration.TAKES); clips are
written to each scene's own folder.

Usage:
    python tools/split_narration.py ep01_a path/to/take.mp3
    python tools/split_narration.py ExampleIntro path/to/take.mp3
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from explainer_kit.narration import SCENES, TAKES, take_beats  # noqa: E402

NOISE_DB = -38      # quieter than this counts as silence
MIN_SIL = 0.30      # ignore gaps shorter than this
PAD = 0.12          # seconds of silence kept at each clip edge


def silences(path: Path):
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-af",
         f"silencedetect=noise={NOISE_DB}dB:d={MIN_SIL}", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    return list(zip(starts, ends))


def duration(path: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)]).decode())


def choose_boundaries(gaps, beats, total):
    """Pick len(beats)-1 pauses as boundaries.

    Longest-pauses-wins fails when a sentence-internal pause is as long as a
    real beat break. So each candidate is scored by both its length and how
    close it sits to where the boundary should be, judging by how much text
    comes before it. Dynamic programming finds the best ordered set.
    """
    import math
    need = len(beats) - 1
    chars = [len(b[-1]) for b in beats]
    pause_total = sum(e - s for s, e in sorted(gaps, key=lambda g: g[1] - g[0])[-need:])
    speech = total - pause_total
    avg_pause = pause_total / need
    expected, acc = [], 0
    for k in range(need):
        acc += chars[k]
        expected.append(speech * acc / sum(chars) + avg_pause * (k + 0.5))

    def cost(gap, k):
        mid = (gap[0] + gap[1]) / 2
        dev = (mid - expected[k]) / 3.0          # ~3 s tolerance
        return dev * dev - 4.0 * math.log(gap[1] - gap[0])

    n = len(gaps)
    INF = float("inf")
    best = [[INF] * n for _ in range(need)]
    back = [[-1] * n for _ in range(need)]
    for j in range(n):
        best[0][j] = cost(gaps[j], 0)
    for k in range(1, need):
        run, arg = INF, -1
        for j in range(n):
            if j >= 1 and best[k - 1][j - 1] < run:
                run, arg = best[k - 1][j - 1], j - 1
            if arg >= 0:
                best[k][j] = run + cost(gaps[j], k)
                back[k][j] = arg
    j = min(range(n), key=lambda j: best[need - 1][j])
    picks = []
    for k in range(need - 1, -1, -1):
        picks.append(gaps[j])
        j = back[k][j]
    return sorted(picks)


def main(take_name: str, take: str):
    beats = take_beats(take_name)          # [(scene, beat_id, text)]
    src = Path(take)
    total = duration(src)
    gaps = silences(src)
    # Leading/trailing silence are not boundaries.
    inner = [(s, e) for s, e in gaps if s > 0.05 and e < total - 0.05]
    need = len(beats) - 1
    if len(inner) < need:
        sys.exit(f"{take_name}: found {len(inner)} pauses, need {need}. "
                 "Lower MIN_SIL or regenerate with longer pauses.")

    chosen = choose_boundaries(inner, beats, total)
    lens = sorted(e - s for s, e in chosen)
    unused = sorted((e - s for s, e in inner if (s, e) not in chosen), reverse=True)
    print(f"{take_name}: {total:.1f}s, {len(beats)} beats; shortest boundary "
          f"{lens[0]:.2f}s, longest unused pause {unused[0] if unused else 0:.2f}s")

    # Clip k runs from the end of silence k-1 to the start of silence k.
    edges = [(0.0, None)] + chosen + [(None, total)]
    manifests: dict = {}
    for scene in dict.fromkeys(sc for sc, _, _ in beats):
        d = ROOT / "audio" / scene
        d.mkdir(parents=True, exist_ok=True)
        for old in d.glob("*.wav"):
            old.unlink()
        manifests[scene] = {}
    idx: dict = {}
    for k, (scene, beat_id, text) in enumerate(beats):
        start = max(0.0, edges[k][1] - PAD) if k else 0.0
        end = min(total, edges[k + 1][0] + PAD) if k < need else total
        n = idx.get(scene, 0)
        idx[scene] = n + 1
        f = ROOT / "audio" / scene / f"{n:02d}_{beat_id}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src),
                        "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
                        "-ac", "1", "-ar", "44100", str(f)], check=True)
        d = duration(f)
        manifests[scene][beat_id] = {"file": f.name, "duration": round(d, 3)}
        rate = len(text) / d
        flag = "  <- check" if not 9 <= rate <= 22 else ""
        print(f"  {scene:<22} {beat_id:<14} {d:5.2f}s  {rate:4.1f} ch/s{flag}")
    for scene, m in manifests.items():
        (ROOT / "audio" / scene / "manifest.json").write_text(json.dumps(m, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 3 or (sys.argv[1] not in SCENES and sys.argv[1] not in TAKES):
        sys.exit(f"usage: split_narration.py <take or scene> <take.mp3>\n"
                 f"takes: {', '.join(TAKES)}")
    main(sys.argv[1], sys.argv[2])
