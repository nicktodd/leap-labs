# Model Answers — Clean Code

## Part 1: notes on the refactor

`OrderCategoriser.java` (in this solution folder) shows one defensible refactor. A few choices
worth explaining:

- **`CategoryCounts` as a small private static class**, rather than three separate `int`
  parameters passed around or returned as an array/`Map<String, Integer>`. Passing three named
  fields on one object is more self-documenting than three positional `int`s, and safer than a
  `Map` keyed by string (no risk of a typo'd key). This is a small, deliberately unexported type —
  it exists only to make `countByInstrumentType`'s return type readable, not as a reusable
  abstraction.
- **`averageFee` guards the empty-list case with an early return**, rather than the original's
  `if (o.size() == 0) { avg = 0; } else { avg = t / o.size(); }`. Both are correct; the guard
  clause reads as "handle the edge case, then do the normal thing" rather than "here are two
  branches of equal weight."
- **No comments in the final version, except one explaining *why* `CategoryCounts` exists** (an
  intentional design choice a reader might otherwise question) — nothing explaining *what* each
  method does, because the method names already say that.

## Part 2: what a good Copilot critique looks like

There's no single correct critique — it depends on what Copilot actually suggests, which varies
run to run. But a strong critique, regardless of the specific suggestion, will:

- **Distinguish stylistic preference from an actual improvement.** Copilot might suggest renaming
  `CategoryCounts` to something else, or using a `record` instead of a class (a genuine, defensible
  Java 21 alternative) — neither is "wrong," and a good critique says so rather than reflexively
  accepting or rejecting.
- **Catch anything that changes behaviour**, even subtly. A common failure mode: Copilot
  "simplifying" the average calculation in a way that changes rounding, or handling the empty-list
  case differently. Running `mvn test` against its suggestion is the check that catches this — not
  reading the code and deciding it "looks fine."
- **Notice when a suggestion adds complexity in the name of "best practice"** — e.g., introducing
  a `Comparator` or a `Stream` pipeline that's genuinely harder to read than the loop it replaced,
  even though it "looks more modern." Clean code is about the reader, not about using the newest
  language feature available.

## A question worth carrying into Module 10-11

TDD (Module 11) will ask you to write tests *before* the implementation. Notice something about
today's exercise: `OrderCategoriserTest` already existed, and its role was entirely to *protect*
behaviour during a refactor, not to *drive* new behaviour. Both are legitimate uses of a test
suite — Module 11 introduces the second one.
