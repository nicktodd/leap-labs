# Module 4 Lab — Kafka Fundamentals: Topics, Producers, Consumers, Partitions, Offsets

## Objectives

By the end of this lab you will have:

- Matched every core Kafka term to a concrete piece of a real trade-event scenario
- Reasoned about partition key choice and its consequence for ordering, before writing any code

## Format

A guided worksheet. No code — Module 5 is hands-on with real Kafka.

## The Scenario

The mission's trading platform needs to tell downstream systems whenever a trade is executed.
Three systems care:

- **Settlement** needs every trade, and for any given account, needs them in the order they
  happened.
- **The risk dashboard** needs every trade, doesn't care about order across different accounts,
  but does need each account's own trades in order (a sell after a buy must be seen as after it).
- **The compliance audit log** needs every trade, and doesn't care about ordering at all — it's
  just building a complete historical record.

## Task

### Part A — Match the Terms

For each term, write **one sentence** naming the specific thing in this scenario it corresponds
to:

1. **Topic** —
2. **Producer** —
3. **Consumer** —
4. **Consumer group** (three independent systems, each reading the whole topic, each tracking its
   own progress) —
5. **Partition** —
6. **Offset** —

### Part B — Choose a Partition Key

The mission's trading platform needs to decide what to use as the partition key for trade events.
Two candidates: **account ID**, or **ticker**.

1. Given Settlement's requirement above, which key satisfies it, and why?
2. Is there a key choice that would satisfy Settlement's ordering requirement AND still spread
   events across multiple partitions (rather than everything landing in one partition)? Explain
   your reasoning — don't just name a key, justify it against what "same key = same partition"
   actually guarantees.
3. The risk dashboard and the compliance log both consume the *same* topic as Settlement. Does
   the partition key chosen for Settlement's benefit cause either of them a problem? Why or why
   not?

### Part C — Offsets in Practice

Settlement's consumer crashes after processing offset 47 in partition 2, and restarts five
minutes later.

1. What does Settlement need to have stored *before* the crash, to pick up correctly where it
   left off?
2. If Settlement had NOT stored that, what are the two possible failure modes it could hit on
   restart? Name both, specifically.

## Deliverable

Your answers to Parts A, B, and C.

## Acceptance criteria

- Part A's six answers are specific to this scenario, not textbook definitions
- Part B correctly identifies that ordering is guaranteed only per-key, and reasons about whether
  a single key can serve multiple consumers' needs
- Part C names both failure modes (reprocessing already-handled trades, or skipping unprocessed
  ones) explicitly, tied to what "offset" actually tracks
