# Module 2 Lab — Object-Oriented Principles in Practice

## Objectives

By the end of this lab you will have:

- Applied encapsulation as a design decision that protects an actual invariant
- Used inheritance from an abstract class, and implemented an interface
- Recognised a genuine bad-inheritance anti-pattern and fixed it using composition

## Setup

- Java 21 and Maven installed
- `mvn test` runs the pre-written test suite in `src/test/java` against your implementation

## Task

### Kata A — `Holding` (encapsulation as a design decision)

The simplest kata — start here. `HoldingStarter.java` shows the bad version (a public,
unvalidated field) — read it, but don't modify it. Instead, complete `Holding.java`:

- The quantity field must be **private**.
- The constructor accepts an initial quantity; throws `IllegalArgumentException` if negative.
- `getQuantity()` returns the current quantity.
- `adjust(double delta)` applies `delta`; throws `IllegalArgumentException` (without changing
  state) if the result would go negative.

### Kata B — `BondInstrument` and `CryptoInstrument` (inheritance from an abstract class)

Both extend the given `Instrument` abstract class (which implements `Feeable` — see Kata D).

- `BondInstrument.calculateFee(tradeValue)` — a flat $5.00 fee, regardless of trade size.
- `CryptoInstrument.calculateFee(tradeValue)` — 0.5% of trade value, with a $1.00 minimum
  (i.e. never charge less than $1.00, even on a tiny trade).

### Kata C — `GoodClientRegistry` (recognising and fixing bad inheritance)

`BadClientRegistry.java` shows the bad version (`extends ArrayList<String>`) — read it, but
don't modify it. Instead, complete `GoodClientRegistry.java` using **composition**: it must hold
an internal list privately, and must not extend or implement any collection type itself.

- `addClient(String clientId)` — adds the ID; throws `IllegalArgumentException` if already present.
- `contains(String clientId)` — returns whether the ID is registered.
- `size()` — returns the number of registered clients.

### Kata D — `AnnualServiceFee` (interfaces: a capability, not a hierarchy)

`Feeable.java` is given — a pure interface, one method, no state. Complete `AnnualServiceFee.java`:

- It must `implement Feeable` **directly** — it must not extend `Instrument` or relate to it in
  any way (this is checked automatically, via reflection).
- `calculateFee(tradeValue)` always returns a flat $30.00, regardless of the `tradeValue` argument.

## Running the tests

```bash
mvn test
```

All 16 tests should pass. Two of them check your class hierarchies directly via reflection —
`GoodClientRegistryTest` confirms you used composition, not inheritance; `AnnualServiceFeeTest`
confirms your interface implementation has no relationship to `Instrument` at all.

## Acceptance criteria

- `mvn test` passes with 0 failures and 0 errors.
- `Holding`'s field is private (verified by the test suite via reflection).
- `GoodClientRegistry` does not extend or implement any `Collection` type.
- `AnnualServiceFee` implements `Feeable` directly, with no relationship to `Instrument`.
- Neither `HoldingStarter.java` nor `BadClientRegistry.java` has been modified — they exist only
  to show you the "before."
