# Module 2 Demo Guide - Data Movement at Enterprise Scale: Batch vs Real-Time

Run both, back to back, and watch the timestamps. That's the entire demo.

## Run the Batch Job

```bash
mvn compile
java -cp target/classes com.neueda.leap.mission.stream.BatchSettlementJob
```

Expect two timestamps roughly **milliseconds** apart - "started" and "finished" - because the
whole file existed, on disk, before a single trade was processed. There's no meaningful gap
between the first trade and the last; they were all "available" at the same instant.

## Run the Live Feed Simulator

```bash
java -cp target/classes com.neueda.leap.mission.stream.LivePriceFeedSimulator
```

Expect six timestamps roughly **800ms apart**, printed as they happen, one at a time. **Point at
this explicitly**: there was no file to read ahead of time. Each price update is handled the
moment it exists - the program has no idea what the seventh update will be, or when it'll arrive,
because it hasn't happened yet.

## The Actual Distinction

Write both definitions on the board, from what was just observed, not from a textbook:

- **Batch**: a *bounded*, known dataset, processed as one unit, on a schedule. You can ask "how
  many records are in this batch?" before processing starts.
- **Real-time**: an *unbounded* stream. There is no "how many will there be" - only "how many have
  arrived so far." Processing has no natural end while the source is still live.

## What Actually Changes as Volume Grows

This is the second half of the module's objectives - not just definitions, but consequences at
real enterprise scale:

- A batch job that takes 4 minutes at today's volume might take 40 minutes at 10x volume - and if
  it's scheduled to run in a 30-minute overnight window before markets reopen, that's not a
  performance nuisance, it's a hard deadline miss.
- A real-time stream doesn't have a "job duration" to blow through - but it needs infrastructure
  that can sustain continuous throughput indefinitely, which is a different engineering problem
  (and a different cost) than a job that runs once and stops.
- Batch failures are usually visible (the job didn't finish, or finished with an error code).
  Stream failures can be silent - a consumer falling behind, or dropping messages, can go
  unnoticed for a long time without deliberate monitoring (Module 8 picks this up directly).

## Point Back at Module 1

`BatchSettlementJob` and `TradeReportGenerator` (Module 1's starter codebase) are the same shape
of thing: read a whole, known dataset, process it, done. Naming that shape today - "batch" - gives
the group vocabulary for what they already reviewed critically yesterday.

## Transition to the Lab

Three real data scenarios, no code: decide batch or real-time for each, and justify it against the
actual consequences just discussed, not a gut feeling.
