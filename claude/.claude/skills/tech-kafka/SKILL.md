---
name: tech-kafka
description: Apache Kafka producers, consumers, topics, partitioning, consumer lag, rebalancing, KRaft, and upgrades between Kafka versions (3.x and 4.x). Detects the Kafka version used in the current project first. Not for Flink or Spark job logic, Kafka Connect, Debezium or Schema Registry.
---

# Kafka

Version-aware guidance. Kafka behavior, defaults and removed APIs differ between lines, so detect the version before answering anything version-sensitive.

## Version protocol (always do this first)

1. Run `python3 ~/.claude/skills/tech-kafka/scripts/detect_version.py` from the project root.
2. Read `references/versions/index.md`, then load ONLY the delta file for the detected line (`3.x.md` or `4.x.md`).
3. Treat `references/core/` as true for all versions unless the delta file overrides it.
4. Output `UNKNOWN`, `line UNKNOWN`, or a version newer than the newest row in `index.md`: do not guess. Check the official upgrade notes (kafka.apache.org/documentation, upgrade section) or ask me. A pinned version in the project's `CLAUDE.md` also counts.
5. Broker version decides cluster behavior. Client version decides available API and config. If they differ, say so.
6. Say which version you assumed in the answer.

## Routing

| Topic | Load |
|---|---|
| Consumer lag, rebalances, stuck consumers, under-replicated partitions, producer timeouts | `references/core/debugging.md` |
| Topic and partition design, keys, ordering, idempotence, transactions, retention, CDC topics | `references/core/patterns.md` |
| Config defaults, removed configs or APIs, ZooKeeper vs KRaft, upgrade path | `references/versions/<line>.md` |

## Rules

- Never state a config default or an API as fact without the detected version. If a delta file does not cover it, say it is unverified.
- Prefer KRaft concepts for new designs. ZooKeeper mode only exists on 3.x.
- Config names in answers must be exact. If unsure, check the docs instead of guessing.
- Keep answers short. Point to a reference file instead of pasting from it.
- Neighbors: for Flink, Spark, Kafka Connect, Debezium or Schema Registry, answer only the Kafka side here. Do not treat this skill's content as vetted for those tools. Name a dedicated skill only if it is listed as available.

## Maintaining this skill

See the maintenance rules at the bottom of `references/versions/index.md`.
