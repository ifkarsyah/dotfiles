"""Narration: the single source of truth for every spoken word.

Each scene is an ordered list of (beat_id, text). A beat is one animation
step: the scene wraps that step in `with self.beat("beat_id"):` and the step
lasts exactly as long as the spoken clip.

Audio is generated per TAKE (a group of scenes, kept under ~2,000 characters)
with a pause between beats, then split back into per-beat clips by
tools/split_narration.py.

Writing rules:
- Write for the ear: "partition one" not "p1", "the send call" not "send()".
  On-screen captions can use code; narration should not.
- One beat = one visual change. If the picture must change mid-sentence,
  split the sentence into two beats.
- Numbers you state are claims. Put each one in docs/ASSUMPTIONS.md.
- Changing a beat's text means regenerating that take.
"""

PAUSE = " [long pause] "   # eleven_v4 / v3 audio tag; see references/narration-and-voice.md

# ---------------------------------------------------------------- scenes

EXAMPLE_INTRO = [
    ("hook", "Every request you send crosses three systems before it's done."),
    ("flow", "A client, an API, and a database. Each one can fail on its own."),
    ("takeaway", "This series is about what happens in between."),
]

SCENES = {
    "ExampleIntro": EXAMPLE_INTRO,
}

# Which scenes/<file>.py each scene class lives in.
SCENE_FILES = {
    "ExampleIntro": "example",
}

# Playing order of each episode.
EPISODES = {
    "ep01": ["ExampleIntro"],
}

# Scenes generated together as one audio take (fewer files to download).
TAKES = {
    "ep01_a": ["ExampleIntro"],
}


def take_beats(take: str) -> list[tuple[str, str, str]]:
    """(scene, beat_id, text) for every beat in a take, in order."""
    if take in SCENES:          # a single scene can be its own take
        return [(take, b, t) for b, t in SCENES[take]]
    return [(sc, b, t) for sc in TAKES[take] for b, t in SCENES[sc]]


def take_text(take: str) -> str:
    """Exact text to send to TTS: every beat in the take, joined by pauses."""
    return PAUSE.join(t for _, _, t in take_beats(take))


if __name__ == "__main__":
    total = 0
    for name in TAKES:
        t = take_text(name)
        total += len(t)
        warn = "   <- over 2,000 chars, consider splitting" if len(t) > 2000 else ""
        print(f"{name}: {len(take_beats(name))} beats, {len(t)} chars{warn}")
    in_takes = {sc for scs in TAKES.values() for sc in scs}
    for ep, scenes in EPISODES.items():
        missing = [s for s in scenes if s not in in_takes]
        if missing:
            print(f"{ep}: scenes not in any take: {missing}")
        words = sum(len(t.split()) for sc in scenes for _, t in SCENES[sc])
        print(f"{ep}: {len(scenes)} scenes, {words} words, ~{words / 150:.1f} min spoken")
    print(f"total: {total} chars (≈ ElevenLabs credits at 1 credit/char)")
