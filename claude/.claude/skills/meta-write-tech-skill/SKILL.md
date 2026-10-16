---
name: meta-write-tech-skill
description: Create, refine or review a tech-<tool> skill (kafka, flink, spark, airflow, iceberg and similar data or infra tools) in this dotfiles repo, using the agreed folder structure and version protocol. Use when asked to add a skill for a tool, add a version delta file, or review an existing tech-* skill. Not for non-tech skills.
---

# Writing a tech-* skill

Skills live in `claude/.claude/skills/` (the `claude` Stow package, which becomes `~/.claude/skills/`). Discovery is flat, so grouping comes from names, not folders.

## Naming

- `<kind>-<name>`. Kinds: `tech` (a tool), `wf` (a cross-tool workflow), `meta` (rules about skills), `lang`, and existing ones.
- One skill per tool, not per topic. No `kafka-tuning`. Topics go in `references/`.
- Neighbor tools with their own versions (Debezium, Schema Registry) are separate skills.
- Never name another skill in a description or body unless it exists.

## Structure

```
tech-<tool>/
├── SKILL.md                    # thin: scope, rules, routing, version protocol
├── scripts/detect_version.py   # reads the version from the current project
└── references/
    ├── core/                   # version-stable knowledge, a few files by topic
    └── versions/
        ├── index.md            # line -> delta file, status, upgrade path facts
        └── <line>.md           # deltas only, with frontmatter
```

Templates for each file are in `assets/`. Copy and fill them, do not write from scratch.

## Steps

1. Confirm there is real material (incidents, defaults, checklists). If the user has none, say a skill from general knowledge adds little, and ask for material before writing `core/`.
2. Find the real version lines: read the tool's upgrade or release notes pages and note which versions diverge in behavior. Do not split per minor release.
3. Write `versions/<line>.md` from those notes. Fill frontmatter `source_url` and `verified_at`. Record what you did not read.
4. Write `index.md` from `assets/index.template.md`.
5. Copy `assets/detect_version.template.py` to `scripts/detect_version.py` and fill the probes for how this tool shows up in projects (build files, compose, lockfiles). Test it on fixture projects, including an empty one.
6. Write `core/` from the user's material. Mark any file written from general knowledge as unverified at the top.
7. Write `SKILL.md` from `assets/SKILL.template.md`. The description lists only topics the references actually cover.
8. Run the checklist below. State what was not verified in the PR.

## Rules

- Description is a trigger: concrete phrases, artifacts and error names, plus what it is not for. It must not claim more than the references cover.
- Keep `SKILL.md` under about 200 lines. Keep a delta file under about 150 lines. Past that, trim or split.
- Delta files hold differences only: removed or renamed config, changed defaults, removed APIs, features worth using, migration gotchas.
- Every delta file starts with frontmatter holding `source_url` and `verified_at`. Update both when re-checked.
- Version protocol in every tech skill: detect first, load one delta file, treat `core/` as true unless the delta overrides it, and on `UNKNOWN` or a version newer than the index, check the official notes or ask. Never guess.
- Only record a version you have run or whose notes you read.
- Exact config names and defaults must come from the docs. If unsure, say so.
- Paths in `SKILL.md` use `~/.claude/skills/tech-<tool>/...`.
- Avoid em dashes. Code examples in Python unless the tool needs another language.

## Pre-merge checklist

- [ ] Description matches what references cover, and names no nonexistent skill.
- [ ] `detect_version.py` run on at least: a project with the version, an empty project (`UNKNOWN`), and a newer-than-known version.
- [ ] Every delta file has `source_url` and `verified_at`, and the page was actually read (note partial reads).
- [ ] `index.md` rows match delta files and status says verified or not.
- [ ] No file written from general knowledge is presented as verified.
- [ ] No em dashes: `grep -rn $'\xe2\x80\x94' claude/.claude/skills/tech-<tool>` prints nothing (byte pattern, works in any locale).
- [ ] `TODO.md` updated (remove the finished row, add new follow-ups).
- [ ] PR description lists what was not verified.
