# Kafka design patterns (version-stable)

Status: written from general knowledge, NOT checked against the docs line by line. Confirm exact config names and defaults for the detected version in `references/versions/<line>.md` before quoting them.

## Topics and partitions

- Ordering is guaranteed only within a partition. Pick the key so that records that must stay ordered share a key.
- Partition count caps consumer parallelism. Size for peak consumer parallelism with headroom, since increasing partitions later changes key-to-partition mapping and breaks ordering for existing keys.
- Avoid hot keys. Check key distribution before choosing a key, or add a salt if strict per-key ordering is not needed.
- One topic per event type or entity stream, not one per consumer.

## Delivery guarantees

| Goal | Producer | Consumer |
|---|---|---|
| At least once | `acks=all`, retries on | commit offset after processing |
| No duplicates from producer retries | idempotence on | n/a |
| Exactly-once read-process-write | transactions | `isolation.level=read_committed`, commit offsets inside the transaction |

- Exactly-once covers Kafka to Kafka. Writing to an external sink still needs idempotent writes or a transactional sink.
- Transaction handling advice changed in 4.0 (KIP-890), see `4.x.md`.

## Retention and compaction

- `delete` retention: time or size based, good for event streams.
- `compact`: keeps the latest value per key, good for changelogs and current-state topics. A null value (tombstone) deletes a key after compaction.
- Compaction is not immediate and does not guarantee only one record per key at read time.

## Changelog topics (Kafka side only)

- One topic per source table or entity, keyed by the entity's primary key so updates for the same row stay ordered.
- Keep tombstones if downstream relies on compaction.
- Make consumers idempotent, since duplicates can appear.
- Tool-specific behavior (Debezium, Connect, Schema Registry) is out of scope here.

## Consumers

- Commit after processing for at least once. Make processing idempotent.
- Keep time between `poll()` calls well under `max.poll.interval.ms`.
- Use one consumer group per independent downstream application.
- Handle rebalances by committing in the revoke callback if committing manually.

## Operations

- Replication factor 3 and `min.insync.replicas=2` with `acks=all` is the common durable setup.
- Monitor consumer lag, under-replicated partitions, request latency, disk usage.
- Test upgrades in a staging cluster, and follow the rolling procedure in the version delta file.
