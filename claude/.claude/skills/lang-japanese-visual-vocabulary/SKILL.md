---
name: "lang-japanese-visual-vocabulary"
description: "Build an illustrated Japanese vocabulary artifact for a real-life place (station, shop, hospital): hover scene per sub-place, kana readings, Kokoro audio, study and quiz modes."
---

# Japanese visual vocabulary artifacts

Output: one private claude.ai artifact per place (home, train station, restaurant, school, grocery store, hospital and so on). Each has one tab per sub-place. Each tab is a flat vector scene in which every word is a hoverable object (tooltip: kanji, kana reading, English). Plus Study and Quiz modes, a "Find it" chip row, a Cards view, saved progress and pre-generated Kokoro audio.

## Learner rules (always)
- Ferdi reads hiragana and katakana. **No romaji anywhere**: not in the data, the tooltips, the header or the cards.
- English glosses must be unambiguous. Example: "rice bowl (the container)", because ごはん is the rice itself.
- No em dashes in any page text. Be honest about what is unverified.
- Tell him if a word, reading or assumption looks wrong rather than going along.

## Where the working assets are
The reusable template and scripts are saved in the Project "Learn 日本語" under the `visual-vocab/` path: `template.html`, `helpers.js`, `build_place.py`, `harness.js`, `check.py`, `audio.py`, `example_scenes.js`, `example_data.js`, `BRIEF.md`. Read them with `project_read` (large text is written to a local file). Put them in one directory `shared/` inside the working directory, and per place create `<place>/{meta.json,data.js,scenes.js}`. `project_write` only accepts `local_path` inside the working directory.
If the Project is not attached or the files are missing, say so and rebuild from the design below, or ask Ferdi to attach the project.

In `audio.py` edit the `base` path to the directory that holds `venv/` and `kokoro-models/`.

## One-time setup in a fresh sandbox (audio)
- `python3 -m venv venv` then `pip install kokoro-onnx soundfile` plus the Japanese frontend (`misaki[ja]`, which brings fugashi, unidic-lite and jaconv). Needs ffmpeg with libmp3lame.
- Model files come from GitHub, because Hugging Face is blocked in the sandbox: `https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx` and `.../voices-v1.0.bin` (same release folder). Put them in `kokoro-models/`.
- Voice `jf_alpha`, speed 0.9, `lang="ja"`. Clips are trimmed, loudness-normalised, mono 24 kHz 48 kbps mp3, embedded as base64 in `audio-data.js` (about 6 to 9 KB per word). Other Japanese voices: jf_gongitsune, jf_nezumi, jf_tebukuro, jm_kumo.
- Kokoro cannot run inside the page (the artifact blocks fetch), so audio is always pre-generated and embedded. The page falls back to the device `ja-JP` speech voice if a clip fails.
- You cannot listen to the clips. Always say the audio is unverified and ask Ferdi to spot-check, especially rare readings.

## Data model
`data.js` defines `var ROOMS = [...]`. Each tab: `id`, `scene: true`, `tab`, `tabJp`, `jp`, `en`, `note` (one or two sentences with a real usage point), `sections: [{ items: [[jp, kana, "", english, emoji], ...] }]`. The third slot stays empty. `kana` is the reading, or `""` only for words that are already pure kana. It is also what the audio says. Word ids are `<tabId>:<index>` in item order. Aim for 7 to 14 words per tab, 3 to 5 tabs per place.

`scenes.js` has one function per tab, built from the helpers `R C E P T HIT wrapSvg shell` and `hot(room, n, inner)`, plus `var SCENES = { tabId: tabIdSvg, ... }`. `meta.json`: `{title (2 to 4 words), h1jp, h1ro (plain English), key, kicker}`.

## Drawing rules
- Flat style with the palette classes only (`f-wall f-floor f-wood f-glass f-red f-blue f-yellow f-green f-orange f-train f-brick f-metal f-tv f-screen ...`). A CSS class beats an attribute, so never mix them on one shape. Inline colours only for small signs and food.
- Exactly one hotspot per word, each starting with a `HIT(x,y,w,h)` rectangle at least about 30 px each way. Never nest hotspot groups. Draw big things first, small things on top (later siblings win overlaps).
- Abstract words (procedures, symptoms, events, prices) become signs, banners, forms, price tags, speech bubbles, body diagrams or device screens.
- Text on signs with `T(x,y,size,text,fill)`. Check that size times character count fits the sign. No brand logos, real company names or known characters or mascots.
- Past mistakes to look for: overlapping bicycle wheels, a handrail floating away from stairs, thin diagonal objects that vanish, text overflowing a sign, objects with no ground contact.

## Workflow
1. Settle the sub-places and word list. If the request is clear, start. Split a place when it mixes unrelated vocabularies (for example park, shrine and temple, amusement park).
2. Write `meta.json`, `data.js`, `scenes.js`.
3. Run `python3 -I check.py <placeDir>`. It builds `index.html`, validates every scene (XML plus one hotspot per word), writes `words.json`, takes screenshots into `shots/` (including dark mode) and tests hover, cards, phone overflow and page errors. **Open every PNG with Read and look at it**, fix, re-run. Up to 4 rounds.
4. Run `python3 -I audio.py <placeDir>`. Use an optional `overrides.json` for readings Kokoro would mispronounce, for example a lone は read as "wa" (key `はブラシ` maps to `ハブラシ`).
5. Publish a NEW artifact: `file_path` = `index.html`, `files = {"audio-data.js": <path>}`, `capabilities = {"db": {}, "user": {}}` (progress is saved per viewer in a private db doc with localStorage as fallback), a generic `icon` word, and a one-sentence `description`. To update later, pass the artifact `url`.
6. Final message: what the page is, word counts per tab, what is unverified (audio, readings, any drawing flaw you know of). Do not paste the artifact URL unless asked.

## Doing several places at once
Write one `spec.md` per place (title strings, icon, suggested sub-places and vocabulary) and give each parallel agent `BRIEF.md` plus its spec. Each agent works only in its own directory and ends with a five-line report: URL, tabs and word counts, changes from the suggested vocabulary, unverified items, known visual flaws. Then spot-check a few screenshots yourself and summarise. A past run built ten places this way in about 12 minutes. Machine limit to remember: 2 CPUs, 8 GB RAM.

## Existing artifacts (Ferdi's account)
Home (Ie no Tango), Station Words, Restaurant, Government Office, School, Park, Shrine and Temple, Amusement Park, Grocery Store, Electronics Store, Convenience Store, Hospital and Pharmacy. Use the artifact list action to find the links.