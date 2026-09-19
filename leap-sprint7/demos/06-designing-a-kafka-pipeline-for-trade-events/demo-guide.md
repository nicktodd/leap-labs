# Module 6 Demo Guide — Designing a Kafka Pipeline for Trade Events

Module 5 proved the mechanics work. Today is about the decision that determines whether they
work FOR you or AGAINST you: what do you use as the partition key, before any code gets written.

## Run It

```bash
mvn compile
mvn exec:java -Dexec.mainClass=com.neueda.leap.sprint7.PartitionKeyChoice
```

Six trade events, three for `ACC-001` (BUY, SELL, BUY, in that order), produced twice with two
different key strategies.

## Option A: Key = eventId (a random UUID, one per event)

```
partition 0: ACC-002/BUY  ACC-001/SELL  ACC-002/SELL  ACC-001/BUY
partition 1: ACC-003/BUY
partition 2: ACC-001/BUY
```

Point at it directly: ACC-001's SELL is in partition 0, its two BUYs are split between partitions
0 and 2. A consumer reading partition 2 alone sees a BUY with no idea a SELL for the same account
happened somewhere else, in some other order, at some other time. **This is a real, common
mistake** — using a unique ID as the key feels "safe" (maximum spread, no hot partitions) but it
destroys the one guarantee Kafka actually offers: order per key.

## Option B: Key = accountId

```
partition 0: ACC-001/BUY  ACC-001/SELL  ACC-001/BUY
partition 1: ACC-002/BUY  ACC-002/SELL
partition 2: ACC-003/BUY
```

Same six events. ACC-001's three events land in the same partition, in production order — BUY,
SELL, BUY — exactly what Settlement needs, and it cost nothing extra: no code in the consumer,
no reordering logic, no timestamps to sort by. **The key choice IS the design.**

## Transition to the Lab

Learners now design the mission's real Kafka pipeline: not the worksheet scenario from Module 4,
but the actual trading platform from Sprint 6 — naming the topic(s), choosing the partition key,
setting partition counts, and identifying every consumer group that needs to read from it. Module
9 implements exactly what gets designed here.
