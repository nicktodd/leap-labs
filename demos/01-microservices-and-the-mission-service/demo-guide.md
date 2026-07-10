# Module 1 Demo Guide — Microservices & the Mission Service

Deliberately brief and motivating — this module's job is to set up the whole sprint's arc, not
to teach microservices exhaustively. Keep it under 20 minutes.

## Open With the Diagram

Show `monolith-vs-service.png`. Point at the Sprint 5 box first — everything ran in one process,
one `main()` method, reading a file and printing to a console. Then point at the Sprint 6 box:
the same core logic (`OrderValidator`, `OrderProcessingEngine`, `HoldingUpdater` — literally the
same classes) now sits behind an HTTP boundary, talks to a separate auth service, and persists to
a real database.

**Say explicitly: nothing about the business logic changed.** This is the whole point of Sprint
5's SOLID work paying off a second time — the classes that were designed to not know about their
concrete collaborators don't care whether they're being called from a `main()` method or a REST
controller.

## Microservices: Benefits and Trade-offs, Kept Brief

Don't turn this into a full architecture lecture. Cover, in a few minutes each:

**Benefits:**
- Independent deployment — the Order Processing service can ship without redeploying the auth
  service, or anything else
- Independent scaling — if order volume spikes, scale that one service, not everything
- Clear ownership boundaries — a team can own a service without needing to understand every
  other service's internals

**Trade-offs (say these just as plainly):**
- Network calls replace method calls — slower, and can fail in ways a direct call never does
- Data consistency across services is genuinely harder than one shared in-memory `Map`
- More moving parts to deploy, monitor, and debug — a monolith's stack trace is one process; a
  service's problem might be three services away

**The honest framing:** neither is "better" — it's a trade-off made for specific reasons (team
boundaries, independent scaling needs, security isolation). For this mission, the reason is
concrete: order processing needs to be a separately deployable, separately securable piece of a
larger system that will eventually include other services this cohort doesn't build.

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
