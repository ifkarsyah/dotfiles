# Kafka version index

Read this first, then load ONLY the delta file for the detected line.
Everything in `references/core/` is assumed true for all versions unless a delta file overrides it.

Last checked against kafka.apache.org upgrade notes: 2026-10-16. The site listed 4.3 as the newest release at that time.

## Version protocol

1. Run `python3 ~/.claude/skills/tech-kafka/scripts/detect_version.py` from the project root.
2. `line 3.x` means load `3.x.md`. `line 4.x` means load `4.x.md`.
3. `UNKNOWN` or `line UNKNOWN`: do not guess. Ask, or check the project's `CLAUDE.md` for a pinned version.
4. Detected version newer than the newest row below: say so and check the official upgrade notes for it before answering. Do not extrapolate.
5. Broker version decides cluster behavior. Client version decides API and config available in code. If they differ, mention both.

## Lines

| Line | Delta file | Status | Key change vs previous line |
|---|---|---|---|
| 2.x | not written | not used | Legacy, ZooKeeper only. Ask before assuming anything. |
| 3.x (3.3 to 3.9) | `3.x.md` | partly verified | ZooKeeper and KRaft both exist. KRaft production ready for new clusters since 3.3.1. 3.9 is the last 3.x release. |
| 4.x (4.0 to 4.3) | `4.x.md` | verified 2026-10-16 against upgrade notes | ZooKeeper removed, KRaft only. Brokers/Connect/tools need Java 17, clients/Streams Java 11. Protocol versions from before 2.1 removed. KIP-848 consumer protocol GA. |

Minor-version differences inside a line go in that line's delta file under "Minor notes", not in new files.

## Quick signals

| You see | Means |
|---|---|
| `zookeeper.connect` in broker config | 3.x or earlier, ZooKeeper mode (broken on 4.x) |
| `process.roles`, `controller.quorum.voters` | KRaft mode |
| `confluentinc/cp-kafka:7.x` | Confluent Platform 7.x, which tracks Kafka 3.x. Unverified mapping, check Confluent's table. |
| `confluentinc/cp-kafka:8.0` | Confluent Platform 8.0, which tracks Kafka 4.0. Unverified. |
| `confluent-kafka` (Python) version | librdkafka version, NOT the Kafka version. Say so explicitly. |

## Upgrade path facts (4.x, from official notes)

- To reach any 4.x, brokers must be KRaft with software and metadata version at least 3.3.x.
- KRaft clusters older than 3.3.x: go to 3.9.x first. ZooKeeper clusters: migrate to KRaft first.
- Rolling upgrade, one broker at a time, then finalize with `kafka-features.sh ... upgrade --release-version <x.y>`.
- Metadata downgrade support depends on the release (see `4.x.md`).

## Maintenance rules

- Add a delta file only for a line whose behavior diverges. Not one per minor release.
- A delta file holds differences only: removed or renamed config keys, changed defaults, removed APIs, new features worth using. Past about 150 lines, trim.
- Only write a row for a version you have run or whose release notes you read.
- Every delta file starts with frontmatter holding `url` (the release notes page read) and `verified_at` (date). Update both when you re-check.
- When a project bumps Kafka, update the Status column and date here.
- Source of truth: `https://kafka.apache.org/<NN>/getting-started/upgrade/` (for example `/43/`).
