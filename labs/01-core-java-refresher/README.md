# Module 1 Lab — Core Java Refresher

## Objectives

By the end of this lab you will have:

- Used Java's core syntax, types, and control flow to implement working methods
- Used the Java collections framework (`List`, `Map`, `Set`) at a working level
- Correctly distinguished checked from unchecked exceptions in your own code

## Setup

- Java 21 and Maven installed
- `mvn test` runs the pre-written test suite in `src/test/java` against your implementation

## Task

Three small katas, each in its own class under `src/main/java/com/neueda/leap/sprint5/`. Every
class currently throws `UnsupportedOperationException("TODO: ...")` — replace each with a real
implementation. Do not modify the test files; they define what "correct" means for each kata.

### Kata 1 — `TradeClassifier` (types & control flow)

- `classifySize(Trade)` — `"LARGE"` if the trade's value exceeds `LARGE_THRESHOLD`, else `"NORMAL"`.
- `classifySide(Trade)` — `"BUY"`/`"SELL"` (case-insensitive match), or `"UNKNOWN"` for anything else.

### Kata 2 — `TradeBook` (collections framework)

- `totalValue()` — sum of every trade's value in the book.
- `valueByInstrument()` — a `Map<String, Double>` of instrument to total value traded.
- `distinctClients()` — a `Set<String>` of client names, no duplicates.

### Kata 3 — `TradeParser` (checked vs. unchecked exceptions)

- `parse(String line)` — parse a comma-separated trade line into a `Trade`.
- A non-numeric `quantity` or `price` should let `NumberFormatException` (unchecked) propagate
  unhandled — do not catch it.
- A numeric but non-positive `quantity` or `price` should throw the checked
  `MalformedTradeException`, with a message naming the bad value.

## Running the tests

```bash
mvn test
```

All 12 tests should pass once every method is implemented. Run this often as you go, not just at
the end — each kata's tests will tell you exactly what's still missing.

## Acceptance criteria

- `mvn test` passes with 0 failures and 0 errors.
- No test file has been modified.
- `TradeParser.parse` does not catch `NumberFormatException` anywhere in its own body.
- Every method's implementation avoids `UnsupportedOperationException` — the TODO stubs are gone.
