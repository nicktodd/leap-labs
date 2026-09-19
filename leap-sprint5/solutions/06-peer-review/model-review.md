# Model Review — `demos/06-peer-review/flawed-design.mmd`

A worked example of what a good review looks like, applied to the deliberately flawed
`OrderManager` design from the demo. This is **a** defensible review, not **the** only correct
set of comments — the point is the *shape* of good feedback, not this exact wording.

## Comments

**1. Responsibility and cohesion — `OrderManager` does too much**
> `OrderManager` has six public methods spanning five distinct responsibilities: validation
> (`validateOrder`), execution (`processOrder`, `updateHolding`), fee calculation
> (`calculateFee`), reporting (`printReport`), and notification (`sendEmail`). Consider splitting
> this into `OrderValidator`, `OrderExecutor`, and a separate reporting/notification path (see
> Module 3's worksheet, which already separates these). One class handling all of them makes it
> hard to test any one responsibility in isolation, and any future requirement change (e.g., a
> new report format) risks breaking unrelated logic.

**2. Encapsulation — every field is public**
> Both `orders` and `clientBalances` on `OrderManager`, and every field on `Order`, are public.
> Nothing stops `orders` being mutated from anywhere in the codebase with no validation — compare
> to `Holding` from Module 2, where the constructor and `adjust()` are the only way to change
> `quantity`, and both enforce the non-negative invariant. The same pattern should apply here:
> make the fields private, and expose only the operations that are actually needed.

**3. Reuse of existing work — fee calculation is reinvented**
> `calculateFee(order)` on `OrderManager` duplicates logic that `Instrument`/`Feeable` (Modules
> 1-2) already provide per instrument type. As written, this design either ignores the different
> fee rules per instrument (equity vs. bond vs. crypto), or reimplements them somewhere new,
> disconnected from the tested `Feeable` implementations. Delegate to the instrument's own
> `calculateFee()` instead.

**4. Traceability — `sendEmail(client)` isn't in the requirements**
> `shared/mission-brief.md` doesn't mention client notification anywhere in its seven
> requirements. Either this is a genuine hidden requirement worth raising with the "business" (the
> instructor), or it's scope that crept in unintentionally. Either way, it's worth a comment:
> silently expanding scope during design is exactly the kind of thing peer review should catch
> before it costs implementation time later.

## Decision

**Request Changes.** The responsibility-splitting and reinvented-fee-logic issues (comments 1 and
3) are significant enough that building on top of this design would mean re-doing the split later
anyway — better to fix it now, before Modules 7-8 (SOLID) and before any Java code exists.

## What a defensive response would look like (don't do this)

> "It's fine, `OrderManager` just coordinates everything, that's its job."

## What a constructive response looks like

> "Good catch on the fee calculation — I hadn't connected `calculateFee` back to `Feeable` yet.
> I'll split `OrderManager` into a validator and executor, and have execution delegate to the
> instrument's own fee method instead of reimplementing it. I'll leave `sendEmail` out entirely
> unless it turns out to be a real requirement — good spot, I think I remembered it from a
> production system rather than from the brief."
