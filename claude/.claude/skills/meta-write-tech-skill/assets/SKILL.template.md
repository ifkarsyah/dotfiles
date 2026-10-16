---
name: tech-<tool>
description: <Tool> <topics the references actually cover>, and upgrades between <Tool> versions (<lines>). Detects the <Tool> version used in the current project first. Not for <out of scope>.
---

# <Tool>

Version-aware guidance. Behavior, defaults and removed APIs differ between lines, so detect the version before answering anything version-sensitive.

## Version protocol (always do this first)

1. Run `python3 ~/.claude/skills/tech-<tool>/scripts/detect_version.py` from the project root.
2. Read `references/versions/index.md`, then load ONLY the delta file for the detected line.
3. Treat `references/core/` as true for all versions unless the delta file overrides it.
4. Output `UNKNOWN`, `line UNKNOWN`, or a version newer than the newest row in `index.md`: do not guess. Check the official upgrade notes or ask me. A pinned version in the project's `CLAUDE.md` also counts.
5. Say which version you assumed in the answer.

## Routing

| Topic | Load |
|---|---|
| <topic> | `references/core/<file>.md` |
| Config defaults, removed configs or APIs, upgrade path | `references/versions/<line>.md` |

## Rules

- Never state a config default or an API as fact without the detected version. If a delta file does not cover it, say it is unverified.
- Config names in answers must be exact. If unsure, check the docs instead of guessing.
- Keep answers short. Point to a reference file instead of pasting from it.
- Neighbors: answer only the <Tool> side for related tools. Name a dedicated skill only if it is listed as available.

## Maintaining this skill

See the maintenance rules at the bottom of `references/versions/index.md`.
