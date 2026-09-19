# Sprint 5 Mission: Order Processing & Settlement Engine

This is the business scenario that drives the rest of Sprint 5. Starting in
Module 3, you will design it (on paper, then in UML); starting in Module 12,
you will build it in Java, driven by the design and tests you have written
along the way.

You already have some of the building blocks from Modules 1 and 2:
`Trade`, `Instrument` (and its subclasses `EquityInstrument`, `BondInstrument`,
`CryptoInstrument`, `FundInstrument`), and `Feeable`. The mission reuses and
extends these.

## The Business Problem

LEAP Wealth (our fictional business unit) accepts client instructions
to buy or sell financial instruments, and must process them safely before they
reach a settlement report. Right now this is done by hand. We are building the
**Order Processing & Settlement Engine** to automate it.

## Requirements (as given to the business analyst)

1. A **client** holds a **portfolio**. A portfolio is a collection of
   **holdings** — how much of a given instrument the client currently owns.

2. A client (or their advisor) submits an **order**: buy or sell a given
   quantity of a given instrument, at a given price. Orders arrive in a batch,
   once per day, from an upstream system (for this sprint: a CSV/text file).

3. Before an order can be processed, it must be **validated**:
   - The quantity must be positive.
   - The price must be positive.
   - A **sell** order cannot reduce a holding below zero (the client cannot
     sell what they don't own).
   - A **buy** order cannot be accepted if it would take the client's total
     portfolio value over their **risk limit** (a per-client setting).

4. If an order fails validation, it is **rejected** with a reason, and does
   not affect the client's portfolio. Rejected orders still appear in the
   settlement report.

5. If an order passes validation, it is **executed**: a **fee** is
   calculated (fee rules differ by instrument type — see Modules 1-2), the
   client's holding is updated, and a **confirmation** is recorded.

6. At the end of the batch, a **settlement report** is produced, listing
   every order processed that day, whether it was accepted or rejected (and
   why), and the fee charged for each accepted order.

7. The business wants this system to be easy to extend. In particular, they
   expect to add:
   - New instrument types (e.g., derivatives) with their own fee rules,
     without changing the order validation or execution logic.
   - New validation rules, without rewriting existing ones.
   - New report formats (e.g., a CSV export, alongside the console report),
     without changing how orders are processed.

## What This Means for the Sprint

- **Module 3** (this module): before any diagrams, identify the candidate
  entities, responsibilities, and relationships hiding in the requirements
  above.
- **Modules 4-5**: express that design as UML class and sequence diagrams.
- **Module 6**: peer-review each other's designs.
- **Modules 7-8**: apply SOLID principles to fix the rough edges peer review
  finds — especially around requirement 7 (extensibility).
- **Module 9**: clean code pass.
- **Modules 10-11**: TDD fundamentals and JUnit, practised on pieces of this
  domain.
- **Module 12**: scaffold the real project structure from the UML.
- **Module 13**: build the engine, test-first.
- **Module 14**: wrap-up and design rationale — what changed between your
  Module 3 sketch and what you actually built, and why.

## A Non-Goal

You do not need a database, a UI, or real market data. Orders come from a
file, output is a report (console or file). The interesting problem is the
**design**, not the plumbing.
