# Module 12 Demo Guide — TDD in Practice

This is where Modules 3, 7-11 converge: build a real piece of the mission
(`OrderValidator`, straight from `shared/mission-brief.md` requirement 3), test-first, using
JUnit's organisational features from Module 11.

Delete `OrderValidator.java`'s body, `ValidationResult.java`, and
`OrderValidatorTest.java`'s contents before the session. Build it back up live, in this order.

## Before Writing Any Code: Read the Requirement Together

> "3. Before an order can be processed, it must be validated: the quantity must be positive; the
> price must be positive; a sell order cannot reduce a holding below zero; a buy order cannot be
> accepted if it would take the client's total portfolio value over their risk limit."
>
> "4. If an order fails validation, it is rejected with a reason..."

Point out: requirement 4's "with a reason" is *why* this build starts with a small value type
(`ValidationResult`), not a plain `boolean` — the test-first process surfaces this design need
immediately, because the very first test can't be written meaningfully without deciding what
`validate()` returns.

## Cycle 1: The Simplest Valid Case, and `ValidationResult` Is Born

**Red:**
```java
@Test
void acceptsAValidBuyOrder() {
    OrderRequest request = new OrderRequest(10, 100, true);
    ValidationResult result = validator.validate(request, 0, 0, 5000);
    assertTrue(result.isValid());
}
```
This doesn't compile yet — `OrderRequest` and `ValidationResult` don't exist. Write the smallest
versions of both that make this compile and pass: `OrderRequest` with three fields and a
constructor; `ValidationResult` with a static `valid()` factory and `isValid()`.

**Green:**
```java
public ValidationResult validate(OrderRequest request, double currentHoldingQuantity,
                                  double currentPortfolioValue, double riskLimit) {
    return ValidationResult.valid();
}
```
Say it out loud again: yes, this ignores every parameter. That's correct — nothing has demanded
otherwise yet.

## Cycle 2-3: The Order Shape Checks

**Red** (quantity): `new OrderRequest(-5, 100, true)` should be invalid, with reason `"quantity
must be positive"`. This forces `ValidationResult.invalid(reason)` and `getReason()` into
existence too.

**Green:** the first `if` branch.

**Red** (price): same pattern, forces the second `if` branch.

## Cycle 4: Selling

**Red:** selling more than the current holding should be rejected. This is the first test that
actually uses `currentHoldingQuantity` — point out that the parameter existed since Cycle 1 but
was **dead** (never read) until this test forced it to matter.

**Green:** the sell-side `if`.

**Refactor moment:** organise the growing test class into `@Nested` groups now, before it gets
harder to do — `WhenOrderShapeIsInvalid`, `WhenSelling`, `WhenBuying`. Do this live; re-run tests
immediately after to prove the reorganisation didn't change behaviour.

## Cycle 5: Buying

**Red:** a buy that would push `currentPortfolioValue + tradeValue` over `riskLimit` should be
rejected.

**Green:** the buy-side `if`.

## Cycle 6: The Boundary Tests

Add `acceptsSellingExactlyWhatIsHeld` and `acceptsBuyExactlyAtRiskLimit` — both should already
pass if `>` (not `>=`) was used correctly in Cycles 4-5. Run them. If either fails, it's caught
here, immediately, rather than as a production incident.

## Points to Make Explicitly

- **The requirement drove the design, not the other way round.** `ValidationResult` exists
  because requirement 4 demanded a reason — nobody sat down and designed a "result object
  pattern" in the abstract first.
- **Every `@Nested` group corresponds to a natural grouping in the requirement text itself**
  (order shape, selling, buying) — the test structure documents the business rule structure.
- **This is the same five-cycle shape as Module 10's `FeeBandClassifier` kata**, just applied to
  a real requirement instead of an invented one. The discipline transfers directly.

## Transition to the Lab

Learners build a complementary piece — `HoldingUpdater`, which applies an already-validated
order to a `Holding` — using the exact same test-first discipline, working from
`labs/12-tdd-in-practice/README.md`.
