# Module 7 Lab — SOLID Principles, Part 1 (S, O, L)

## Objectives

By the end of this lab you will have:

- Split a multi-responsibility class into single-purpose classes (SRP)
- Extended a system with a new instrument type without modifying any existing class (OCP)
- Fixed a Liskov Substitution violation using composition instead of inheritance (LSP)

## Setup

- Java 21 and Maven installed
- `mvn test` runs the pre-written test suite in `src/test/java` against your implementation
- Given, don't modify: `Instrument.java`, `Feeable.java`, `EquityInstrument.java`,
  `BondInstrument.java`, `FundInstrument.java`, `Holding.java`, `Order.java`, `FrozenHoldingBad.java`

## Task

### Kata A — `FeeAggregator` and `FeeReportFormatter` (Single Responsibility Principle)

Two classes, each with exactly one job:

- `FeeAggregator.totalFees(orders)` — sums `order.calculateFee()` across a list of orders
- `FeeReportFormatter.format(orders, total)` — builds the report string, exactly:
  ```
  Settlement Report
  <clientId>: $<fee>
  ... one line per order ...
  Total fees: $<total>
  ```
  (no trailing newline after the total line)

Neither class should know anything about the other's job — `FeeReportFormatter` doesn't
calculate anything itself, `FeeAggregator` doesn't format anything.

### Kata B — `DerivativeInstrument` (Open/Closed Principle)

A new instrument type: a flat 2% fee on trade value. Add it **without** modifying
`Instrument.java`, `Feeable.java`, `Order.java`, or any existing instrument class — extend the
system, don't change what's already there.

### Kata C — `FrozenHolding` (Liskov Substitution Principle)

`FrozenHoldingBad.java` (given, don't modify) extends `Holding` and overrides `adjust()` to
always throw — this breaks the promise `Holding` makes to any code that already depends on it.
Fix this properly in `FrozenHolding.java`, **using composition, not inheritance**:

- `FrozenHolding` must not extend `Holding`
- Constructor takes a `Holding` and holds it as a field
- `getQuantity()` returns the wrapped holding's quantity
- No `adjust()` method should exist on `FrozenHolding` at all — there's no promise to break if
  the type never claimed to support adjustment in the first place

## Running the tests

```bash
mvn test
```

All 10 tests should pass. `FrozenHoldingTest` checks your class hierarchy directly via
reflection — confirming `FrozenHolding` doesn't extend `Holding`, and has no `adjust` method.

## Acceptance criteria

- `mvn test` passes with 0 failures and 0 errors
- `FeeAggregator` and `FeeReportFormatter` each do only what their name says
- `DerivativeInstrument` required no changes anywhere else in the codebase
- `FrozenHolding` uses composition, not inheritance, and exposes no `adjust()` method
