---
name: "lang-japanese-visual-vocab-verb"
description: "Build a visual Japanese verb-learning artifact as a day timeline by persona (student, office worker, weekend): polite and plain sentences, key-word chips, furigana, Kokoro audio."
---

# Japanese verbs artifact (a day by persona, in sentences)

Siblings: `lang-japanese-visual-vocab-noun` (places and situations) and `lang-japanese-visual-vocab-adjective` (pairs and forms). Same page shell, audio pipeline and saved progress. Strategy for choosing what to learn: `lang-general-mining-vocabulary` (verbs are divided by persona, nouns by place, adjectives by antonym pair).

Output: one private claude.ai artifact, "Daily Routines" (一日の流れ). One tab per persona. Each tab is a timeline from waking up to going to bed, and every step is one polite sentence built around one or two verbs, with a picture, a clock time and key-word chips.

## Learner rules
- Ferdi reads hiragana and katakana. **No romaji.** Furigana as `{漢字|かんじ}` markup, with a toggle.
- Sentences are polite (ます form) by default, with a Plain form toggle that shows the dictionary-form version (食べる) for every step.
- Code examples in Python, notes in Markdown, few em dashes.
- Say plainly that routines are typical examples, not rules. Say that the audio is made by Kokoro and has not been checked by ear.

## Where the working assets are
The Project "Learn 日本語" holds `visual-vocab-verb/`: `routines.js`, `app.js`, `extra.css`, `build.py`, `dump.js`, `shot.py`. The base page (`template.html`, with the head and CSS tokens) and `audio.py` live under `visual-vocab/`. Copy `template.html` and `audio.py` next to the verb files before building. `build.py` takes everything before `</style>` from `template.html`, then adds `extra.css`, the page body, `routines.js` and `app.js`. Paths inside the scripts can be absolute to an old scratchpad, so change them. Read the files with `project_read`; `project_write` only accepts `local_path` inside the working directory.

## Data (routines.js)
`var DAYS = [...]`. Each persona: `{id, tab, tabJp, jp, en, note, steps}`. The note gives one real cultural point and says it is a typical example.

Each step: `{t: "7:30", pic: emoji pair, jp: polite sentence with markup, plain: plain-form sentence with markup, en, words: [[jp, kana, en, say?], ...], note?, say?, plainSay?}`.
- `jp` and `plain` use the same words. A chain uses the て-form (顔を洗って、歯を磨きます), which teaches the て-form in context.
- `words`: two or three key chips. Put the verb in dictionary form (起きる), then the main noun. A chip speaks its kana, or `say` when the kana would be misread (歯 read as は, say ハ).
- `say` and `plainSay` override the spoken text of the sentence when the default kana would be wrong (a lone は read as "wa": write ハ).
- Order steps by clock time, 12 to 16 per day. Times after midnight sort after 24:00.
- Personas so far: College student (大学生), Office worker (会社員), Weekend (休日). Good next ones: parent with a child, retiree, traveller, job hunter, someone who works from home.

## Choosing the verbs
- Cover the high-frequency daily verbs once per persona so they repeat across tabs: 起きる, 食べる, 飲む, 行く, 来る, 帰る, 見る, 寝る, 乗る, 出る, 入る, 作る, 買う, 書く, 読む, 話す, 始める, 終わる, 着る, 洗う, 着く.
- Include する-verbs as noun plus する (洗濯をする, 掃除する).
- Mix the three groups: る-verbs (食べる), う-verbs (飲む) and the irregulars (する, 来る). Use varied time words and particles (に for time, を for object, で for place, へ for direction).
- Keep the situation true to life in Japan (満員電車, バイト, サークル, ベランダに干す, お風呂 at night, shower in the morning). Flag anything doubtful.

## Page (app.js, extra.css)
- Header: kicker "Japanese verbs and sentences by situation", an overall steps-learned counter and bar.
- Controls: Study and Quiz, Furigana, Plain form, Hide learned.
- Per persona: heading, a day bar with ticks (0 to 24 h) and one dot per step that jumps to it, then a vertical list of steps with time, a time-of-day label (朝, 昼, 午後, 夕方, 夜) and a background tone (dawn, day, dusk, night).
- A step shows the picture, the English, the sentence with furigana, the plain form with its own play button, an optional note and the word chips. A speaker plays the sentence. Mark learned toggles per step.
- Quiz mode shows the picture and English only, with a Show the Japanese button. Tap to reveal.
- Progress is per step id `persona:index`, saved to localStorage (key `daily-routine:v1`) and to the db document `data/users/<uid>/progress` when the capabilities `{"db": {}, "user": {}}` are declared.
- Audio comes from `audio-data.js` keyed by the plain text of the sentence, the plain form and each chip, with the device `ja-JP` voice as fallback.

## Workflow
1. Write `routines.js`. Run `node dump.js`, which checks markup and writes `words.json` and `overrides.json` (key to spoken text, using `say`, `plainSay` and chip `say`).
2. Generate audio in the background with the Kokoro setup from the noun skill (voice jf_alpha, speed 0.9; the spoken text is the kana). Replace "・" with "、". Check the log says no words without a clip.
3. `python3 build.py`, then test with Playwright: tab count, step count, learned counter, quiz reveal, plain-form toggle, furigana toggle, a phone-width screenshot (`shot.py` has the screenshot code). Fonts and audio-data.js 404s are expected locally.
4. Publish with Artifact: `index.html`, `files = {"audio-data.js": path}`, a generic icon (calendar or clock), a one-sentence description, capabilities db and user. Do not paste the URL in the reply.
5. Report honestly: audio unchecked by ear, typical-not-rule disclaimer, doubtful readings.

## Teaching notes behind the design
Learn verbs inside a whole sentence tied to a time of day, never as a bare list. The same verbs recur across personas to build repetition. Show polite first, plain second, and the て-form appears through chained steps. After the timelines, add conjugation drills only if needed, the same way the adjective page does it.