# TODO

Planned skills under `claude/.claude/skills/`. Follow `meta-write-tech-skill` when writing any `tech-*` skill.

Rule: write a skill only when you have real material for it (incidents, defaults, review checklists). A skill written from general knowledge adds little, so leave the slot empty until then.

## Tech skills to write

| Skill | Scope | Version axis | Notes |
|---|---|---|---|
| `tech-kafka-connect` | Connect framework: workers, distributed mode, offsets, DLQ, SMTs, converters | follows the Kafka version | Framework ships with Kafka. Connectors are separate. |
| `tech-debezium` | Connector config, snapshot modes, offsets, schema history, slots | own versions | Runs on Connect. Do not mix into tech-kafka. |
| `tech-schema-registry` | Compatibility modes, subjects, serializers | own versions, vendor specific | Confluent, Apicurio and Karapace differ. Decide which to cover. |
| `tech-flink` | Job logic, state, checkpoints, connectors | 1.x and 2.x lines | Check the real line breaks before writing deltas. |
| `tech-spark` | Batch and streaming, tuning, shuffle | 3.x and 4.x lines | Verify against release notes. |
| `tech-airflow` | DAGs, scheduling, executors, upgrades | 2.x and 3.x lines | Verify against release notes. |
| `tech-iceberg` | Table format, maintenance, catalogs, engine integrations | two axes: table format version and engine runtime version | Detect both. Key `versions/` by table format and add a compatibility matrix. |

## tech-kafka follow-ups

- Finish verifying `references/versions/3.x.md` (the last 5700 characters of the 3.9 upgrade page were not read; ZooKeeper migration status, deprecation timeline and minimum Java are missing).
- Confirm the minimum Java version for 4.1 to 4.3.
- Test the Gradle, sbt and `pyproject.toml` probes in `scripts/detect_version.py`, verify the Confluent Platform to Kafka mapping, add `NEWER_THAN_INDEX` output and the minor version, and add fixture tests.
- Run triggering evals (does it load, run detection, and read only one delta file?).
- Rewrite `references/core/` from real incidents and defaults.
- Add a staleness check for `verified_at` (warn after about 90 days).
- Re-add Connect, Debezium, Schema Registry and exactly-once to the description only when a reference backs each one.
