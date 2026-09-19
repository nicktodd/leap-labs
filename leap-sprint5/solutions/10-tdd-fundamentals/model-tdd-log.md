# Model TDD Log — FeeBandClassifier

| Cycle | Test written (red) | Minimal change to go green | Refactor notes |
|---|---|---|---|
| 1 | `classify(1000)` returns `"STANDARD"` | `return "STANDARD";` unconditionally | — |
| 2 | `classify(60000)` returns `"INSTITUTIONAL"` | `if (tradeValue >= 50000) return "INSTITUTIONAL"; return "STANDARD";` | — |
| 3 | `classify(10000)` returns `"PREMIUM"` | Added a middle branch: `if (tradeValue >= 5000) return "PREMIUM";` | — |
| 4 | `classify(5000)` returns `"PREMIUM"` | Already passed — `>=` was used from the start in Cycle 3, so no change needed | Noted in the log anyway: worth checking a boundary even when you suspect it'll already pass, because sometimes it doesn't |
| 5 | `classify(50000)` returns `"INSTITUTIONAL"` | Already passed too, for the same reason | — |
| 6 (refactor only) | — | — | Extracted `PREMIUM_THRESHOLD = 5000` and `INSTITUTIONAL_THRESHOLD = 50000` as named constants |

## Reflection

**Was there a point where you wanted to write more implementation than the current test
demanded?** Yes — after Cycle 2, it was tempting to add the `PREMIUM` branch immediately, since
it's "obviously" needed from the spec. Resisting this and waiting for Cycle 3's test is the
actual discipline being practised — the temptation doesn't go away, it just gets easier to
notice and set aside.

**Did any test surprise you by failing for a different reason than you expected?** In this
particular kata, no — but that's exactly why Cycles 4 and 5 are included even though they "should
obviously pass." If the implementation had used `>` instead of `>=` from the start, exactly one
of these two boundary tests would have failed, and it would have failed at a point where the
mistake is trivial to spot and fix (one line) rather than several cycles later when the
implementation is more tangled.

**What would you do differently building this again?** Nothing structural — this kata is small
enough that the sequence given is close to optimal. On a larger piece of behaviour, the lesson
generalises: pick the next test based on "what's the smallest additional fact I can force the
implementation to handle," not "what's next on the requirements list."

## Why boundary tests matter, even when "they'll obviously pass"

This is worth calling out explicitly, since Cycles 4 and 5 above didn't actually change any code.
A boundary test that passes without forcing a change isn't wasted — it's evidence. Writing
`classify(5000)` and watching it pass *confirms* the `>=` decision was made correctly back in
Cycle 3, rather than assuming it. If a teammate's PR later "simplifies" the condition to `>`
without running the tests, this is exactly the test that catches it.
