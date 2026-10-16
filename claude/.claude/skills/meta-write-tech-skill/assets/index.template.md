# <Tool> version index

Read this first, then load ONLY the delta file for the detected line.
Everything in `references/core/` is assumed true for all versions unless a delta file overrides it.

Last checked against <source> on <date>. Newest release seen then: <version>.

## Version protocol

1. Run `python3 ~/.claude/skills/tech-<tool>/scripts/detect_version.py` from the project root.
2. `line <N>.x` means load `<N>.x.md`.
3. `UNKNOWN` or `line UNKNOWN`: do not guess. Ask, or check the project's `CLAUDE.md` for a pinned version.
4. Detected version newer than the newest row below: say so and check the official notes before answering. Do not extrapolate.

## Lines

| Line | Delta file | Status | Key change vs previous line |
|---|---|---|---|
| <N>.x (<a> to <b>) | `<N>.x.md` | verified <date> or partly verified or draft | <one line> |

## Quick signals

| You see | Means |
|---|---|
| <config key or file> | <line or mode> |

## Upgrade path facts

- <fact from official notes>

## Maintenance rules

- Add a delta file only for a line whose behavior diverges. Not one per minor release.
- A delta file holds differences only. Past about 150 lines, trim.
- Only write a row for a version you have run or whose release notes you read.
- Every delta file starts with frontmatter holding `source_url` (the release notes page read) and `verified_at` (date). Update both when you re-check.
- When a project bumps the tool, update the Status column and date here.
- Source of truth: <upgrade notes URL pattern>.
