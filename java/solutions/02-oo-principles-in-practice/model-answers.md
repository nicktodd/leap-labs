# Module 2 Lab - Model Answer Notes

See `src/main/java/com/neueda/leap/mission/engine/`. Verified: `mvn test` passes all 16 tests.

Key points to check in a delegate's solution:

- **`CryptoInstrument` uses `Math.max(fee, MINIMUM_FEE)`**, not an `if` that only checks one
  direction - a delegate who writes `if (fee < MINIMUM_FEE) fee = MINIMUM_FEE;` is functionally
  fine, but `Math.max` is worth pointing out as the more idiomatic one-liner.
- **`Holding`'s `adjust()` computes the new quantity in a local variable before assigning it** -
  a delegate who does `quantity += delta; if (quantity < 0) throw ...;` has a real bug: the field
  is mutated *before* the check, so a rejected adjustment leaves the object in a corrupted state
  despite throwing. The test `adjustRejectsADeltaThatWouldGoNegative` explicitly checks quantity
  is unchanged after a rejected call - this is the test that catches that exact mistake.
- **`GoodClientRegistry` must genuinely not extend or implement any collection type** - a
  delegate who "fixes" `BadClientRegistry` by adding a duplicate check but still extending
  `ArrayList` hasn't actually solved the problem: every other inherited `ArrayList` method (like
  `remove(int)`) still bypasses that check. The `doesNotExtendAnyCollectionType` reflection test
  exists specifically to catch this half-fix.
- **`addClient`'s duplicate check happens before adding**, not by checking `size()` afterwards or
  similar - straightforward, but worth confirming a delegate didn't invert the logic.
- **`AnnualServiceFee` must implement `Feeable` directly, with no relationship to `Instrument`
  whatsoever.** A delegate who makes it `extends Instrument` (perhaps to reuse `getTicker()`, or
  out of habit from Kata A) has recreated exactly the reuse-only-inheritance mistake
  `BadClientRegistry` was meant to teach against - the `doesNotExtendInstrument` reflection test
  exists specifically to catch this.
