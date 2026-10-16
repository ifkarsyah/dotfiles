---
name: tech-kafka
description: Apache Kafka design, tuning and debugging. Use for producers, consumers, topics, partitioning, consumer lag, rebalancing, KRaft, upgrades between Kafka versions, Kafka Connect and Debezium CDC, Schema Registry, exactly-once and transactions. Detects the Kafka version used in the current project first. Not for Flink job logic (use tech-flink) or Spark (use tech-spark).
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
- When Kafka is only a source or sink (Flink, Spark, Connect), keep Kafka-side advice here and hand the rest to the relevant `tech-*` skill.

## Maintaining this skill

See the maintenance rules at the bottom of `references/versions/index.md`.
