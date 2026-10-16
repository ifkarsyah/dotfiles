---
name: "lang-general-mining-vocabulary"
description: "Decide which vocabulary to learn in a target language (Japanese, German) and how to mine it: frequency spine, themed lists, function words, transfer map, gap check."
---

# Mining vocabulary for a target language

Scope for now: **Japanese and German**. For another language, say it has no profile yet, then write one (section 3) before mining. Output of this skill is a **word plan**, not a finished app. Rendering is done by the language skills, for example `lang-japanese-visual-vocabulary-noun`, `-verb` and `-adjective`.

Learner rules: no romaji for Japanese, code in Python, Markdown files rather than Word, few em dashes, and say plainly when a choice is doubtful or a claim is unverified.

## 1. Principle
Themes make words memorable. Frequency decides which words matter. Use frequency as the spine, themes as the hook, and a gap check to join them.

## 2. Two layers
- **Concept layer (language-neutral):** concept id, English gloss, category, and the scene or persona it belongs to. Reuse it for every language.
- **Language layer:** the word, reading or gender, a short example, audio text, transfer tag, notes.
Keep a **local flavour** slot for items that are not universal (Japan: IC card gate, konbini, shrine; Germany: Pfand, Anmeldung, Bahncard). Do not force these into the universal list.

## 3. Language profile (ask: what does this language make hard?)
Write one short profile per language before mining.

**Japanese**
- Nouns: counters; kanji readings; loanwords in katakana.
- Verbs: group (ichidan, godan, irregular), transitive and intransitive pairs, て and た forms, polite and plain.
- Adjectives: い vs な, irregular いい, きれい and 嫌い are な.
- Function words: particles, demonstratives, question words, connectors, counters and numbers.
- Hook: furigana markup `{漢字|かんじ}`; spoken text is the kana reading.
- Frequency sources: BCCWJ-based or subtitle-based lists. JLPT publishes no official word lists, so treat JLPT-level lists as unofficial.

**German**
- Nouns: gender is part of the word. Always store the article and the plural (der Tisch, die Tische). Capitalised.
- Verbs: separable prefixes (anrufen: ich rufe an), strong and irregular forms (store the principal parts), the perfect with haben or sein, modal verbs, reflexive verbs.
- Adjectives: endings change with case, gender and article type, so do not drill them as bare words. Teach the predicate form first (Das Haus ist groß), then attributive endings as a separate drill.
- Function words: articles and cases, prepositions with their case, pronouns, conjunctions that change word order (weil, dass), nützliche Partikeln (doch, mal, schon).
- Frequency and level sources: Goethe-Institut Wortliste for A1, A2, B1 (official), plus a subtitle or web-corpus frequency list (for example SUBTLEX-DE, Leipzig Wortschatz).
- Local flavour: bureaucracy, housing and transport words matter early if the learner is relocating (Anmeldung, Bürgeramt, Krankenversicherung, Mietvertrag).

## 4. Sources and priority
Find sources with web search. If the sandbox cannot download a list, ask the learner to attach it. Never invent a list.
1. Official level list if one exists (Goethe for German).
2. A ranked frequency list of lemmas.
3. The learner's own life: words they met this week, documents they must read, places they actually go.
Priority = frequency x usefulness for the learner's current situation x ease (cognate or not). Use it to order the first 500, then the next 500.

## 5. Build the lists
Supply these categories, then add themes on top:
- **Nouns by place.** Universal places first (home, station, restaurant, grocery, government office, school, park, hospital and pharmacy, electronics store, convenience store), then local flavour. Sub-places become tabs.
- **Verbs by persona and routine.** Typical student day, employed adult day, weekend. Add the **top 100 frequent verbs** regardless of persona (be, have, go, do, make, want, can, must, say, see), and verbs by pattern (Japanese transitive pairs; German separable and strong verbs).
- **Adjectives by antonym pair**, with a phrase and a sentence each. Mark pairs whose opposite is loose.
- **Function words** as their own list, ordered by frequency. These are the most frequent words and fit no theme.
- **Chunks.** Collocations and set phrases (make an appointment, einen Termin machen). Attach the best two or three to each word.

## 6. Transfer map
Tag each word with one of: `cognate` (shares a root with a language the learner knows), `loan` (borrowed), `shared-script` (Japanese kanji overlapping with Chinese characters), `false-friend`, or `new`. Notes the learner may benefit from: German shares many roots with English; Indonesian has many Dutch loanwords (useful if Dutch is added later). Flag false friends explicitly. Do not claim a cognate when unsure; mark it `check`.

## 7. Gap check (frequency vs your lists)
After drafting the themed lists, compare them with a frequency list to find what the themes miss. Save this script as `gap_check.py` (a copy lives in the Project under `general-mining/`):

```python
import argparse, sys

def read_words(path):
    out = []
    with open(path, encoding="utf8") as f:
        for line in f:
            w = line.strip().split("\t")[0].strip()
            if w and not w.startswith("#"):
                out.append(w)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("freq"); ap.add_argument("mine")
    ap.add_argument("--top", type=int, default=2000)
    ap.add_argument("--out", default="gaps.md")
    a = ap.parse_args()
    freq = read_words(a.freq)[: a.top]
    mine = set(read_words(a.mine))
    missing = [(i + 1, w) for i, w in enumerate(freq) if w not in mine]
    hit = len(freq) - len(missing)
    print(f"top {len(freq)}: covered {hit} ({hit / max(len(freq), 1):.0%}), missing {len(missing)}")
    with open(a.out, "w", encoding="utf8") as f:
        f.write("# Gaps\n\n| Rank | Word |\n|---|---|\n")
        for r, w in missing:
            f.write(f"| {r} | {w} |\n")

if __name__ == "__main__":
    sys.exit(main())
```
Run `python3 -I gap_check.py freq.txt mine.txt --top 2000`. Both files list lemmas, one per line (use dictionary forms; for German store the noun without its article). Read the missing list by rank, add the real gaps (mostly function words and abstract verbs), and ignore proper nouns and noise.

## 8. Order and pacing
- Learn one language at a time. German and Dutch are close enough to be confused, so add Dutch only after German is around B1. Chinese is a separate track that gets a head start from kanji but not from tones or grammar.
- Spaced repetition only for items the learner misses, not for everything.
- Review the plan after each level: re-run the gap check against the next 1,000 words.

## 9. Deliverable
A Markdown word plan: language profile, source list with links, priority order for the first 500 words, the themed lists by category, the function-word list, the transfer tags, the gap report, and the next artifact to build with the matching renderer skill. State what is unverified (sources not downloaded, readings or cognate tags not checked).