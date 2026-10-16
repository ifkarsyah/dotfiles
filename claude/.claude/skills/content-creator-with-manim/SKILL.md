---
name: content-creator-with-manim
description: Create narrated, 3Blue1Brown-style animated explainer videos with Manim, voiced in the user's own cloned ElevenLabs voice and synced sentence by sentence to the animation. Use this whenever the user wants to make or continue an educational or technical video, YouTube explainer, series episode, or animated walkthrough of how a system works or fails (Kafka, databases, networking, ML systems...), wants a script turned into a narrated animation, or asks for "the next episode/chapter" of their series, even if they don't name Manim. Manim fits animated diagrams, flows and step-by-step mechanics; if a sibling content-creator-with-* skill matches the request's medium better (talking head, screen recording, slides), prefer that one.
---

# Content creator with Manim: narrated explainer videos

Turns a topic into a finished, narrated explainer episode: planned chapters, narration written for the ear, Manim scenes whose timing is driven by the audio, the user's cloned voice from ElevenLabs, and a reviewed 1080p render.

The core idea, learned the hard way: **audio drives timing**. Guessing `wait()` times and recording narration later never lines up. Every animation step lives inside a narration *beat*, and each beat lasts exactly as long as its spoken clip.

## What's bundled

- `scripts/new_project.py` scaffolds a working project (style system, components, `NarratedScene`, tools, docs, a runnable example scene).
- `assets/template/` is that project. Read `explainer_kit/components.py` once before building scenes; it has boxes, packets, logs, tables, timelines, badges, captions, and `flow()` for left-to-right system diagrams.
- References, read when you reach that stage:
  - `references/narration-and-voice.md`: writing beats, generating takes in ElevenLabs, getting audio into the workspace, splitting.
  - `references/visual-pitfalls.md`: the layout and Manim bugs that showed up in review, and their fixes. Read before building scenes.
  - `references/setup.md`: installing Manim and its system dependencies.

## Workflow

Use a task list; this is long work and the user may step away.

### 1. Scaffold

```bash
python <skill-dir>/scripts/new_project.py <project-dir> --series "Streaming Systems" --tag 101
```

If Manim fails to install, see `references/setup.md` (usually missing Pango headers). Continuing an existing project? Skip this, and read its `explainer_kit/narration.py` and `docs/PLAN.md` first.

### 2. Plan the episode

Fill in `docs/PLAN.md`. Viewers need three things in the first minute, so a first episode is shaped like this:

1. **Hook** (10 to 20 s): a concrete failure the audience recognizes, shown, not told. "A customer pays $100 once; the dashboard says $200; every component is green."
2. **What this series is and who it's for** (one sentence each).
3. **System overview**: one happy-path pass through the system being explained.
4. **Roadmap**: every chapter placed on the part of the system it covers, ending on "today: chapter 1".
5. **The chapter itself**, then a short recap and a teaser for the next episode.

Later episodes: a 10 to 15 s cold open with that chapter's failure, a one-line recap, then the chapter.

Two things to settle with the user before generating audio, because changing them later costs credits:
- **Chapter numbering.** The roadmap is a public promise. If chapters might be cut, show only the sure ones.
- **Length.** About 150 spoken words per minute; animation adds roughly 10% on top. A chapter of 6 to 9 minutes holds attention; a single 80-minute video does not. Recommend a series.

Fix a **system model** (versions, configs, the example data) and keep it constant across scenes. When a scene changes an assumption (say `acks=1`), show it on screen with `config_chip()` before the behavior happens.

### 3. Write the narration

All spoken text goes in `explainer_kit/narration.py`, one list of `(beat_id, text)` per scene. Read `references/narration-and-voice.md` for the rules; the short version:

- One beat = one visual change. Split sentences where the picture must change.
- Write for the ear: "partition one", "the send call". On-screen captions may use code; narration should not.
- Group scenes into TAKES of ≤ ~2,000 characters each (fewer files for the user to download).

Then run `.venv/bin/python -m explainer_kit.narration` for beat counts, characters per take (≈ credits) and spoken minutes.

**Verify every factual claim before generating audio.** Defaults, version numbers, guarantees: look them up in official docs (they change; e.g. Kafka's `linger.ms` default went 0 → 5 in 4.0) and record each in `docs/ASSUMPTIONS.md`. Re-recording a wrong number costs money and time; a wrong claim in a published explainer costs credibility.

### 4. Build the scenes

Read `references/visual-pitfalls.md` first. Then, per scene:

- Subclass `NarratedScene`; wrap each step in `with self.beat("id") as d:`, beats in the same order as `narration.py`. `d` is the clip length: spread motion across the sentence with it instead of front-loading everything.
- Use colors by meaning from `style.py` (`S.FAILURE`, `S.DUPLICATE`, ...), never raw hex. Never rely on color alone: duplicates also get a dashed outline, failures a cross.
- Use `Narrator` for the caption line (it cross-fades; text-to-text morphs garble).
- Keep the main system diagram at the same positions across scenes.

Scenes render without audio (estimated timing) until clips exist, so build and review visuals while the voice is being generated.

**Review every scene visually.** Render at `-ql`, make a contact sheet, and look at it:

```bash
tools/contact_sheet.sh media/videos/<file>/480p15/<Scene>.mp4 sheet.png 2.5 5
```

Read the PNG. Look for text on text, moving objects covering labels, things vanishing when a box animates, and anything off-frame. When a frame looks wrong, extract that exact moment before "fixing" it (sheets sample every few seconds and can catch a mid-transition frame):

```bash
ffmpeg -v error -y -i <video> -vf "select='between(t,3,9)',fps=2,scale=480:-1,tile=4x3" -frames:v 1 check.png
```

### 5. Generate the narration in the user's voice

Follow `references/narration-and-voice.md`. In short: find the user's **cloned** voice via the ElevenLabs connector (it appears with `category: cloned`, often named "My Voice <date>"; a name search finds library voices instead), create one flow, generate one take per TAKE with `eleven_v4` and `generations_count: 1`, poll until done.

If the workspace can't reach the audio URLs (check once with curl; blocked hosts fail with a 403 CONNECT error), send the user the links with a note that they expire in about 2 hours, plus the flow link as a fallback, and ask them to attach the mp3s. Match the files to takes by duration.

### 6. Split and sync

```bash
cp <attached>.mp3 audio/takes/<take>.mp3
.venv/bin/python tools/split_narration.py <take> audio/takes/<take>.mp3
```

Every clip prints its speaking rate. Normal is about 12 to 19 characters per second; outliers (`<- check`) mean a cut landed in the wrong place. Very short beats ("So it retries.") can read low because of fixed padding, which is fine.

### 7. Fix pacing

```bash
.venv/bin/python tools/pacing_report.py <episode>
```

- **OVERRUN** (animation longer than its sentence): always fix by shortening run times.
- **HOLD > ~5.5 s mid-scene** (picture frozen while the voice continues): add a second motion timed to the words that refer to it: `self.wait(x)` then an `Indicate` on text/tokens or a `Circumscribe` on boxes. Holds on closing takeaway cards are fine.

Re-run until clean, then re-check the changed scenes' contact sheets.

### 8. Render, verify, deliver

```bash
.venv/bin/python tools/render_episode.py <episode>      # stitched + loudness-normalized
```

A 9-minute episode takes ~20 to 30 minutes at 1080p60; run it in the background and keep working. Then verify:
- audio and video stream durations match (audio may end ~1 s early on the final fade);
- loudness is consistent across the episode (`volumedetect` at a few timestamps);
- a contact sheet of the whole episode at 20 s intervals shows scenes in order with no broken frames.

Deliver the video with the file-sending tool. Zip the project without `.venv`, `media`, `output` and the per-beat `.wav` clips (they regenerate from the takes); the upload limit is about 30 MB.

## Reporting to the user

Lead with what they get and its length. Mention what you can't check yourself: you can see frames but cannot hear audio, so ask them to listen for clipped words at beat boundaries. List open technical claims from `ASSUMPTIONS.md` before they publish. Mention credits spent on generations.
