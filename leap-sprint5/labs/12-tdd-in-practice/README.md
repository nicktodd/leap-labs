# Module 12 Lab — TDD in Practice

## Objectives

By the end of this lab you will have:

- Built a real piece of the mission (`HoldingUpdater`) entirely test-first
- Applied Module 11's JUnit organisation (`@Nested`, `@DisplayName`) to a suite you write yourself
- Produced a component that complements the demo's `OrderValidator` — together they cover
  validation and execution for one order

## Setup

- Java 21 and Maven installed
- `Holding.java` is given, don't modify (from Module 2) — `HoldingUpdater.java` and
  `HoldingUpdaterTest.java` both start essentially empty, you write both, incrementally, together
- `tdd-log-template.md`, for recording each cycle as you go

## The Business Rule

`HoldingUpdater.applyOrder(Holding holding, boolean isBuy, double quantity)` applies an
**already-validated** order to a holding:

- A buy increases the holding's quantity by `quantity`
- A sell decreases the holding's quantity by `quantity`
- A non-positive `quantity` is a programming error at this point (validation should have caught
  it already) — throw `IllegalArgumentException`
- Selling more than the current holding should fail — but notice `Holding.adjust()` (Module 2)
  already enforces this. Let it.

**Do not implement this from the spec above in one go.** Follow the sequence below.

## The Sequence

1. **Red:** applying a buy of `10` to a `Holding` starting at `100` results in a quantity of
   `110`.
   **Green:** the smallest implementation — even if it only handles buying so far.

2. **Red:** applying a sell of `10` to a `Holding` starting at `100` results in a quantity of
   `90`.
   **Green:** now you're forced to branch on `isBuy`.

3. **Red:** applying a buy of `-5` throws `IllegalArgumentException`.
   **Green:** a guard clause.

4. **Red:** applying a sell of `200` to a `Holding` starting at `100` throws
   `IllegalArgumentException`.
   **Green:** this might already pass — `Holding.adjust()` already enforces the non-negative
   invariant. If it does already pass, that's not wasted effort: it's confirming
   `HoldingUpdater` correctly delegates to `Holding` rather than re-implementing the check
   itself. Log this in your TDD log either way.

5. **Refactor:** organise your test class with `@Nested` — for example, `WhenBuying` and
   `WhenSelling` — with `@DisplayName` on each.

## A Question to Sit With, Not Answer Immediately

`HoldingUpdater` and `Holding` both end up capable of rejecting an over-large sell — one by
delegation, one by its own invariant. Is that duplication, or is it two different classes each
correctly guarding their own boundary? There's a defensible answer either way; note your view in
the TDD log's reflection section.

## Deliverable

- `HoldingUpdater.java` and `HoldingUpdaterTest.java`, both fully built
- A completed `tdd-log-template.md`

## Acceptance criteria

- `mvn test` passes with 0 failures and 0 errors
- At least 4 tests exist, matching the 4 red-green steps above
- Tests are organised with at least two `@Nested` groups, each with a `@DisplayName`
- The TDD log has one entry per cycle
