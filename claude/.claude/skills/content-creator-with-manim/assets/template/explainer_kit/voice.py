"""Audio-driven timing.

A NarratedScene plays its narration one beat at a time. Inside
`with self.beat("id"):` the animations run while the clip plays, and the
block does not end until the clip has finished (plus a short breath). So the
audio sets the pace, and no scene needs hand-tuned wait() values.

If audio/<Scene>/manifest.json does not exist yet (no narration generated),
beats fall back to an estimated speaking time so the scene still renders,
silently, with roughly the right pacing.
"""

from __future__ import annotations

import json
from contextlib import contextmanager
from pathlib import Path

from manim import Scene, logger

from .narration import SCENES

AUDIO_DIR = Path(__file__).resolve().parents[1] / "audio"
WORDS_PER_SEC = 2.6   # fallback estimate only
BREATH = 0.35         # pause after each beat before the next one starts


class NarratedScene(Scene):
    #: key into narration.SCENES; defaults to the class name
    narration_key: str | None = None

    def setup(self):
        key = self.narration_key or type(self).__name__
        self._beats = dict(SCENES[key])
        self._order = [b for b, _ in SCENES[key]]
        self._used: list[str] = []
        manifest = AUDIO_DIR / key / "manifest.json"
        self._audio = None
        if manifest.exists():
            self._audio = json.loads(manifest.read_text())
            self._audio_dir = manifest.parent
        else:
            logger.warning(f"{key}: no narration found at {manifest}; "
                           "rendering silently with estimated timing.")

    def beat_duration(self, beat_id: str) -> float:
        if self._audio:
            return self._audio[beat_id]["duration"]
        return len(self._beats[beat_id].split()) / WORDS_PER_SEC + 0.3

    @contextmanager
    def beat(self, beat_id: str):
        expected = self._order[len(self._used)] if len(self._used) < len(self._order) else None
        if beat_id != expected:
            raise ValueError(f"beat {beat_id!r} played out of order; expected {expected!r}")
        self._used.append(beat_id)

        start = self.renderer.time
        dur = self.beat_duration(beat_id)
        if self._audio:
            self.add_sound(str(self._audio_dir / self._audio[beat_id]["file"]))
        yield dur
        elapsed = self.renderer.time - start
        remaining = dur + BREATH - elapsed
        if remaining > 4.0:
            logger.info(f"HOLD beat {beat_id!r}: {remaining:.1f}s with no motion "
                        f"(animation {elapsed:.1f}s of {dur:.1f}s narration)")
        if remaining > 0.02:
            self.wait(remaining)
        elif elapsed > dur + 0.5:
            logger.warning(f"beat {beat_id!r}: animation {elapsed:.1f}s runs "
                           f"{elapsed - dur:.1f}s past its narration")

    def tear_down(self):
        missing = [b for b in self._order if b not in self._used]
        if missing:
            logger.warning(f"beats never played: {missing}")
        super().tear_down()
