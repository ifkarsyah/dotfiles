# Kafka debugging (version-stable)

Status: written from general knowledge, NOT checked against the docs line by line. Config names below are long-standing, but confirm exact names and defaults for the detected version in `references/versions/<line>.md` or the official docs before quoting them.

Always state the detected broker and client version in the answer.

## Consumer lag keeps growing

Work through in order, stop at the first hit:

1. Is the consumer alive and assigned? Check group state and member count with `kafka-consumer-groups.sh --describe --group <g>`.
2. Is lag growing on all partitions or a few? A few means key skew or one slow/stuck partition. All means consumers are too slow overall.
3. Is processing slower than poll interval allows? Long processing between `poll()` calls can exceed `max.poll.interval.ms` and trigger a rebalance, which looks like lag.
4. Is the fetch config the limit? Check `fetch.min.bytes`, `fetch.max.wait.ms`, `max.poll.records`, `max.partition.fetch.bytes`.
5. Are there more consumers than partitions? Extra consumers sit idle. Parallelism is capped by partition count.
6. Downstream slowness (DB, HTTP) is the usual real cause. Measure time spent per batch before tuning Kafka settings.

## Frequent rebalances

- Causes: missed heartbeats (`session.timeout.ms`), slow processing (`max.poll.interval.ms`), consumers restarting, deployments rolling all pods at once.
- Check broker and consumer logs for the reason a member left.
- Static membership (`group.instance.id`) reduces rebalances from restarts.
- The classic and the newer consumer protocol behave differently. The version delta file says which one is the default.

## Producer problems

- Timeouts: check `delivery.timeout.ms`, `request.timeout.ms`, `max.block.ms`, broker reachability, and whether metadata fetch is failing.
- Throughput low: look at `batch.size`, `linger.ms`, `compression.type`, and `buffer.memory`. The `linger.ms` default changed in 4.0, see `4.x.md`.
- Duplicates or reordering: check `enable.idempotence`, `acks`, `retries`, and `max.in.flight.requests.per.connection`.
- `NotEnoughReplicas`: `min.insync.replicas` not met with `acks=all`. Check ISR.

## Under-replicated partitions, ISR shrinking

- Look at follower lag, broker disk and network, GC pauses, and `replica.lag.time.max.ms`.
- One broker slow often shows as many partitions under-replicated on that broker.
- Check disk usage and log directory health before changing replication settings.

## Data seems lost

- Producer side: `acks`, retries exhausted, unflushed producer on shutdown.
- Broker side: unclean leader election, `min.insync.replicas` too low, retention deleted the data before the consumer read it.
- Consumer side: offsets committed before processing finished, `auto.offset.reset` jumped to latest after offsets expired.

## Useful commands

```bash
kafka-topics.sh --bootstrap-server <b> --describe --topic <t>
kafka-consumer-groups.sh --bootstrap-server <b> --describe --group <g>
kafka-get-offsets.sh --bootstrap-server <b> --topic <t>
```

Script names and options changed in 4.2 (KIP-1147). See `4.x.md` before giving exact flags.

## What to ask the user if the cause is unclear

- Kafka broker and client versions, and whether KRaft or ZooKeeper.
- Partition count, consumer count, key distribution.
- Exact error text and which side logs it.
