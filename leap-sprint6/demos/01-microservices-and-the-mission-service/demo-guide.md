# Module 1 Demo Guide — Microservices & the Mission Service

Deliberately brief and motivating — this module's job is to set up the whole sprint's arc, not
to teach microservices exhaustively. Keep it under 20 minutes.

## Define Both Terms Precisely First

Don't assume the group already has a working definition — ask for one before giving your own,
then correct/tighten whatever comes back.

**A monolith**: one deployable unit containing every business capability, one process, usually
one shared database. A method call to another part of the system is just a method call — no
network involved. Sprint 5's Order Processing & Settlement Engine was, structurally, a monolith —
small, but the shape is the same as a much bigger one.

**A microservice**: a small service built around ONE business capability, deployable on its own,
owning its own data, talking to other services only over the network (HTTP, messaging) — never
an in-process method call. A microservice *architecture* is a system made of many of these, each
small enough for one team to fully own.

## Monolith and Microservices: Both Sides, Both Ways

This is the part worth slowing down on — most learners have only heard "microservices good,
monolith legacy," which is wrong and worth correcting directly.

**Monolith — pros:** simple to develop, run, and debug locally; no network calls between
components (fast, and fails only the ways a normal program fails); transactions across the whole
system are trivial (one database, one transaction manager); easier to reason about at small
scale.

**Monolith — cons:** everything deploys together, even a one-line change; everything scales
together, whether or not it needs to; grows harder to understand as it grows, until no one owns
the whole thing; one team's mistake can take the entire system down.

**Microservices — pros:** independent deployment and scaling; clear ownership boundaries; failure
isolation (one service crashing doesn't necessarily take the others down); each service can use
the technology that actually fits it.

**Microservices — cons:** network calls replace method calls, and can fail in new ways; data
consistency across services is genuinely harder; more moving parts to deploy, monitor, and debug;
real operational overhead; testing an end-to-end flow now means running several services together.

**Land the honest conclusion explicitly**: neither is "better" as a default. Sprint 5's engine
was correctly a monolith — small, one team, no need for independent scaling. Sprint 6 has a
concrete, specific reason to split it out (separate deployability, separate security boundary,
part of a larger system this cohort doesn't build) — and if a team can't name a reason that
concrete, that's usually a sign microservices is the wrong call for them, not a safe default.

## Open the Diagram

Show `monolith-vs-service.png`. Point at the Sprint 5 box first — everything ran in one process,
one `main()` method, reading a file and printing to a console. Then point at the Sprint 6 box:
the same core logic (`OrderValidator`, `OrderProcessingEngine`, `HoldingUpdater` — literally the
same classes) now sits behind an HTTP boundary, talks to a separate auth service, and persists to
a real database.

**Say explicitly: nothing about the business logic changed.** This is the whole point of Sprint
5's SOLID work paying off a second time — the classes that were designed to not know about their
concrete collaborators don't care whether they're being called from a `main()` method or a REST
controller.

## Where the Sprint 5 Algorithm Becomes a Service Boundary

Walk through the Sprint 6 half of the diagram slowly:

- The **HTTP boundary** (`POST /orders`) is new — Modules 4-6 design this properly
- **JWT validation against the Node auth service** is new — Module 9
- **MyBatis persistence to Postgres** replaces the in-memory `Map` — Module 7
- **Everything else inside the box** — `OrderValidator`, `OrderProcessingEngine`,
  `HoldingUpdater` — is unchanged Sprint 5 code

## Transition to the Lab

In pairs, 15 minutes, whiteboard or shared doc — not a formal design, just enough to motivate
what's coming: sketch how the Sprint 5 algorithm could become a service boundary. What comes in
over the wire? What goes out? What does it need to talk to? What stays entirely internal?
