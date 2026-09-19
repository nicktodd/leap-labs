# Model Answer — Order Processing & Settlement Engine

This is **a** defensible design, not **the** correct one. If your pair made different, reasoned
calls, that's fine — bring the disagreement to Module 6's peer review.

## Class or attribute?

| Candidate | Class or attribute? | Reasoning |
|---|---|---|
| Client | Class | Has identity (a client ID), owns a portfolio, has a risk limit |
| Portfolio | Class | More than a bare list — it has a total value, computed from holdings |
| Holding | Class | Has its own state (instrument + quantity) and its own behaviour (apply a delta) — this is `Holding` from Module 2, reused |
| Order | Class | Has identity, state (pending/accepted/rejected), and its own fields (instrument, quantity, price, direction) |
| Instrument | Class hierarchy | Already exists from Modules 1-2 (`Instrument`, `EquityInstrument`, `BondInstrument`, `CryptoInstrument`, `FundInstrument`) |
| Risk limit | Attribute of `Client` | It's just a number scoped to one client — no behaviour or identity of its own |
| Fee | Attribute of `Order` (once executed) | A calculated value attached to one order, not something with its own identity or lifecycle |
| Confirmation | Could go either way | Simplest: an attribute/status on `Order`. More elaborate: its own class if you want an audit trail separate from the order itself. Either is defensible — this is one of the ambiguous calls worth flagging in peer review. |
| Settlement report | Class | Coordinates output — not a noun with pre-existing behaviour, but earns its place because "produce a report from a batch of orders" is a distinct responsibility |
| Order batch / order source | Class | Something has to read the day's orders from the upstream file — this responsibility doesn't belong to `Order` itself |

## Responsibilities (verb -> owning class)

| Responsibility | Owning class | Why this class, not another? |
|---|---|---|
| Validate an order (quantity/price positive, sell doesn't go negative, buy doesn't breach risk limit) | An `OrderValidator` (or a set of validator objects) | Deliberately **not** on `Order` or `Client` — validation needs both, plus is exactly the kind of logic the business wants to extend later (requirement 7). Putting it in its own class is what makes SOLID (Modules 7-8) possible later. |
| Reject an order, with a reason | `OrderValidator` decides; `Order` records the outcome | Separates "deciding" from "recording the decision" |
| Calculate a fee | `Instrument` subclasses, via `Feeable` | Already built in Modules 1-2 — reused, not reinvented |
| Execute an order (apply fee, update holding) | An `OrderExecutor` (or similar coordinating class) | Same reasoning as validation: this needs `Order`, `Client`'s `Portfolio`, and the fee calculation together — no single existing class owns all three naturally |
| Update a holding | `Portfolio` (delegating to `Holding.adjust()`) | `Portfolio` knows which holding to update; `Holding` (Module 2) already knows how to safely adjust itself |
| Produce the settlement report | `SettlementReport` | Distinct responsibility, and requirement 7 explicitly asks for multiple report formats later — a strong signal this deserves its own class now, not a stray method on something else |

## Relationships (sketch)

- `Client` **has one** `Portfolio`, **has a** risk limit
- `Portfolio` **has many** `Holding`s
- `Holding` **refers to** one `Instrument`
- `Order` **refers to** one `Client` and one `Instrument`
- `OrderValidator` **depends on** `Order`, `Client` (for risk limit and current holdings)
- `OrderExecutor` **depends on** `OrderValidator`, `Order`, `Portfolio`, and the `Instrument`'s
  `Feeable` fee calculation
- `SettlementReport` **depends on** the full batch of processed `Order`s (with their outcomes)

## The genuinely ambiguous call, and why it matters

**Confirmation as its own class, or a status on `Order`?** Keeping it simple (a status field) is
the right call *for now* — YAGNI. But if the business later needs an audit trail that survives
independently of the order (e.g., confirmations get archived on a different schedule than orders),
promoting it to its own class becomes worth it. This is exactly the kind of decision Module 14's
"design rationale" retrospective is for: was YAGNI the right call here, in hindsight?

## Why validator/executor as separate classes matters for later modules

Requirement 7 (extensibility: new instrument types, new validation rules, new report formats
without touching existing code) is the requirement SOLID (Modules 7-8) exists to satisfy. If
validation logic were buried as a single large method on `Order` or `Client`, adding a new rule
would mean editing that method — violating Open/Closed. Separating `OrderValidator` out now, even
before you know the word "SOLID," sets up Module 7-8 to *refine* this design rather than rebuild
it from scratch.
