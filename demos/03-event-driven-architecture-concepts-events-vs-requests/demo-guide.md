# Module 3 Demo Guide — Event-Driven Architecture Concepts: Events vs Requests

Run both, back to back, and read the timestamps out loud.

## Run the Request-Driven Example

```bash
mvn compile
java -cp target/classes com.fidelity.leap.sprint7.RequestDrivenExample
```

Expect one call after another, each ~400ms, totalling roughly 1.2 seconds. **Point at this
explicitly**: `OrderService` calls `PricingService`, waits for a response, THEN calls
`RiskService`, waits, THEN calls `ConfirmationService`, waits. It cannot proceed to the next line
until the current call returns. It also has a compile-time dependency on all three — add a fourth
thing that needs to know about a new order (say, a new fraud-detection check) and `OrderService`
itself has to be changed to call it.

## Run the Event-Driven Example

```bash
java -cp target/classes com.fidelity.leap.sprint7.EventDrivenExample
```

Expect `publish()` to return in single-digit milliseconds, while the three listeners finish
300ms, 620ms, and 919ms later — each independently, none of them blocking `OrderService`, none of
them known to `OrderService` at all. **Read the source together**: `OrderService` (in `main`)
never references `PricingHistoryListener`, `RiskAuditListener`, or `ConfirmationListener` by name.
It publishes one fact — `OrderPlacedEvent` — and has no idea who's listening, how many listeners
there are, or what any of them do.

## The Actual Distinction

- **Request-driven**: the caller knows exactly who it's talking to, waits for an answer, and is
  coupled to that specific thing existing. Good when you genuinely need an answer before
  proceeding — you can't confirm risk was checked without knowing the risk check happened.
- **Event-driven**: the publisher states a fact and moves on. Any number of unrelated things can
  react, now or later, without the publisher knowing or caring. Good when the publisher doesn't
  need an answer — it just needs to announce something happened.

## Point Forward, Deliberately

Say explicitly: this `EventBus` is a toy — in-memory, single-process, gone the moment this JVM
exits. **Kafka, starting Module 4, is a real, durable, distributed version of exactly this same
idea** — the pattern doesn't change, only the infrastructure underneath it does. Today is about
understanding the pattern well enough that Kafka's concepts land as "oh, that's how they solved
the durability and scale problem," not as a wall of new vocabulary with no context.

## Transition to the Lab

Learners revisit Module 2's three scenarios (end-of-day settlement, live price feed, monthly
statements) and decide event vs request for each — a different axis than batch vs real-time, and
worth being explicit that the two axes aren't the same question, even though they often correlate.
