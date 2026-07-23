# Kafka Pipeline Design — Trade Events

**For implementation in Module 9.**

---

## Part A — Topic Design

**One topic: `trade-events`.**

All four downstream systems need every executed trade. None of them need a different
subset of the data, and none of them impose schema requirements incompatible with the others.
Multiple topics would force the producer to publish the same event multiple times (once per
topic), adding coupling, duplication, and consistency risk — if one publish succeeded and
another failed, some consumers would have the event and others would not.

One topic per consumer would be worse: it would route the event fanout responsibility to the
producer, defeating the point of an event bus. The producer should not know or care who its
consumers are.

**Topic name:** `trade-events`

---

## Part B — Partition Key

**Key: account ID**

**Why it satisfies Settlement, Risk Dashboard, and Fraud Detection simultaneously:**

Settlement needs trades per account in arrival order. Account ID as the key routes all trades
for a given account to the same partition, and Kafka guarantees within-partition ordering — so
ACC-001's BUY always arrives before ACC-001's SELL in the partition, and Settlement sees them
in that order.

The Risk Dashboard needs each account's own trades in order (but not cross-account ordering) —
account ID satisfies this for the same reason.

Fraud Detection needs trades per account within seconds, in order, to detect rapid buy-sell
patterns. Account ID means all of a given account's trades are in one partition, consumed by
one Fraud Detection consumer instance, in order, with Kafka's own low-latency delivery.

The Compliance Audit Log needs every trade with no ordering requirement — any key that delivers
all records is fine; account ID is fine.

**Why `eventId` would be the wrong choice:**

If the key is a unique ID generated per trade, every trade lands in a different (pseudo-random)
partition. Two trades for the same account could be in different partitions. Kafka only
guarantees ordering within a partition — so if ACC-001's BUY is in partition 0 and ACC-001's
SELL is in partition 2, a consumer reading both partitions has no guarantee which record it
reads first. Settlement would see the SELL before the BUY in the worst case. The demo showed
this directly: with a unique key, ordering across partitions is lost even for events that share
a business key.

**Is there a requirement that a single key CANNOT satisfy alongside the others?**

No. Account-level ordering (one partition per account-key) happens to cover every requirement
here: Settlement and Risk Dashboard need per-account ordering; Fraud Detection needs per-account
ordering; Compliance does not care. If there were a requirement that two *different* accounts'
trades must be ordered relative to each other (e.g. "a SELL from ACC-001 must be processed
before a BUY from ACC-002 if they share a ticker"), no single partition key on account ID could
satisfy it — but that requirement does not appear in this scenario.

---

## Part C — Partition Count & Consumer Groups

**Starting partition count: 6**

The trade-off is between parallelism and overhead. More partitions mean more consumer instances
can run in parallel (one consumer per partition per group is the Kafka ceiling on parallelism),
which increases throughput and reduces the load per consumer — but also adds per-partition
overhead in the broker (file handles, leader elections), increases rebalance time when consumers
join or leave, and means the ordering guarantee applies within each partition, not across the
topic. Starting at 6 is a reasonable balance for a system with a moderate number of accounts and
four consumer groups: it allows up to 6 instances of each consumer group to run in parallel, and
is easy to increase later (Kafka allows adding partitions; removing them requires a new topic).

**Consumer groups needed: four (one per downstream system)**

- `settlement-service`
- `risk-dashboard`
- `compliance-audit`
- `fraud-detection-service`

Each system needs to read every trade independently, tracking its own position in the topic.
If Settlement and Risk Dashboard shared a group, they would each see only a subset of events
(Kafka splits partitions across group members) — wrong for both. One group per system is the
correct design.

**Does partition count or consumer group design affect Fraud Detection's latency requirement?**

Partition count affects the *parallelism* of fraud detection (more partitions = more consumer
instances can run concurrently = more accounts processed in parallel) but not the end-to-end
latency for any individual event. Kafka's own delivery latency (producer to broker to consumer)
is typically sub-second and is controlled by producer `linger.ms`/`acks` settings and consumer
`fetch.min.bytes`/`max.poll.interval.ms` — not by partition count. Consumer group design does
not affect latency either: whether there is one or four consumer groups, each group polls the
broker independently on its own schedule. The "within a few seconds" requirement is met by
Kafka's inherent low-latency delivery model, not by partition count or group topology.
