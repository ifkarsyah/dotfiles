# Narrated explainer project

Made from the `content-creator-with-manim` skill.

```bash
.venv/bin/python -m explainer_kit.narration            # beats, chars per take, est. minutes
.venv/bin/manim -pql scenes/example.py ExampleIntro     # render one scene
.venv/bin/python tools/pacing_report.py ep01            # overruns / long holds
.venv/bin/python tools/split_narration.py ep01_a audio/takes/ep01_a.mp3
.venv/bin/python tools/render_episode.py ep01           # 1080p, stitched, loudness-normalized
tools/contact_sheet.sh media/videos/example/480p15/ExampleIntro.mp4 sheet.png 2.5 5
```

Layout:
- `explainer_kit/` style, components, narration (all spoken text), voice (NarratedScene)
- `scenes/` one file per episode part
- `audio/takes/` raw TTS takes; `audio/<Scene>/` per-beat clips + manifest (generated)
- `docs/` PLAN, ASSUMPTIONS
