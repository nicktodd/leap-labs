# TDD Log — HoldingUpdater

Fill in one row per cycle, as you go — not from memory afterward.

| Cycle | Test written (red) | Minimal change to go green | Refactor notes (if any) |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 (refactor only) | — | — | |

## Reflection

- Did Cycle 4 pass immediately, or did it force a change? Either way, what does that tell you
  about how `HoldingUpdater` relates to `Holding`?
- `HoldingUpdater` and `Holding` both end up capable of rejecting an over-large sell. Is that
  duplication worth removing, or two classes correctly guarding their own boundary? Why?
- How did this compare to Module 10's `FeeBandClassifier` kata — easier, harder, or about the
  same discipline, applied to a slightly more realistic requirement?
