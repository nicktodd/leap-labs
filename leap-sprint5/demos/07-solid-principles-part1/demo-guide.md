# Module 7 Demo Guide — SOLID Principles Part 1 (S, O, L)

Run `SolidDemo.java` end to end first, then walk back through it section by section. Each
section is a direct payoff of earlier modules — make that link explicit as you go.

```bash
mvn package
java -cp target/classes com.neueda.leap.sprint5.SolidDemo
```

## S — Single Responsibility Principle

`BadReportGenerator` is Module 6's `flawed-design.mmd` `OrderManager`, in code — one method does
calculation, formatting, *and* "delivery" (a `println` standing in for email). Point out: the
output is identical whether you call `BadReportGenerator` or the split `FeeAggregator` +
`FeeReportFormatter` pair. **SRP is not about behaviour changing — it's about how many reasons a
class has to change.** Ask the group: name a change to the fee rule, the report format, and the
delivery mechanism, one at a time. In the bad version, all three risk touching the same file. In
the good version, each touches exactly one.

## O — Open/Closed Principle

`DerivativeInstrument` is a brand new instrument type with its own fee rule. The demo's point
isn't the 2% calculation — it's the sentence in the console output: *zero changes to Instrument,
Feeable, Order, FeeAggregator, or FeeReportFormatter*. This is the direct payoff of Module 1-2's
`Feeable` interface: the abstraction was built before this requirement existed, and it absorbed
the new requirement without being touched. Ask: what would adding a new instrument type have
looked like against `flawed-design.mmd`'s `OrderManager` instead? (Answer: an edit to
`calculateFee(order)`, risking every existing instrument type's fee logic in the same change.)

## L — Liskov Substitution Principle

This is the subtlest of the three, so slow down here. Run the demo and watch `adjustAll` crash on
`FrozenHoldingBad` even though the calling code only ever declared `List<Holding>` — nothing
about the *type* warned the caller this could happen. Contrast with `Holding.adjust()`'s own
`IllegalArgumentException`: that one's fine, because it's part of the documented contract every
caller already expects (don't let the quantity go negative). The problem isn't "throwing
exceptions" — it's throwing *unconditionally*, breaking a promise the type claims to keep.

Show the fix: `FrozenHolding` doesn't extend `Holding` at all — it wraps one (composition, same
pattern as Module 4's `Portfolio`/`Holding` relationship). No `adjust()` method exists on it, so
there's no contract to break.

## Points to Make Explicitly

- **All three of today's fixes are things you already did in Modules 1-2 and 4**, without the
  vocabulary for them yet: `Holding`'s encapsulation, `Feeable`'s abstraction, composition over
  inheritance. SOLID names patterns you've already been practising.
- **These three are about structure, not correctness.** `BadReportGenerator` and the SRP-split
  version produce identical output. The value is entirely in how easy each is to change safely.

## Transition to the Lab

Learners implement the same three fixes themselves: `FeeAggregator`/`FeeReportFormatter` (SRP),
`DerivativeInstrument` (OCP), and `FrozenHolding` (LSP) — with `FrozenHoldingBad.java` given as
the "before," exactly as in this demo.
