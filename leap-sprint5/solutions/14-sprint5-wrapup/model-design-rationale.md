# Model Design Rationale — Order Processing & Settlement Engine

A worked example, using decisions that were genuinely made (and flagged as open questions) across
Modules 3-13 of this course. Yours doesn't need to match this — the point is the shape of the
reasoning, not these specific answers.

## Decision 1 — Confirmation: status field, or its own class?

**Module 3's worksheet:** flagged this explicitly as the one ambiguous call — "Confirmation as
its own class, or a status on Order? Keeping it simple (a status field) is the right call *for
now* — YAGNI."

**Module 4's class diagram:** kept it as a status field on `Order`. Nothing changed yet, because
nothing had tested the decision.

**Module 13's actual build:** `SettlementReport` records accepted/rejected as report entries, not
as state on `Order` at all — `Order` (via `IncomingOrder`) never even gained a status field. The
report itself became the record of outcome.

**Survived, revised, or dropped?** Revised — not in the direction either Module 3 option
anticipated. Neither "status field on Order" nor "separate Confirmation class" turned out to be
where this data actually needed to live.

**What caused the change?** Module 13's actual orchestration logic (`OrderProcessingEngine`)
made it clear the *report* was the natural place to record an outcome — it's built once, for the
whole batch, specifically to answer "what happened to every order." Retrofitting a status onto
`Order` itself would have meant two sources of truth for the same fact.

## Decision 2 — OrderValidator and OrderExecutor as separate classes

**Module 3's worksheet:** already separated "validate an order" and "execute an order" as
distinct responsibilities, assigned to different (at the time, unnamed) classes — explicitly
reasoned as "deliberately not on Order or Client... exactly the kind of logic the business wants
to extend later."

**Module 4's class diagram:** `OrderValidator` and `OrderExecutor` appear as separate classes,
`OrderExecutor` depending on `OrderValidator`.

**Module 13's actual build:** `OrderValidator` (built test-first in Module 12, straight from the
Module 3 wording) and the coordination logic in `OrderProcessingEngine` (which plays the
`OrderExecutor` role, renamed) — still two separate responsibilities, still not merged.

**Survived, revised, or dropped?** Survived, essentially unchanged, from the very first worksheet
through to the final build.

**What caused it to survive?** Nothing forced a change, and that's itself worth noting — Module
6's peer review, Module 7's SRP, and Module 12's actual TDD build all independently confirmed the
same split was correct. Three different checkpoints agreeing is stronger evidence than any one of
them alone.

## Decision 3 — Where fee calculation lives

**Module 3's worksheet:** assigned "calculate a fee" to `Instrument` subclasses via `Feeable`,
reusing work already built in Modules 1-2.

**Module 4's class diagram:** `Instrument` implements `Feeable`; `EquityInstrument`,
`BondInstrument`, `FundInstrument` each override `calculateFee()`.

**Module 13's actual build:** unchanged — `OrderProcessingEngine` calls
`order.getInstrument().calculateFee(tradeValue)` directly, with zero fee logic anywhere in the
orchestration layer.

**Survived, revised, or dropped?** Survived unchanged, from Module 1 all the way through.

**What caused it to survive?** This is the module's clearest example of design paying off ahead
of when it was needed — `Feeable` was built in Module 1-2 for a much simpler reason (teaching
interfaces), and turned out to be exactly the abstraction the real mission needed later, without
modification. Module 7's OCP kata (`DerivativeInstrument`) proved this concretely months before
the final build, by adding a new instrument type without touching anything else.

## Overall Reflection

**Which module's feedback changed the design the most?** Module 3 itself, ironically — not a
later module correcting it. The mission brief's explicit call-out of the Confirmation ambiguity
meant that decision was always going to need revisiting; every other early decision that *wasn't*
flagged as ambiguous survived unchanged.

**What would we design differently, knowing what we know now?** `Portfolio.adjustTotalValue()`
takes a signed delta from the caller (`OrderProcessingEngine` decides the sign). In hindsight,
`Portfolio` itself could own "apply this order's effect," the same way `Holding` owns validating
its own adjustment — this is a live SRP question, not a mistake, and would be a reasonable thing
to revisit in a real second iteration.

**Was there a decision we were confident about that turned out wrong?** Not wrong exactly, but
under-specified: nothing in Module 3-4 anticipated that `OrderBatchReader` would need its own
factory (`InstrumentFactory`) to turn a plain string into an `Instrument`. This wasn't visible
until Module 13's actual file-reading requirement forced it — a good example of a design gap that
diagrams alone couldn't have caught, because it only exists at the boundary with the outside
world (a CSV file), which UML diagrams don't naturally represent.
