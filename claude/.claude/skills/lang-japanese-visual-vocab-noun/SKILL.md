---
name: "lang-japanese-visual-vocab-noun"
description: "Build an illustrated Japanese vocabulary artifact for a real-life place or situation (station, shop, hospital, arriving in Tokyo, seasons): hover scenes, kana readings, Kokoro audio, study and quiz."
---

# Japanese visual vocabulary artifacts (nouns by place or situation)

Renamed from `lang-japanese-visual-vocabulary`. Siblings: `lang-japanese-visual-vocab-verb` (daily routines) and `lang-japanese-visual-vocab-adjective` (pairs and forms). The general strategy for choosing what to learn is in `lang-general-mining-vocabulary`.

Output: one private claude.ai artifact per place (home, train station, restaurant, school, grocery store, hospital and so on). Each has one tab per sub-place. Each tab is a flat vector scene in which every word is a hoverable object (tooltip: kanji, kana reading, English). Plus Study and Quiz modes, a "Find it" chip row, a Cards view, saved progress and pre-generated Kokoro audio.

## Learner rules (always)
- Ferdi reads hiragana and katakana. **No romaji anywhere**: not in the data, the tooltips, the header or the cards.
- English glosses must be unambiguous. Example: "rice bowl (the container)", because ごはん is the rice itself.
- Few em dashes in any page text or reply. Be honest about what is unverified.
- Tell him if a word, reading or assumption looks wrong rather than going along. Examples of past catches: uncertain bank fees, conflicting deadlines, loose antonym pairs.
- Code examples in Python, notes in Markdown.

## Where the working assets are
The reusable template and scripts are saved in the Project "Learn 日本語" under the `visual-vocab/` path: `template.html`, `helpers.js`, `build_place.py`, `harness.js`, `check.py`, `audio.py`, `example_scenes.js`, `example_data.js`, `BRIEF.md`. Read them with `project_read` (large text is written to a local file). Put them in one directory `shared/` inside the working directory, and per place create `<place>/{meta.json,data.js,scenes.js}`. `project_write` only accepts `local_path` inside the working directory.
If the Project is not attached or the files are missing, say so and rebuild from the design below, or ask Ferdi to attach the project.

In `audio.py` edit the `base` path to the directory that holds `venv/` and `kokoro-models/`.

## One-time setup in a fresh sandbox (audio)
- `python3 -m venv venv` then `pip install kokoro-onnx soundfile` plus the Japanese frontend (`misaki[ja]`, which brings fugashi, unidic-lite and jaconv). Needs ffmpeg with libmp3lame.
- Model files come from GitHub, because Hugging Face is blocked in the sandbox: `https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx` and `.../voices-v1.0.bin` (same release folder). Put them in `kokoro-models/`.
- Voice `jf_alpha`, speed 0.9, `lang="ja"`. Clips are trimmed, loudness-normalised, mono 24 kHz 48 kbps mp3, embedded as base64 in `audio-data.js` (about 6 to 9 KB per word). Other Japanese voices: jf_gongitsune, jf_nezumi, jf_tebukuro, jm_kumo.
- Kokoro cannot run inside the page (the artifact blocks fetch), so audio is always pre-generated and embedded. The page falls back to the device `ja-JP` speech voice if a clip fails.
- `audio.py` reads `words.json` (rows `{jp, kana}`, key = kana or jp) plus an optional `overrides.json` (key to the text actually synthesised). The spoken text is the kana reading.
- A "・" inside a phrase makes Kokoro produce clips of about 9 seconds. Replace it with "、" or reword. Check the longest clips in `audio_report.json` (keep them under about 5 seconds).
- You cannot listen to the clips. Always say the audio is unverified and ask Ferdi to spot-check, especially rare readings.

## Data model
`data.js` defines `var ROOMS = [...]`. Each tab: `id`, `scene: true`, `tab`, `tabJp`, `jp`, `en`, `note` (one or two sentences with a real usage point), `sections: [{ items: [[jp, kana, "", english, emoji], ...] }]`. The third slot stays empty. `kana` is the reading, or `""` only for words that are already pure kana. It is also what the audio says. Word ids are `<tabId>:<index>` in item order. Aim for 7 to 14 words per tab, 3 to 5 tabs per place.

`scenes.js` has one function per tab, built from the helpers `R C E P T HIT wrapSvg shell` and `hot(room, n, inner)`, plus `var SCENES = { tabId: tabIdSvg, ... }`. `meta.json`: `{title (2 to 4 words), h1jp, h1ro (plain English), key, kicker}`.

## Drawing rules
- Flat style with the palette classes (`f-wall f-floor f-wood f-glass f-red f-blue f-yellow f-green f-orange f-train f-brick f-metal f-tv f-screen ...`). A CSS class beats an attribute, so never mix them on one shape. Inline colours only for small signs and food.
- Outdoor and nature scenes (sky, plants, sea) need inline colours. Use small local helpers that write `fill` attributes (rect, circle, ellipse, path, stroke path, a sky gradient with a unique id per scene, a standing person, a seated person) and keep the hotspot rules below unchanged.
- Exactly one hotspot per word, each starting with a `HIT(x,y,w,h)` rectangle at least about 30 px each way. Never nest hotspot groups. Draw big things first, small things on top (later siblings win overlaps).
- Abstract words (procedures, symptoms, events, prices) become signs, banners, forms, price tags, speech bubbles, body diagrams or device screens.
- Text on signs with `T(x,y,size,text,fill)`. Check that size times character count fits the sign. No brand logos, real company names or known characters or mascots.
- Past mistakes to look for: overlapping bicycle wheels, a handrail floating away from stairs, thin diagonal objects that vanish, text overflowing a sign, objects with no ground contact, a phone shelf hidden behind a board, a grey strip where a translucent band meets a gradient.

## Workflow
1. Settle the sub-places and word list. If the request is clear, start. Split a place when it mixes unrelated vocabularies (for example park, shrine and temple, amusement park).
2. Write `meta.json`, `data.js`, `scenes.js`.
3. Run `python3 -I check.py <placeDir>`. It builds `index.html`, validates every scene (XML plus one hotspot per word), writes `words.json`, takes screenshots into `shots/` (including dark mode) and tests hover, cards, phone overflow and page errors. **Open every PNG with Read and look at it**, fix, re-run. Up to 4 rounds.
4. Run `python3 -I audio.py <placeDir>`. Use an optional `overrides.json` for readings Kokoro would mispronounce, for example a lone は read as "wa" (key `はブラシ` maps to `ハブラシ`).
5. Publish a NEW artifact: `file_path` = `index.html`, `files = {"audio-data.js": <path>}`, `capabilities = {"db": {}, "user": {}}` (progress is saved per viewer in a private db doc with localStorage as fallback), a generic `icon` word, and a one-sentence `description`. To update later, pass the artifact `url`.
6. Final message: what the page is, word counts per tab, what is unverified (audio, readings, any drawing flaw you know of). Do not paste the artifact URL unless asked.

## Extension A: situation pages (example: Arriving in Tokyo)
The same engine works for a life situation instead of a place, when each tab is a stage and needs more than nouns. The Tokyo arrival page had five tabs: airport, ward office, housing, utilities and phone, money. Add an `EXTRAS[tabId]` layer under each scene:
- `steps`: the journey in order, `{pic, jp, en, note?}`, shown as a numbered strip.
- `docs`: rows of document fields or checklist items, `{title, en, note?, check?, rows:[{jp, en, val?}]}`. Never reproduce a real form. Label sample documents as study diagrams with a 見本 stamp.
- `phrases`: `{jp, en}` things the learner says.
- `dialogues`: `{title, en, them: emoji, lines:[{who: "you"|"them", jp, en}]}`. In Quiz mode the learner's own lines blur until tapped. A Play all button plays the lines in sequence.
Markup `{漢字|かんじ}` gives furigana. A furigana toggle sits next to Hide learned. The audio key is the plain display text and the spoken text is derived from the markup, so one source feeds both. A `dump.js` writes `words.json` and `overrides.json` from data plus extras and reports problems (unbalanced braces, latin letters, extras for an unknown tab, key clashes).

Implementation: copy the template and patch it with a `build.py` that asserts each marker occurs exactly once. Swap the data block (from `  // Word format:` to `  var INDEX = {};`) and the helpers and scenes block (from `  /* Small drawing helpers */` to `  function viewSwitch() {`). Add journey HTML before `viewSwitch()`, and `extrasHtml(r)` after the scene and after the cards. Insert the extras functions before `  /* Rendering */` and the extras events before `  var foot = ...`. Put `.xq` on elements that should blur in Quiz mode and `data-xsay` on anything that speaks.

Content rules for a situation page: cover the core only (about 5 tabs), flag fees, deadlines and procedures as typical examples that differ by ward, employer or bank, and keep a footer saying it is a study aid, not official guidance. If a source gives conflicting figures, show a range and tell Ferdi to confirm.

## Extension B: season pages (example: Four Seasons of Japan)
Four tabs (春 夏 秋 冬), each with a scene of 12 to 13 hotspots, then the same extras layer with a different meaning: `steps` become "Best things to do" (six activities with when and where in the note, numbers and arrows hidden), `docs` become a calendar with typical dates in `val` plus a seasonal food or sayings list (no stamp), plus phrases and one dialogue. Typical dates (blossom, leaves, climbing season, festivals) must be marked as typical and checked against current sources before you state them as fact.

## Doing several places at once
Write one `spec.md` per place (title strings, icon, suggested sub-places and vocabulary) and give each parallel agent `BRIEF.md` plus its spec. Each agent works only in its own directory and ends with a five-line report: URL, tabs and word counts, changes from the suggested vocabulary, unverified items, known visual flaws. Then spot-check a few screenshots yourself and summarise. A past run built ten places this way in about 12 minutes. Machine limit to remember: 2 CPUs, 8 GB RAM.

## Existing artifacts (Ferdi's account)
Places: Home (Ie no Tango), Station Words, Restaurant, Government Office, School, Park, Shrine and Temple, Amusement Park, Grocery Store, Electronics Store, Convenience Store, Hospital and Pharmacy. Situations: Arriving in Tokyo. Seasons: Four Seasons of Japan. Use the artifact list action to find the links. The files for the Tokyo and seasons pages were not saved to the Project, so rebuild them from Extension A and B if needed.

## Next candidates
A Berlin arrival page in German (same layout, German article and plural instead of kana), and a shared concept layer so a word learned in one language is reused in the next.