# Model Answers — TDD in Practice

## Why `HoldingUpdater` doesn't duplicate `Holding`'s own check

Cycle 4 (selling more than the current holding throws) passes without any new code, purely by
delegating to `Holding.adjust()`. That's the right outcome, not a coincidence to paper over: it
demonstrates `HoldingUpdater`'s actual responsibility is *translating* a buy/sell decision into a
signed adjustment, not *re-validating* the business rule that `Holding` already owns. If
`HoldingUpdater` re-implemented the "can't go negative" check itself, that would be duplicated
logic (Module 9's checklist) that could drift out of sync with `Holding`'s own rule over time —
one bug fix in `Holding.adjust()` wouldn't automatically fix a parallel bug in `HoldingUpdater`.

This is worth contrasting with `OrderValidator` (the demo): it *does* independently check "sell
more than the current holding" as part of pre-execution validation, using `currentHoldingQuantity`
passed in as a plain number — it has no reference to an actual `Holding` object to delegate to.
Two classes checking "the same" business rule isn't automatically duplication; it depends on
whether they're checking it for the same reason, at the same point in the flow.

## Why `OrderValidator` and `HoldingUpdater` are separate classes at all

This is Module 7's SRP, showing up again: `OrderValidator` decides *whether* an order should
proceed; `HoldingUpdater` decides *how* to apply one that already has. Module 13's mission build
will wire these together (plus `Instrument`'s fee calculation) inside something like an
`OrderExecutor` — but neither `OrderValidator` nor `HoldingUpdater` needs to know that the other
exists.

## How this generalises to Module 13

Every piece of Module 13's mission build should be approached the way both of today's
components were: read the relevant `shared/mission-brief.md` requirement, write the simplest
test that captures one fact from it, and let the implementation grow exactly as far as the tests
demand — no further, and no design decisions made in the abstract before a test forces them.
