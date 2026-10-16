---
name: "lang-german-visual-vocab-noun"
description: "Build an illustrated German noun vocabulary artifact for a real-life place (home, station, bank, doctor): hover scene per sub-place, article and plural, Hide English default, quiz and cards."
---

# German visual vocabulary artifacts (nouns by place)

Named to match `lang-japanese-visual-vocab-noun`. German verb and adjective siblings are not written yet. The general strategy for choosing what to learn is in `lang-general-mining-vocabulary`.

Output: one private claude.ai artifact per place (home, restaurant, supermarket, station, Buergeramt, flat hunting, utilities, doctor and pharmacy, bank and post and phone, and so on). Each has one tab per sub-place. Each tab is a flat vector scene (viewBox 800 x 480) in which every noun is a hoverable object. Modes: Learn, Find it, Quiz (article, plural pattern, spelling), Cards. Saved progress per viewer. Audio is the browser German voice.

A second, different engine exists for public signs (Schilder und Verbote): pictograms from a data table, filters by place and sign type, modes Learn, Quiz, Sort, Fill. See the last section.

## Learner rules (always)
- Ferdi is an Indonesian living in Tokyo, moving to Berlin, learning German from scratch, target B2. Nouns always come with article and plural. Never show a noun without its article.
- **Hide English is the default.** Tooltip, panel, Find it prompts, quiz glosses, spelling and cards show German first, with a picture cue. English is revealed on request (switch `#enSwitch`, "Show English", "English hint"). Keep every new feature consistent with this.
- Show code examples in Python unless he asks otherwise. Markdown files, not Word, unless he asks for .docx. Avoid em dashes in all page text and replies. Tell him when he is wrong. Do not flatter.
- All German data and notes come from my own knowledge, not a word list. Say so in the final message and ask him to check uncertain words and every legal or practical claim (deposit caps, notice periods, fees, deadlines) against a real source. Say plainly that nouns alone do not get him through an office; offer phrase drills as a separate artifact, never inside a noun app.
- Correct word choices honestly (for example a pig is das Schwein, not der Schinken; Hähnchen is the food, das Huhn the bird).

## Where the working assets are
The template and scripts are saved in the Project "Learn German" under `visual-vocab/`: `BRIEF.md`, `app.js`, `style.css`, `body.html`, `build.py`, `check.py`, `scene_helpers.js`, `example_words.js`, `example_scenes.js`, and `signs/` for the sign engine. Read them with `project_read` (large text is written to a local file). `project_write` only accepts `local_path` inside the working directory. Put the template in a directory, then for each place copy it to `<place>/`.
If the Project is not attached or the files are missing, say so and ask him to attach it. Do not rebuild from memory unless he agrees.

## Per-place setup (small edits, easy to forget)
- `app.js`: the storage key `LS = '<xx>-progress-v1'` and the db doc name `'<place>-progress'`. Each app needs its own, or progress collides.
- `build.py`: the `<title>` (2 to 4 words, a name, for example "Am Bahnhof"). `body.html`: h1 and subtitle.
- `check.py`: the ROOMS list of tab ids, the chip key it clicks (must belong to the first room) and the spelling string it types.
- Add `words.js` (ROOMS data) and `scenes.js` (`scene_helpers.js` plus one `SC.<roomId> = function () {...}` per room). `build.py` concatenates them.

## Data model
`words.js` defines `var ROOMS = [...]`. Each room: `id`, `de` (tab label), `art` (der, die or das, also used for plural labels), `en`, `intro` (one or two sentences), `words: [w(key, article, noun, plural, english, example, {parts, pg, note, tag})]`.
- `key` is ASCII and unique in the room (umlauts become ae, oe, ue, ss in keys only). The noun itself keeps ä ö ü ß; the spelling quiz compares exactly, with an ä ö ü ß key row. Never write a note that says an ASCII spelling is accepted.
- `parts` and `pg` for compounds, for example `Wasser|hahn` and `water + rooster`. `tag` for `false friend` or `two meanings`.
- `note` is one or two sentences with a real usage point (weak noun, the verb, the typical phrase, the legal or practical fact). Keep an example sentence in `ex`.
- Plurals: use a real plural for every noun. The Bahnhof-lineage `app.js` does not handle empty plurals. Skip mass nouns (Schimmel, Fieber, Bargeld) or choose a countable neighbour (Schimmelfleck, Fieberthermometer). The Supermarkt app handles `''`, but the saved template does not.
- The plural quiz uses `patternOf`: -e, -en/-n, -er, -s, umlaut, umlaut+e, no change, and the added rule `p === sg + last letter + 'e'` for Bus to Busse.
- Aim for 12 words per tab, 4 to 5 tabs per place (48 to 60 words). Split a place when it mixes unrelated vocabularies.
- Keep distinct vocabularies where possible, but repeating a word in another place is fine if the scene shows it differently.

## Drawing rules
- Helpers: `R C E P L T hot`, `DEFS`, `baseRoom(floorTop)`, `floorBoards()`. `hot(k, box, inner)`: `box` is `[x,y,w,h]` or a path string; it makes one `g.hot[data-k]` with exactly one `.hit` shape.
- **One hotspot per word, hit at least 30 units each way.** Never nest hotspots. Draw big things first and small things on top (later siblings win overlaps). A table can be a decoration, not a word.
- Colour from CSS classes only: `wall wall2 floor floor2 wood wood2 metal metal2 glass glassA white cer cer2 red blue green yellow orange dark skin fab1 fab2 fab3 water door door2 rug screen glow shine ctop stripe`; strokes `ln lnr lnl lnd lnd2 lnk lnw cf`; text `tx txd txw`. Do not mix a class with an inline fill on the same shape.
- `cer` and `cer2` render nearly white. For terracotta, boxes and brown, use `orange`, `wood`, `wood2`. A pale object on a pale wall vanishes, so check contrast.
- Abstract words become pictures: documents as paper with a telling icon (key, house, calendar, bar chart, tick, euro sign, arrow), forms, price tags, cards, a body diagram. For paperwork use the **document grid**: a wooden desk with 4 columns by 3 rows of cells, one hotspot per cell (see `example_scenes.js`). For a mixed place use a desk or counter scene.
- People are simple figures (head, hair cap, coat, tie). Do not draw logos, real brands, mascots or card-scheme marks (no overlapping red and yellow circles on a credit card).
- Text on signs with `T(x,y,size,text,cls)`. Check size times characters fits. Do not print the target word on its own hotspot, because that gives away Find it.
- Past mistakes: an unclear chicken or ham (draw pig and chicken as the animal), missing cow or beef, thin diagonal objects that vanish, a hotspot under 30 units, objects with no ground contact.

## Workflow
1. Settle the sub-places and a word list. If the request is clear, start; if it is ambiguous and expensive to redo, ask once. Ferdi may add scope (for example insurance in the doctor place): add a tab, do not drop it.
2. Write `words.js`, then `scenes.js`. Build with `python3 -I build.py`.
3. Run `python3 -I check.py`. It checks one hotspot per word, hit sizes of 30 or more, writes screenshots into `shots/` (desktop, dark phone) and tests overflow and page errors. The console error `ERR_TUNNEL_CONNECTION_FAILED` is only Google Fonts being blocked in the sandbox and is harmless. **Open every scene PNG with Read and look at it**, fix, re-run.
4. Publish a NEW artifact: `file_path` = `index.html`, `capabilities = {"db": {}, "user": {}}`, one generic `icon` word, a one-sentence `description`. No external audio file is needed. To update later, publish the same file path or pass the artifact `url`.
5. Final message: what the page is, tab and word counts, what is unverified (my own word data and notes, the legal or practical claims, audio, any weak drawing) and one next step if there is a real one. Do not paste the URL unless asked.

## Audio
Browser `speechSynthesis`, `de-DE`, rate 0.85, German voice preferred. Free, and chosen after he rejected paid TTS. It cannot be heard from the sandbox: always say audio and progress sync are untested.

## Existing artifacts (Ferdi's account, all private)
Das Zuhause, Im Restaurant, Im Supermarkt (fleisch, fisch, obst, gemuese), Am Bahnhof, Schilder und Verbote, Am Buergeramt, Wohnung und Mietvertrag, Strom und Gas, Arzt und Apotheke (including Der Koerper and Die Versicherung), Bank, Post und Handy. Use the artifact list action to find links.
Not yet built: Buero (workplace), phrase drills, the remaining supermarket sections (Kasse und Pfand, Milchprodukte, Backwaren, Trockenwaren, Tiefkuehl).

## Sign app variant (`visual-vocab/signs/`)
Use it for public signs and other short fixed texts. Data in `signs.js`: `sg(id, type, icon, text, places, paraphrase, english, note, {vary, tone})`, types verbot, gebot, warnung, hinweis, plus the `ICONS` table of 100 x 100 stroke pictograms. Shapes: verbot is a white disc, red ring and slash; gebot a blue disc; warnung a yellow triangle; hinweis a green or blue rounded square (green for rescue signs). Mark `vary: true` where sign wording differs between operators. Pictograms are drawn by hand, not official DIN or ISO artwork, and Ferdi must be told so. Modes: Learn, Quiz (what does it mean), Sort (type), Fill (missing word). Change storage key `sg-progress-v1` and the db doc name when you fork it.