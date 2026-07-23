# Module 4 Lab — Kafka Fundamentals: Answers

## Part A — Match the Terms

1. **Topic** — The `trade-events` stream: the single, named channel into which the trading
   platform publishes every executed trade, and from which all three downstream systems read.

2. **Producer** — The trading platform's order execution service: the component that writes a
   new record to the `trade-events` topic each time a trade is executed.

3. **Consumer** — Each of the three downstream systems (Settlement, Risk Dashboard, Compliance
   Audit Log) reading trade records from the topic and processing them according to their own
   business logic.

4. **Consumer group** — Each downstream system is its own independent consumer group (e.g.
   `settlement-service`, `risk-dashboard`, `compliance-audit`). Each group tracks its own
   offset, so all three systems read every trade independently without any system blocking or
   competing with another for records.

5. **Partition** — A single ordered sub-stream within `trade-events`. The topic is divided
   into multiple partitions; within each partition, records arrive in the order they were
   produced. The partition key (account ID) determines which partition a given trade event lands
   in, so all events for a given account are in the same partition and therefore ordered.

6. **Offset** — The position of a specific trade event within its partition — the sequence
   number that lets Settlement (or any consumer group) record exactly how far through partition
   2 it has read, so it can resume from exactly record 48 after a restart.

## Part B — Choose a Partition Key

### 1. Which key satisfies Settlement's ordering requirement?

**Account ID** satisfies Settlement's requirement. Kafka guarantees that records with the same
key are always written to the same partition, and within a partition records are read in the
order they were written. If every trade for ACC-001 goes to the same partition, Settlement reads
ACC-001's trades in the order they happened — a SELL after a BUY is always seen as after the
BUY. Ticker as a key would group trades by instrument, not by account, which could scatter
an account's trades across partitions with no ordering guarantee across them.

### 2. Is there a key that satisfies Settlement's ordering AND still spreads events across partitions?

Yes — **account ID as the key, with multiple partitions**. "Same key = same partition" does not
mean all events go to one partition; it means all events for a given account ID go to the same
*one* partition. With 6 partitions and many distinct account IDs, Kafka distributes accounts
across partitions: ACC-001 might always go to partition 0, ACC-002 to partition 3, and so on.
Settlement gets ordering per account (because all of ACC-001's events are in partition 0, in
order) while the load is spread across all partitions and can be consumed in parallel by
multiple Settlement consumers.

### 3. Does the account ID key cause a problem for the Risk Dashboard or Compliance Log?

No problem for either. The Risk Dashboard needs each account's own trades in order — account ID
as the key provides exactly that, for the same reason it satisfies Settlement. The Compliance
Audit Log does not care about ordering at all, so any key choice that delivers all records is
acceptable; account ID is fine. Both systems read from the same topic using their own consumer
groups and their own offsets — they are not affected by how the topic was partitioned.

## Part C — Offsets in Practice

### 1. What does Settlement need to have stored before the crash?

Settlement needs to have committed the offset of the last successfully processed record in
partition 2 — specifically, offset **47** (the offset it just processed). Kafka consumer groups
store committed offsets either in Kafka's internal `__consumer_offsets` topic (the default) or
in an external store. As long as offset 47 was committed before the crash, the consumer can
resume from offset 48 on restart.

### 2. Two failure modes if the offset was NOT stored

**Reprocessing (at least once):** If Settlement had been using automatic offset commits and the
crash occurred before the periodic commit interval, the committed offset could be, say, 40.
On restart, Settlement would re-read records 40 through 47 and process them again — duplicating
settlement actions for those trades (e.g. crediting accounts a second time).

**Skipping (at most once):** If Settlement had committed the offset eagerly (before confirming
the business action was actually taken — e.g. committing offset 47 immediately after consuming
the record, before the database write succeeded), the consumer would resume from 48 on restart
and never retry processing record 47 — leaving that trade unprocessed with no indication of the
gap.
