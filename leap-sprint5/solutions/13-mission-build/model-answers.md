# Model Answers — Mission Build

## What `OrderProcessingEngine` does NOT contain, and why that's the point

Search `OrderProcessingEngine.java` for any arithmetic involving a fee rate, a risk limit
comparison, or a check on whether a sell is too large. There isn't any — every one of those
decisions is a single method call out to a class that already owns it
(`order.getInstrument().calculateFee(...)`, `validator.validate(...)`,
`holdingUpdater.applyOrder(...)`). This is the entire payoff of Modules 7-8's SOLID work,
made concrete: `OrderProcessingEngine` depends on abstractions and pre-built collaborators, not
on reimplementing anything they already do.

## Why the portfolio's total value updates AFTER the fee is calculated, not before

Look at the order of operations inside the `if (result.isValid())` branch: fee is calculated
from `request.tradeValue()` (quantity × price, independent of the portfolio), then the holding is
updated, then the portfolio's total value is adjusted. The fee calculation doesn't depend on
portfolio state at all, so its position relative to the other two operations doesn't matter for
correctness — but validation *does* depend on the portfolio's total value *before* this order is
applied (that's what `riskLimit` is checked against), which is exactly why `validate(...)` is
called with `portfolio.getTotalValue()` *before* `adjustTotalValue(...)` runs.

## Why a rejected order is a strict no-op

Requirement 4 ("rejected... does not affect the client's portfolio") is enforced structurally,
not by a rollback: the `else` branch simply never calls `holdingUpdater.applyOrder(...)` or
`portfolio.adjustTotalValue(...)` at all. There's no "undo" logic anywhere, because nothing ever
needs undoing — this is a direct consequence of validating *before* attempting to execute,
rather than executing optimistically and rolling back on failure.

## What this module demonstrates about the whole sprint

Every class this `OrderProcessingEngine` depends on was built, tested, and finished in a
different module, on a different day, often working from a completely different concrete
example (`Holding` from a `Trade`/`Instrument` demo in Module 2; `OrderValidator` from Module 3's
mission brief in Module 12). None of them needed to change to fit together here. That's not
luck — it's the direct, compounding result of Module 7's Single Responsibility (each class does
one thing) and Module 8's Dependency Inversion (each class depends on an interface or a value,
never on another concrete implementation detail) being applied consistently, module after
module, across the whole sprint.

## A question for Module 14

Now that the pieces are wired together and working, is there anything about this design you'd
change if you were starting over, knowing what you know now? Keep your answer for Module 14's
retrospective — it's asking exactly this.
