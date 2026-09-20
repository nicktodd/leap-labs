# Module 11 Lab - Safe Refactoring: Characterisation Tests & Refactoring Techniques

## Objectives

By the end of this lab you will have:

- Used the demo's characterisation test as a safety net for a SECOND, independent refactoring
  step
- Extracted a self-contained piece of logic into its own named method (Extract Method, again)
- Written a new, focused test for the piece you extracted - and confronted the real limit of
  what Extract Method alone can fix

## Where You're Starting From

`shared/starter-codebase/src/main/java/.../TradeReportGenerator.java` already has the demo's
refactor applied: fee calculation now lives in `FeeCalculator`. The accumulation logic - updating
the running totals per ticker - is still inline, exactly as Module 1 first found it:

```java
if (tot.containsKey(tkr)) {
    tot.put(tkr, tot.get(tkr) + val);
    f.put(tkr, f.get(tkr) + fee);
} else {
    tot.put(tkr, val);
    f.put(tkr, fee);
}
c++;
```

Confirm the safety net still works before you change anything:

```bash
cd shared/starter-codebase
mvn test
```

You should see `Tests run: 4, Failures: 0, Errors: 0, Skipped: 0` (the characterisation test plus
the demo's three `FeeCalculator` tests).

## Task

### Part A - Extract Method

Extract the accumulation block above into a new static method:

```java
static void recordTrade(String ticker, double value, double fee) {
    // your extracted logic here
}
```

Call it from `doIt()` in place of the inline block. Do not change what it does - only where the
code lives.

### Part B - Prove Nothing Broke

```bash
mvn test
```

The characterisation test MUST still pass, unchanged, with the exact same assertions as before.
If it fails, you changed behaviour, not just structure - revert and try again.

### Part C - Write a New Test, and Answer a Question

Write a new test class, `RecordTradeTest`, with at least one test that calls `recordTrade()`
twice for the same ticker and asserts the totals accumulated correctly.

Then answer, in writing: **unlike `FeeCalculator`, `recordTrade()` still can't be tested in full
isolation.** What specifically is still getting in the way? (Hint: look at what `recordTrade()`
reads and writes that isn't a parameter or a return value.) Extract Method moved the CODE - did
it remove the PROBLEM?

## Deliverable

- `TradeReportGenerator.java` with the accumulation logic extracted into `recordTrade()`
- The characterisation test, unchanged and still green
- `RecordTradeTest.java` with at least one passing test
- A written answer to Part C's question

## Acceptance criteria

- `mvn test` reports at least 5 tests passing (1 characterisation + 3 `FeeCalculator` + at least 1 new `RecordTradeTest`)
- The characterisation test's assertions are byte-for-byte unchanged from the demo
- Your Part C answer correctly identifies the static fields (`tot`, `f`, `c`) as the remaining
  obstacle - not something vaguer like "the code is still messy"
