# Module 10 Lab — Code Quality Fundamentals & Code Smell Hunt

## Objectives

By the end of this lab you will have:

- Extended a real static-analysis tool with a new, working check
- Manually identified code smells the tool cannot catch, and explained why each one matters
- Produced a written smell report that Module 11 will use directly when refactoring

## Setup

```bash
mvn compile
java -cp target/classes com.fidelity.leap.sprint7.CodeSmellScanner
```

Confirm the "Duplicated literals" section currently prints nothing — that's the gap you're
about to fill.

## Part A — Implement `scanDuplicatedLiterals()`

Complete the three TODOs in `CodeSmellScanner.java`:

1. Count how many times each distinct decimal literal (e.g. `"0.0005"`) appears across the
   whole file.
2. For every literal appearing more than once, print it and its count.
3. If nothing is duplicated, print `"  none found"`.

Run the scanner again. You should see `0.0005` reported as appearing twice.

**Why this matters, specifically**: `TradeReportGenerator` uses `0.0005` for both the `BOND` fee
rate and the fallback `else` branch (any unrecognized trade type). That's not a deliberate shared
rule — it's two independent decisions that happen to use the same number today. If someone
changes the BOND rate next quarter and only edits one of the two lines, the fallback rate silently
drifts out of sync with no error, no warning, and no test to catch it.

## Part B — Manual Smell Hunt

The scanner only catches what it was built to catch. Working from `TradeReportGenerator.java`
directly, answer the following:

1. **String concatenation in a loop**: `out = out + tkr + "," + ...` runs once per row, inside
   the `while` loop. What's the practical cost of building a string this way as the file grows
   from 10 rows to 10 million? (You don't need to benchmark it — reason about what `String`
   immutability means for repeated concatenation.)
2. **Single Responsibility, named specifically**: list the distinct jobs `doIt()` does (parsing,
   fee calculation, aggregation, reporting is a start — find at least one more). For each job,
   name what would force it to change independently of the others.
3. **A test you cannot write today**: try to describe, in one sentence, how you'd unit test just
   the fee-calculation logic in isolation. What's stopping you from actually writing that test
   right now, given the current structure of `doIt()`?

## Deliverable

- A working `scanDuplicatedLiterals()` that correctly flags `0.0005`
- Written answers to Part B's three questions

## Acceptance criteria

- Scanner output shows `"0.0005" appears 2 times` (or equivalent) and nothing for `0.001`
- Part B's answers are specific to THIS code (line-level, not generic advice)
- Question 3's answer identifies the actual structural reason a test can't isolate the fee logic
  today (not "there are no tests" — why can't one be added without changing the method first)
