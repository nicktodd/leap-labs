# Module 6 Lab - Designing a Kafka Pipeline for Trade Events

## Objectives

By the end of this lab you will have:

- Produced a written design for the mission's real Kafka pipeline - topic(s), partition key,
  partition count, and consumer groups
- Justified every design decision against a concrete downstream requirement, not guesswork

## Format

A design document. No code - Module 9 is where this gets built.

## The Mission's Requirements

The Spring week's trading platform accepts orders and executes trades. Starting this week, every
executed trade must also be published as an event, because four downstream systems now need to
react to trades without polling the mission service directly:

- **Settlement** - needs every trade, and for any given account, needs them in the order they
  happened (a SELL must never be seen as happening before its BUY).
- **The risk dashboard** - needs every trade, needs each account's own trades in order, but
  doesn't care about ordering across different accounts.
- **The compliance audit log** - needs every trade, doesn't care about ordering at all, just a
  complete record.
- **A new fraud-detection service** (added this week) - needs every trade for a given account,
  in order, within a few seconds of it happening, to catch suspicious patterns (e.g. rapid
  buy-sell-buy cycles on the same ticker).

## Task

### Part A - Topic Design

1. How many topics does this pipeline need? Justify your answer against the four systems above -
   don't default to "one topic" or "one topic per consumer" without reasoning through it.
2. Name the topic(s).

### Part B - Partition Key

1. Choose a partition key. Name it, and explain specifically why it satisfies Settlement, the
   risk dashboard, and fraud detection simultaneously.
2. Explain why `eventId` (a unique ID generated per trade) would be the wrong choice, using the
   demo's evidence, not just "it feels wrong."
3. Is there a downstream requirement here that a single key CANNOT satisfy alongside the others?
   If yes, name it and explain the conflict. If no, explain why account-level ordering happens to
   cover every requirement in this scenario.

### Part C - Partition Count & Consumer Groups

1. How many partitions would you start with, and what's the actual trade-off you're weighing
   (not "more is always better")?
2. List the consumer groups this pipeline needs - one per system, or fewer? Justify.
3. Fraud detection needs trades "within a few seconds." Does partition count or consumer group
   design affect that latency requirement at all? Why or why not?

## Deliverable

A short design document (half a page to a page) covering Parts A, B, and C, written as if it
will be handed to whoever implements Module 9 - specific enough that they don't have to guess.

## Acceptance criteria

- Topic design is justified against all four downstream systems, not asserted
- Partition key choice is justified with the SAME reasoning demonstrated in the demo (order is
  guaranteed only within a partition, only for a shared key)
- The eventId-as-key mistake is explicitly ruled out, with a reason
- Partition count and consumer group answers distinguish between what Kafka's design actually
  controls (ordering, parallelism) and what it doesn't (network/processing latency)
