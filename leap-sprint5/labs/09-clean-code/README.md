# Module 9 Lab — Clean Code

## Objectives

By the end of this lab you will have:

- Refactored a working but messy class for readability, without changing its behaviour
- Used the clean code checklist to justify each change, not just "made it look nicer"
- Critically assessed a GitHub Copilot Chat-suggested refactor, rather than accepting it outright

## Setup

- Java 21 and Maven installed
- `mvn test` runs `OrderCategoriserTest` — these tests already pass against the given messy
  version, and must still pass, unchanged, after your refactor
- GitHub Copilot Chat, for Part 2

## Part 1 — Refactor by hand

`OrderCategoriser.java` works correctly, but is hard to read: single-letter names, a magic
number, one long method mixing counting, categorising, and formatting.

Refactor it, guided by `clean-code-checklist.md`. You should end up with:

- Meaningful names throughout
- The threshold (10000) as a named constant
- Separate, single-purpose methods instead of one long one
- No unnecessary comments — if you keep any, they should explain WHY, not WHAT

**Do not change `OrderCategoriserTest.java`.** If your refactor is behaviour-preserving, the
existing tests will still pass without any edits to them.

```bash
mvn test
```

## Part 2 — Critique a GenAI suggestion

Now that you've refactored it by hand, ask GitHub Copilot Chat to suggest its own refactor of
your **original, messy** `OrderCategoriser.java` (keep a copy, or check it out from git history —
don't ask Copilot to refactor your already-clean version, the exercise needs the messy starting
point). Try a prompt like "refactor this class for readability" or be more specific if you
prefer.

Fill in `refactor-critique-template.md`:

- What did it suggest that you'd keep?
- What did it suggest that you'd reject, and why?
- Did its version still pass `OrderCategoriserTest` unchanged?
- Is there anything it suggested that *looked* like an improvement but wasn't one?

This isn't about whether Copilot did a "good" or "bad" job — it's about practising the habit of
evaluating a suggestion against a checklist, the same way you'd evaluate a peer review comment
(Module 6) or a code review (Sprint 2, Module 4), rather than accepting confident-looking code
uncritically.

## Deliverable

- Your refactored `OrderCategoriser.java`, with `OrderCategoriserTest.java` still passing
  unchanged
- A completed `refactor-critique-template.md`

## Acceptance criteria

- `mvn test` passes with 0 failures and 0 errors, against your refactored class
- `OrderCategoriserTest.java` is byte-for-byte unmodified from the given version
- No single-letter variable names remain (other than a genuine loop index, if any survive)
- The `10000` threshold is a named constant
- `refactor-critique-template.md` has at least one kept change, one rejected (or modified) change,
  and an answer to "the one thing worth remembering"
