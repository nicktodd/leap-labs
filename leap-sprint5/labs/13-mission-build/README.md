# Module 13 Lab — Mission Build

## Objectives

By the end of this lab you will have:

- Built the two genuinely new pieces of the mission engine — `SettlementReport` and
  `OrderProcessingEngine` — wiring together everything built in Modules 1-12
- Seen an entire sprint's worth of separately-built, separately-tested classes work together
  correctly the first time they're actually connected

## Setup

- Java 21 and Maven installed
- `mvn test` runs the pre-written test suite in `src/test/java` against your implementation
- Given, don't modify: `Instrument.java`, `Feeable.java`, `EquityInstrument.java`,
  `BondInstrument.java`, `FundInstrument.java`, `Holding.java`, `OrderRequest.java`,
  `ValidationResult.java`, `OrderValidator.java`, `HoldingUpdater.java`, `Client.java`,
  `Portfolio.java`, `InstrumentFactory.java`, `IncomingOrder.java`, `OrderBatchReader.java` — all
  of these already exist, already tested, from earlier modules

## Task

### Kata A — `SettlementReport`

Implements mission-brief requirement 6. Format exactly:

```
Settlement Report
<clientId> <ticker>: ACCEPTED, fee $<fee>
<clientId> <ticker>: REJECTED - <reason>
... one line per order, in the order recorded ...
Total fees: $<sum of all accepted fees>
```

### Kata B — `OrderProcessingEngine`

The orchestrator. Its constructor takes the client map, an `OrderValidator`, and a
`HoldingUpdater`. `process(orders)` should, for each order:

1. Look up the `Client` by `order.getClientId()`, and their `Portfolio`
2. Get the `Holding` for `order.getInstrument().getTicker()`
3. Build an `OrderRequest` from the order's quantity, price, and buy/sell flag
4. Call `OrderValidator.validate(...)`, passing the holding's current quantity, the portfolio's
   current total value, and the client's risk limit
5. **If valid:** calculate the fee via `order.getInstrument().calculateFee(...)`, apply the order
   to the holding via `HoldingUpdater`, adjust the portfolio's total value (add the trade value
   for a buy, subtract it for a sell), and record it as accepted
6. **If invalid:** record it as rejected with the validator's reason, and change nothing else —
   this is mission-brief requirement 4, word for word

## A Note on What You're Actually Doing Here

Notice that neither kata requires you to make a single design decision about fee rules,
validation rules, or how a holding gets adjusted — all of that was decided, built, and tested in
earlier modules. Your job is coordination only. If you find yourself wanting to add a special
case or recalculate something that `Instrument`, `OrderValidator`, or `HoldingUpdater` already
handles, stop — that's a sign you're duplicating logic that already has a home (Module 9).

## Running the tests

```bash
mvn test
```

All 10 tests should pass. `OrderProcessingEngineTest` runs full batches through
`OrderBatchReader` — the same CSV-line format mission-brief.md describes — and checks both the
rendered report and the resulting portfolio/holding state.

## Acceptance criteria

- `mvn test` passes with 0 failures and 0 errors
- `OrderProcessingEngine` performs no fee calculation, validation logic, or holding-adjustment
  logic itself — it only calls out to the classes that already own those decisions
- A rejected order leaves the client's portfolio and holdings completely unchanged
