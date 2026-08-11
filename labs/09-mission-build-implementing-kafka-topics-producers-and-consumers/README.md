# Module 9 Lab — Mission Build: Implementing Kafka Topics, Producers & Consumers

## Format

Team lab. Work in pairs or small groups — this mirrors how a real Kafka consumer bug usually
gets diagnosed: one person reading the stack trace out loud while another checks it against
documentation.

## Objectives

By the end of this lab you will have:

- Implemented Module 6's design for real, exactly as specified (topic, key, consumer group)
- Diagnosed a genuine, unfamiliar Kafka exception from its actual stack trace
- Practiced using GenAI as a second opinion on an error message — verified, not trusted outright

## Setup

Reuse `kafka-sprint7` and the `trade-events` topic from the demo (run the demo's `OrderService`
first if you haven't, so there's data on the topic to consume):

```bash
mvn compile
mvn dependency:build-classpath -Dmdep.outputFile=cp.txt
```

## Task

### Part A — Reproduce the Error

Run the given `FraudDetectionConsumer`:

```bash
java -cp "target/classes;$(cat cp.txt)" com.neueda.leap.sprint7.FraudDetectionConsumer
```

It crashes. Read the full stack trace before doing anything else — specifically the `Caused by:`
line near the bottom.

### Part B — Diagnose It

As a team:

1. Identify which line in `FraudDetectionConsumer.java` is responsible — not the line the stack
   trace points to in Kafka's internals, but the line in OUR code that caused it.
2. Optionally, paste the stack trace into GenAI and ask it to explain the error. **Before
   accepting its explanation**: does it match what the exception message and `Caused by:` chain
   actually say? Does its suggested fix match the difference between `FraudDetectionConsumer`
   and the demo's working `SettlementConsumer`?
3. Write a one-sentence explanation of the root cause, in your own words, that your team agrees
   on.

### Part C — Fix It

Fix `FraudDetectionConsumer` so it runs cleanly and reports 4 received events (or however many
are currently on the topic), with each key printed as the account ID it actually is.

## Deliverable

A working `FraudDetectionConsumer`, plus your team's one-sentence root-cause explanation from
Part B.

## Acceptance criteria

- The consumer runs without throwing, and reports received events with readable account IDs
- Your root-cause explanation names the actual mismatch (not "Kafka is broken" or a vague
  restatement of the exception's class name)
- If GenAI was used, your explanation shows evidence it was checked against the real difference
  between this file and `SettlementConsumer`, not copied verbatim
