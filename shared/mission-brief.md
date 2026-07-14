# Sprint 7 Mission: The Trading Platform Gets Real-Time, and the Old Code Gets Honest

Sprint 7 has two missions running in parallel, meeting at the end in Module 14.

## Mission A — Real-Time: Kafka for Trade Events

The trading platform (the mission service, built across Sprint 6) currently only knows about
orders the moment they're submitted. Nothing downstream — reporting, the analytics dashboard,
other services that care when a trade happens — finds out unless they poll Postgres themselves.

Sprint 7 adds an event stream: every accepted order also publishes a trade event to Kafka. Any
number of independent consumers can subscribe without the mission service knowing or caring who
they are — the same decoupling principle Sprint 6's JWT validation already taught (the mission
service doesn't call the auth service; here, it doesn't call its consumers either, it just
publishes).

## Mission B — Honesty: the Refactor Codebase

Alongside the new work, this sprint ships a **starter codebase** — a real, running, but visibly
neglected trade-reporting utility. It works. It also has the kind of problems that accumulate in
any codebase left alone for a few years: unclear names, functions doing three jobs, no tests
protecting behaviour before someone "improves" it. Module 1 asks you to look at it honestly,
before touching anything. Modules 10-13 give you the tools to fix it *safely* — characterisation
tests before refactoring, automated quality gates, security scanning in CI — using the same
codebase throughout, so the improvement is visible and real, not a toy example.

## Where They Meet: Module 14

The mission's analytics dashboard (introduced in Sprint 4) gets extended to consume from **both**
sources at once: the new Kafka event stream for real-time trade activity, and a batch-loaded
warehouse table (Module 7) for historical/end-of-day data. Two different data-movement patterns,
feeding one dashboard, each used where it's actually the right tool — not because real-time is
"better," but because some data genuinely needs to be current-to-the-second and some genuinely
doesn't.

## What Changes, and What Doesn't

**Doesn't change:**
- The mission service's core order-processing logic (Sprint 6) — Kafka publishing is an addition
  to it, not a rewrite of it
- The Sprint 4 dashboard's existing batch-loaded view

**Changes:**
- Every accepted order now also publishes a trade event to a Kafka topic
- A batch ETL job loads trade data into an analytics warehouse table on a schedule
- The dashboard consumes from both, side by side
- The starter codebase (a separate, smaller utility) goes from "nobody wants to touch it" to
  "safely refactored, tested, and gated in CI" — the same codebase, module by module

## Non-Goals

No new business rules this sprint. Kafka and batch ETL are new *data-movement* mechanisms for
data that already exists and is already correct — this sprint is about how data moves, not what
it means.
