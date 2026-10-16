# Setup

Manim Community Edition (`pip install manim`), not ManimGL (`github.com/3b1b/manim`, a different API). Projects pin `manim>=0.19,<0.23` in `requirements.txt`.

## System packages

| Need | Debian/Ubuntu | macOS |
|---|---|---|
| Cairo, Pango headers | `libcairo2-dev libpango1.0-dev pkg-config` | `brew install cairo pango pkg-config` |
| Video | `ffmpeg` | `brew install ffmpeg` |
| Fonts | `fonts-inter fonts-dejavu` | `brew install --cask font-inter` |

LaTeX is not needed: all text uses Pango (`Text`), not `MathTex`.

## Known install failures

| Error | Fix |
|---|---|
| `pangocairo >= 1.30.0 is required` | install `libpango1.0-dev` (apt) or `pango` (brew) |
| `Failed building wheel for srt` | old system setuptools; use a venv and `pip install --upgrade pip setuptools wheel` first (`new_project.py` does this) |
| Text in a fallback font | install Inter, or change `FONT` in `style.py` |

## Sandboxes

Package registries are usually reachable; arbitrary hosts (ElevenLabs storage, docs sites via curl) often aren't. Use WebFetch for docs. See `narration-and-voice.md` §4 for getting audio in.
