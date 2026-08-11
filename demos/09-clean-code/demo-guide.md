# Module 9 Demo Guide — Clean Code

Run `CleanCodeDemo.java` first, then walk through the two classes side by side.

```bash
mvn package
java -cp target/classes com.neueda.leap.sprint5.CleanCodeDemo
```

## The Point: Identical Output, Very Different Readability

Put `MessySettlementSummary.s()` and `SettlementSummary.summarize()` on screen together. The
output is byte-for-byte identical — this is important to say explicitly: **clean code isn't
about correctness, it's entirely about how cheap the code is to read, change, and trust later.**

## Walk the Checklist Against the Messy Version

Go through `clean-code-checklist.md` against `MessySettlementSummary` live:

- **Naming**: `s`, `o`, `x`, `n1`, `n2`, `od`, `f`, `r` — none of them say what they hold. Ask the
  group to guess what `n1` and `n2` mean *before* revealing the answer (large/small order
  counts) — the fact that nobody can guess correctly is the point.
- **Magic number**: `10000` appears with zero explanation. Ask: is this a business rule that
  might need to change? (Yes — it's exactly the kind of threshold that ends up needing a config
  value eventually. A named constant is step one toward that.)
- **One long method, several jobs**: counting, categorising by size, and formatting a string are
  three different responsibilities, all inline in one method — this is Module 7's SRP, showing up
  again at the method level, not just the class level.
- **The comment**: `// loop through the orders and add up fees and counts` describes WHAT the
  next few lines do — which the code already shows. A useful comment would explain something the
  code *can't* show, like why 10000 is the threshold. There isn't one here, because there's no
  non-obvious reason — which is itself worth noticing: not every method needs a comment.

## Show the Refactor Landing, Piece by Piece

In `SettlementSummary`, point out each fix lands on a specific checklist item:

- `LARGE_ORDER_THRESHOLD` — the magic number now has a name and exactly one place to change
- `totalFees()`, `countByCategory()`, `format()` — each does one job, nameable in one sentence
- No comments at all — none were needed once the names and structure carried the meaning

## Points to Make Explicitly

- **This was a pure refactor — no new behaviour, no bug fixes.** That's deliberate: it isolates
  "harder to read" from "does something different," so the group can evaluate readability without
  the distraction of correctness changes.
- **Clean code and SOLID overlap, but aren't the same thing.** `SettlementSummary`'s three
  extracted methods are *also* small steps toward SRP, but the lesson here is about readability at
  the statement/method level, not the class-level responsibility split from Module 7.

## Transition to the Lab

Learners refactor `OrderCategoriser.java` by hand first (Part 1), then — separately — ask GitHub
Copilot Chat to refactor the same original messy class and critically assess its suggestions
against the same checklist (Part 2). The order matters: doing it by hand first means they have
their own informed opinion before seeing what Copilot proposes, rather than anchoring on its
suggestion.
