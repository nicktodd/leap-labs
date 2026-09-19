# Module 8 Lab — SOLID Principles, Part 2 (I, D)

## Objectives

By the end of this lab you will have:

- Implemented a segregated interface instead of a fat, everything-bundled one (ISP)
- Made a high-level class depend on an abstraction, injected through its constructor, instead of
  constructing a concrete dependency itself (DIP)

## Setup

- Java 21 and Maven installed
- `mvn test` runs the pre-written test suite in `src/test/java` against your implementation
- Given, don't modify: `Instrument.java`, `Feeable.java`, `EquityInstrument.java`,
  `BondInstrument.java`, `FundInstrument.java`, `Order.java`, `CsvReportable.java`,
  `ConsoleReportable.java`, `ReportWriter.java`, `ConsoleReportWriter.java`,
  `InMemoryReportWriter.java`

## Task

### Kata A — `CsvSettlementReport` (Interface Segregation Principle)

Implement `CsvReportable` — **only** `CsvReportable`, not `ConsoleReportable` too, even though
adding it might feel like harmless future-proofing. Format exactly:

```
clientId,fee
<clientId>,<fee>
... one line per order ...
```

### Kata B — `OrderExecutor` (Dependency Inversion Principle)

`OrderExecutor` needs to write a one-line report for every order it executes — but it must not
construct its own `ConsoleReportWriter` (or any other concrete writer). Instead:

- The constructor takes a `ReportWriter` (the interface) and stores it
- `execute(order)` calculates the fee (`order.calculateFee()`), writes
  `"<clientId>: $<fee>"` through the injected writer, and returns the fee

`InMemoryReportWriter` (given) exists specifically so this can be tested without printing to the
console — that's the payoff of depending on the abstraction rather than a concrete writer.

## Running the tests

```bash
mvn test
```

All 6 tests should pass. `OrderExecutorTest` checks your constructor's parameter type directly
via reflection — confirming it depends on `ReportWriter`, not a specific concrete class.
`CsvSettlementReportTest` confirms `CsvSettlementReport` doesn't implement `ConsoleReportable`.

## Acceptance criteria

- `mvn test` passes with 0 failures and 0 errors
- `CsvSettlementReport` implements only `CsvReportable`
- `OrderExecutor`'s constructor takes a `ReportWriter`, and never constructs a concrete writer
  itself
