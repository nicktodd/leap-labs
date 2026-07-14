# Module 11 — Model Answers

`TradeReportGenerator.java`, `RecordTradeTest.java`, and the updated
`TradeReportGeneratorCharacterisationTest.java` in this folder are the completed, verified
implementation.

## Verified test run

```
Running com.fidelity.leap.sprint7.legacy.FeeCalculatorTest
Tests run: 3, Failures: 0, Errors: 0, Skipped: 0
Running com.fidelity.leap.sprint7.legacy.RecordTradeTest
Tests run: 2, Failures: 0, Errors: 0, Skipped: 0
Running com.fidelity.leap.sprint7.legacy.TradeReportGeneratorCharacterisationTest
Tests run: 1, Failures: 0, Errors: 0, Skipped: 0

Tests run: 6, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

## Part A — the extraction

```java
static void recordTrade(String ticker, double value, double fee) {
    if (tot.containsKey(ticker)) {
        tot.put(ticker, tot.get(ticker) + value);
        f.put(ticker, f.get(ticker) + fee);
    } else {
        tot.put(ticker, value);
        f.put(ticker, fee);
    }
    c++;
}
```

Called from `doIt()` as `recordTrade(tkr, val, fee);` in place of the original six-line inline
block. Nothing about WHAT the code does changed — only where it lives.

## Part B — the characterisation test, unchanged

The exact same assertions from the demo still pass, byte-for-byte — including the exact same
"Processed 10 trades" count and the exact same `report.csv` content. This is the proof the
extraction was a genuine refactor, not a rewrite.

## Part C — model answer

**What's still getting in the way**: `recordTrade()` reads and writes `TradeReportGenerator`'s
static `tot`, `f`, and `c` fields directly, rather than taking them as parameters or returning a
result. That means `RecordTradeTest` cannot simply call `recordTrade(...)` and check its return
value — it has to reach into `TradeReportGenerator`'s shared static state before AND after the
call (see `@BeforeEach resetSharedState()` in `RecordTradeTest.java`), and that state is shared
with every other test that happens to run in the same JVM.

**Did Extract Method remove the problem? No — it relocated the code, but the coupling to shared
mutable state came with it.** `FeeCalculator.calculateFee()` is a genuinely pure function: same
inputs, same output, no hidden state, testable with zero setup. `recordTrade()` is an extracted
method that is STILL entangled with global state — a smaller, more honest step forward, not a
complete fix. Removing the static fields entirely (replacing them with an instance-level result
object `doIt()` builds up and returns) is a bigger, riskier refactor than either of Module 11's
two steps — worth naming as a candidate for a FUTURE refactor, not something to attempt casually
inside this module.

## Talking points

- This is the honest, useful lesson of the module: not every refactoring step gets you all the
  way to "fully testable." Some steps (Extract Method + Introduce Constant on a pure calculation)
  pay off completely. Others (Extract Method on code entangled with shared state) are still real
  progress — smaller, more readable, independently named — without solving the deeper design
  problem in one move.
- `RecordTradeTest`'s `@BeforeEach` reset is itself worth pointing at: it's extra test code that
  exists ONLY because of the static state. A future refactor that removes `tot`/`f`/`c` entirely
  would let this setup method be deleted along with the coupling it exists to manage.
