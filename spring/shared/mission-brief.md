# This Week's Mission: The Order Processing & Settlement Engine, as a Service

The Java week built the Order Processing & Settlement Engine as a single Java program: read a
batch of orders from a file, validate them, execute them, print a settlement report. This week
turns that same engine into a real, deployable microservice - the natural next step for a system
whose logic already works and is already fully tested.

You already have the hard part. `OrderValidator`, `HoldingUpdater`, the `Instrument`/`Feeable`
fee-calculation hierarchy, and `OrderProcessingEngine` (all from the Java week, Modules 7-13) do
not need to be rewritten - they need a service wrapped around them.

## What Changes, and What Doesn't

**Doesn't change:**
- The business rules (the Java week's `shared/mission-brief.md`, requirements 1-7)
- The core domain logic - validation, fee calculation, holding updates

**Changes:**
- Orders arrive over HTTP, not from a CSV file read once a day
- Client and portfolio data is persisted in Postgres (the Sprint 3 enterprise schema), not held
  in an in-memory `Map<String, Client>`
- Every request must be authenticated - a valid JWT, issued by a separate Node.js auth service
  (introduced in Module 9), is required before an order can be submitted
- The whole thing runs in a container, not as a bare `java -jar`

## The Shape of the Work

1. **Days 1-2**: build the service's skeleton - Spring Boot, layered architecture, REST API
   design, contract-first with OpenAPI, DTOs and validation. No persistence yet, no security yet -
   get the shape right first.
2. **Day 3**: wire in persistence (MyBatis, against the Sprint 3 schema), security (JWT
   validation against the Node auth stub), and centralised error handling.
3. **Day 4**: assemble everything into one working, secured, persisted service (Module 11), then
   containerise it and integration-test it end-to-end against the real auth service (Modules
   12-13).

## Non-Goals

No new business rules this week. If a design decision here conflicts with something the Java week
already decided, the Java week's decision wins unless there's a specific architectural reason
(HTTP, persistence, security) that forces a change - and if so, that reason should be traceable,
the same way the Java week's Module 14 asked you to trace design decisions back to their cause.
