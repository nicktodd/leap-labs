# Module 1 Demo Guide - The Cost of Technical Debt & the Refactor Mission

Run the codebase first. It works. That's deliberate - technical debt isn't "broken code," it's
working code that's expensive or risky to change. Make that concrete before naming a single
principle.

## Run It, Then Break It Quietly

```bash
cd shared/starter-codebase
mvn compile
java -cp target/classes com.neueda.leap.mission.stream.legacy.TradeReportGenerator
```

Expect: `Processed 10 trades`, a per-ticker summary, a `report.csv` written to disk. Looks fine.

Now open `trades.csv` and count the rows: 12 data rows, but only 10 processed. **Ask the room:
where did the other two go?** Give them a minute before pointing at `catch (Exception e) { //
skip bad row }` in `TradeReportGenerator.doIt`.

**This is the actual cost, made concrete**: two rows - one with a missing quantity, one with a
corrupted price - were silently dropped. No log line. No error. No count of how many rows were
skipped. If this were a real end-of-day settlement job, two trades would simply be missing from
the report, and nobody would know until a reconciliation caught the discrepancy days later - or
didn't.

## What Technical Debt Actually Costs

Land on three concrete costs, each traceable to something in this exact file:

1. **Silent correctness risk** - the swallowed exception above. Not a hypothetical; a real,
   reproducible bug sitting in working code right now.
2. **Change risk** - `doIt()` does I/O, parsing, fee calculation, aggregation, formatting, and
   more I/O, all in one ~40-line method, with two static mutable maps as shared state. Ask: "if
   we needed to add a third fee tier tomorrow, how confident would you be making that change
   without breaking something else in this method?"
3. **No safety net** - there isn't a single test in this project. Point at the empty
   `src/test/java` tree. Every future change to this file is a change made on faith.

**Say explicitly**: none of this makes the code "bad" in some abstract sense. It makes it
*expensive* - expensive to extend, expensive to trust, expensive to onboard someone new onto.
That's the actual definition being taught today: technical debt is a real, ongoing cost, not a
moral judgment about the person who wrote it.

## Introduce the Mission

Point at `shared/mission-brief.md`. This exact codebase is what Modules 10-13 spend the rest of
the week on: Module 10 hunts for more smells like the ones just found (without fixing them yet);
Module 11 writes characterisation tests as a safety net *before* refactoring; Module 12 wires
automated quality gates into CI so this kind of debt doesn't quietly return; Module 13 adds
security scanning on top. Today is only the honest look - no fixing yet.

## Transition to the Lab

In pairs, learners review the same codebase and write down the first three things that concern
them - deliberately not fixing anything. The instinct to jump straight to "and here's how I'd fix
it" is worth naming and resisting out loud; this lab is about noticing accurately first.
