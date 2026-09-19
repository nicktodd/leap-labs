# Model Answer — Order Processing Sequence

`mission-order-sequence.mmd` (rendered as `mission-order-sequence.png`) is **a** defensible
sequencing, not **the** correct one — bring differences to Module 6's peer review.

## Design decisions worth explaining

- **`OrderValidator` asks `Portfolio` for current holdings, not `Client` directly.** The Module 3
  worksheet put risk-limit and holdings checks on the validator; `Portfolio` is where holding data
  actually lives (Module 4's composition relationship), so the validator has to ask it.
- **The `alt` fragment wraps everything from the validation result onward, not just the
  execution step.** Both branches need to reach `SettlementReport` — an accepted order reports a
  fee, a rejected one reports a reason. Putting the report call *inside* each branch (rather than
  after the `alt`, shared) makes that difference explicit in the diagram.
- **`OrderExecutor` stays activated for the whole execution branch**, including its calls to
  `Instrument` and `Portfolio` — this is deliberate, not an oversight: execution genuinely is one
  coordinated unit of work, unlike, say, `Order` itself, which is mostly a passive data holder that
  gets asked things rather than doing them.
- **What's deliberately left out**: retry logic, concurrent order handling, and how the "day's
  batch" is loaded in the first place. This diagram is scoped to one order, start to finish — the
  batch-level orchestration is a different (and, for this sprint, unnecessary) diagram.

## Common mistakes to watch for when comparing against your own

- Forgetting the `alt`'s rejected branch still needs to reach `SettlementReport` (Module 3's
  requirement 4: "rejected orders still appear in the settlement report")
- Activating `Portfolio` but never deactivating it (or vice versa) — `mmdc` will refuse to render
  this, which is a useful forcing function, not just an annoyance
- Showing `Client` receiving intermediate messages during validation/execution — in this design,
  `Client` only appears at the very start (submits) and very end (gets a confirmation); everything
  in between is between the other objects
