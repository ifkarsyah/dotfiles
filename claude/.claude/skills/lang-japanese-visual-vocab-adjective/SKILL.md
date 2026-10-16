---
name: "lang-japanese-visual-vocab-adjective"
description: "Build a visual Japanese adjective-learning artifact: opposite pairs with phrases and sentences, a table of every form, and a conjugation drill, with furigana and Kokoro audio."
---

# Japanese adjectives artifact (pairs, context, forms, drill)

Renamed from `lang-japanese-visual-vocabulary-adjective`. Siblings: `lang-japanese-visual-vocab-noun` (places and situations) and `lang-japanese-visual-vocab-verb` (daily routines). Same page shell, audio pipeline and saved progress. Strategy for choosing what to learn: `lang-general-mining-vocabulary`. Templates live in the Project "Learn 日本語" under `visual-vocab-adjective/` (adjectives.js, conj.js, app.js, extra.css, build.py, dump.js). Shared pieces (page head and CSS tokens, `audio.py`) live under `visual-vocab/`; `template.html` there is the base page. Read those files with project_read before building. Paths inside build.py and dump.js are absolute to an old scratchpad, so change them.

## Learner rules
- No romaji. Furigana as `{漢字|かんじ}` markup, with a toggle.
- Code examples in Python, notes in Markdown, few em dashes.
- Say plainly when a pairing, reading or nuance is doubtful. Known loose pairs in the first build: 弱い雨 for "light rain", and 多い/少ない has no direct noun phrase. The audio is made by Kokoro and has not been checked by ear; say so.

## Data (adjectives.js)
`TABS` is a list of themed tabs: `{id, tab, tabJp, jp, en, note, pairs:[[A, A], ...]}`. Each adjective is `A(w, type, en, pic, np, npEn, s, sEn, note)`:
- `w`: dictionary form with furigana markup.
- `type`: `i`, `na`, or `ii` (いい only, which uses the stem よ).
- `pic`: one emoji as a memory hook.
- `np` and `npEn`: adjective plus noun phrase (大きい犬). Leave `np` empty and put a usage tip in `npEn` when the word cannot go directly before a noun (多い, 少ない).
- `s` and `sEn`: one short sentence, polite form.
- `note`: optional trap (きれい and 嫌い are な-adjectives ending in い; 高い means tall and expensive; 熱い vs 暑い).
Group by theme: size, price and amount, weather, feelings, taste, な-adjectives, and mixed い/な pairs. Pair true opposites, and flag loose ones. Keep each tab to 4 to 5 pairs.

## Conjugation (conj.js)
One source of truth used by the page, the drill and the audio dump. Forms: plain and polite for present, negative, past, past negative, plus て-form, adverb and before-noun.
- い: drop い, add くない, かった, くなかった, くて, く. Polite adds です.
- な: keep the word, add だ, じゃない, だった, じゃなかった, で, に, な. Polite: です, じゃないです, でした, じゃなかったです.
- いい: stem よ except the plain present.
`wrongConj` applies the other type's rule and supplies the classic wrong answer (静かくない, 大きいじゃない) as a drill distractor.

## Page (app.js, extra.css, build.py)
Tabs: one per theme, then `All the forms` (rule cards, chip picker for every adjective, 4x2 table with the changing part coloured, て/adverb/noun row) and `Conjugation drill` (4 choices, one always the wrong-type mistake, explanation on a miss, score for the visit, filter all/い/な). Pair cards show picture, type badge, word, phrase and sentence with a play button each. Quiz mode shows only picture and English until tapped. Progress is per pair id `tab:index`, saved to localStorage and to the db document `data/users/<uid>/progress` when the capabilities `{"db":{}, "user":{}}` are declared. Audio comes from `audio-data.js` (base64), keyed by the plain display text, with the device voice as fallback.

## Workflow
1. Write adjectives.js; run `node dump.js` in that folder. It checks pair size, type, い endings, latin letters and brace balance, and writes words.json and overrides.json.
2. Generate audio in the background (about 1.2 clips per second, 760 clips takes about 10 minutes): `python3 -I audio.py <dir>` using the Kokoro setup from the noun skill (jf_alpha, speed 0.9, spoken text is the kana reading; replace "・" with "、"). Check the log says no words without a clip.
3. `python3 build.py`, then test with Playwright: tab count, pair count, learned counter, quiz reveal, forms tab, drill answer, a phone-width screenshot. Fonts and audio-data.js 404s are expected locally.
4. Publish with Artifact: the file, `files` mapping `audio-data.js`, icon, description, and capabilities db and user. Do not paste the URL in the reply.
5. Report honestly: audio unchecked by ear, any loose pairs, emoji instead of drawn scenes.

## Teaching notes behind the design
Learn in opposite pairs and in a phrase or sentence, never as bare words. Learn い vs な as the first split, then the exceptions (いい, きれい, きらい). Drill the forms only until they are automatic; add spaced repetition only for misses.