# Module 13 Demo Guide — Mission Build

Run `MissionEngineDemo` first, then walk backward through what's actually new versus what's
being reused.

```bash
mvn package
java -cp target/classes com.neueda.leap.sprint5.MissionEngineDemo
```

## What's Reused, Unchanged, From Earlier Modules

Put this on screen and go through it explicitly — it's the point of the whole module:

| Class | Where it was built | What changed to use it here |
|---|---|---|
| `Instrument`, `Feeable`, `EquityInstrument`, `BondInstrument`, `FundInstrument` | Modules 1-2, 7 (OCP kata) | Nothing |
| `Holding` | Module 2 | Nothing |
| `OrderRequest`, `ValidationResult`, `OrderValidator` | Module 12 (built test-first from the mission brief) | Nothing |
| `HoldingUpdater` | Module 12 (lab) | Nothing |

**Four pieces, built across five separate modules over the last two days, and none of them
needed a single line changed to slot into a working end-to-end engine.** That's the payoff of
Module 7's SRP and Module 8's DIP — each piece only ever depended on an abstraction or a value
it was directly given, never on how it would eventually be wired together.

## What's Actually New

- `Client`, `Portfolio` — new, but small, and follow the same composition pattern from Module 4's
  class diagram (`Client` has a `Portfolio`, has many `Holding`s)
- `InstrumentFactory` — turns a plain string (`"EQUITY"`) from an order file into the right
  `Instrument` subtype. Point out: adding a new instrument type later means one new `case` here
  plus one new class — Module 7's OCP, still holding
- `OrderBatchReader` — implements mission-brief requirement 2 ("orders arrive... from an upstream
  system... a CSV/text file") literally
- `SettlementReport` — implements requirement 6
- `OrderProcessingEngine` — the coordinator. Walk through `process()` line by line: for each
  order, look up the client and holding, build an `OrderRequest`, hand it to `OrderValidator`,
  branch on the result. **Nothing here recalculates a fee rule or re-checks a risk limit — it
  only ever calls out to the class that already owns that decision.**

## Trace the Rejected Orders Back to Requirement 4

Point at the two `REJECTED` lines in the output. Requirement 4 said: "If an order fails
validation, it is rejected with a reason, and does not affect the client's portfolio." Prove the
second half live: show that `C002`'s portfolio total value is still `0` after the batch, and that
`C001`'s `MSFT` holding was never created — the rejected orders genuinely had zero effect.

## The AAPL Holding Number Is the Whole Story in One Line

`100` (bought) `- 20` (sold) `= 80`. Trace that number back through `OrderProcessingEngine` to
`HoldingUpdater.applyOrder()` to `Holding.adjust()` — three classes, three modules, one correct
number, and the instructor never had to trust any of it blindly, because every one of them
already has its own passing test suite from the module that built it.

## Points to Make Explicitly

- **This is not a rewrite.** Nothing from Modules 1-12 was thrown away or redone — Module 13 is
  entirely about wiring, plus the small amount of genuinely new glue code (`Client`, `Portfolio`,
  `OrderBatchReader`, `SettlementReport`, `OrderProcessingEngine`).
- **If any of the reused pieces had a bug, it would already have been caught** by that module's
  own test suite, long before it ever got wired in here. That's the entire argument for building
  test-first, module by module, rather than writing the whole engine in one pass at the end.

## Transition to the Lab

Learners build the same two genuinely-new pieces themselves — `SettlementReport` and
`OrderProcessingEngine` — wiring together the same already-tested components, verified against a
provided order file and an exact expected report.
