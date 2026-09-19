# Model Answers — SOLID Principles Part 1

## Kata A (SRP): why two classes instead of one

It would be entirely possible to write one `FeeReportGenerator` class with both a
`totalFees(orders)` and a `format(orders, total)` method — the tests wouldn't know the
difference. The point isn't that combining them is *impossible* to get right, it's that keeping
them separate makes each class's job legible from its name alone, and means a change to the
report's presentation (say, switching to CSV) can never accidentally break the fee calculation
logic, because they're not in the same file, let alone the same method.

## Kata B (OCP): what "closed for modification" actually means in practice

The test that matters most here isn't `DerivativeInstrumentTest` — it's the fact that
`Instrument.java`, `Feeable.java`, `Order.java`, `FeeAggregator.java`, and
`FeeReportFormatter.java` are all byte-for-byte identical to how they were before this kata. If
you found yourself needing to add an `if (instrument instanceof DerivativeInstrument)` branch
anywhere, that's a sign the abstraction (the `Feeable` interface) isn't doing its job — the whole
point of Module 1-2's design is that new instrument types are additions, not edits.

## Kata C (LSP): the general test for a Liskov violation

Ask: "if I hand this subtype to code that only knows about the supertype, can anything go wrong
that couldn't go wrong with a genuine instance of the supertype?" For `FrozenHoldingBad`, the
answer is yes — `adjustAll(List<Holding> holdings, ...)` (see Module 7's demo) works fine for
every real `Holding`, and crashes unconditionally the moment a `FrozenHoldingBad` is smuggled in,
because nothing about its *type* (`Holding`) warned the caller this could happen.

The fix isn't "don't throw exceptions" — `Holding.adjust()` itself throws
`IllegalArgumentException` for a specific, documented reason (would go negative), and that's
fine, because it's part of the contract every caller already expects. `FrozenHoldingBad`'s
problem is throwing *unconditionally*, for a reason the type system gives no hint of. Composition
sidesteps the whole issue: if `FrozenHolding` never claims to be a `Holding`, there's no contract
to violate.

## A question worth asking in Module 8

All three katas here fix a specific, already-broken example. Module 8 asks a harder question:
looking at your own Module 4 `mission-model.mmd`, where might an SRP, OCP, or LSP violation
already be hiding, un-flagged, because nobody's tried to substitute or extend it yet?
