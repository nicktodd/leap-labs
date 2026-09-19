# Module 10 Lab — TDD Fundamentals

## Objectives

By the end of this lab you will have:

- Built a class entirely test-first, following red-green-refactor for every single addition
- Practised writing the smallest implementation that makes a failing test pass, resisting the
  urge to write more than the current test demands
- Kept a log of your cycles, to make the discipline visible to yourself afterward

## Setup

- Java 21 and Maven installed
- `FeeBandClassifier.java` and `FeeBandClassifierTest.java` both start essentially empty —
  you write both, incrementally, together
- `tdd-log-template.md`, for recording each cycle as you go (don't skip this — filling it in
  *after* the fact from memory defeats the point)

## The Business Rule

`FeeBandClassifier.classify(double tradeValue)` returns one of three bands:

- `"STANDARD"` — trade value below $5,000
- `"PREMIUM"` — trade value from $5,000 up to (but not including) $50,000
- `"INSTITUTIONAL"` — trade value $50,000 or more

**Do not implement this from the spec above in one go.** The point of the exercise is the
sequence below — follow it in order, one cycle at a time.

## The Sequence

For each step: write the ONE test described, run it and confirm it fails (red), write the
smallest code that makes it pass (green), then refactor only if there's something worth
cleaning up. Log each cycle in `tdd-log-template.md` before moving to the next step.

1. **Red:** `classify(1000)` returns `"STANDARD"`.
   **Green:** the smallest possible implementation — yes, that probably means returning
   `"STANDARD"` unconditionally. That's correct at this stage, not a shortcut you're getting
   away with.

2. **Red:** `classify(60000)` returns `"INSTITUTIONAL"`.
   **Green:** now you're forced to write a real conditional.

3. **Red:** `classify(10000)` returns `"PREMIUM"`.
   **Green:** the middle band.

4. **Red:** `classify(5000)` returns `"PREMIUM"` (the lower boundary is inclusive).
   **Green:** fix the boundary condition if your current comparison gets this wrong.

5. **Red:** `classify(50000)` returns `"INSTITUTIONAL"` (the lower boundary is inclusive here
   too).
   **Green:** fix this boundary condition too.

6. **Refactor:** by now you likely have two bare numbers (5000 and 50000) sitting in
   conditionals. Extract them as named constants — this is Module 9's checklist, still applying.

## A Rule to Actually Follow, Not Just Read

If you catch yourself writing implementation code that isn't required by any test you've
written yet — stop, and write the test for it first. This will feel unnatural at first,
especially at Step 1 when "just returning STANDARD" feels like cheating. It isn't — the next
test is what earns the next piece of real logic.

## Deliverable

- `FeeBandClassifier.java` and `FeeBandClassifierTest.java`, both fully built
- A completed `tdd-log-template.md`, one entry per cycle

## Acceptance criteria

- `mvn test` passes with 0 failures and 0 errors
- At least 5 tests exist, matching the 5 red-green steps above (boundary cases included)
- The two thresholds are named constants, not bare numbers, in the final implementation
- The TDD log has one entry per cycle, each naming the test, the minimal implementation change,
  and (where applicable) what was refactored
