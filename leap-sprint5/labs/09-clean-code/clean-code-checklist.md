# Clean Code Checklist

Use this while refactoring `OrderCategoriser.java`, and again when critiquing whatever GitHub
Copilot Chat suggests.

## Naming

- [ ] Does every variable name say what it holds, without needing a comment to explain it?
- [ ] Does every method name say what it does, as a verb phrase?
- [ ] Are there any single-letter names left, other than a genuine loop index?

## Function size and single level of abstraction

- [ ] Does each method do one job? Could you describe it in one sentence without "and"?
- [ ] Does each method operate at one level of detail — not mixing "loop through raw data" with
      "format a user-facing string" in the same block?
- [ ] Is there a method doing three or more genuinely different things in sequence?

## Magic numbers and duplication

- [ ] Are literal numbers (other than 0, 1, or an obviously self-explanatory value) given a
      named constant?
- [ ] Is there any logic duplicated in more than one place that could be extracted once?

## Control flow

- [ ] Is there nesting that could be flattened with an early return or a guard clause?
- [ ] Are `if`/`else if`/`else` chains doing one clear job each, or has one grown to handle
      several unrelated cases?

## Comments

- [ ] Does every remaining comment explain WHY (a non-obvious reason), not WHAT (which the code
      already says)?
- [ ] Is there a comment that exists only because the code below it isn't clear enough to stand
      on its own — and would a rename or extraction remove the need for the comment entirely?

## Behaviour preservation

- [ ] Do `OrderCategoriserTest`'s tests still pass, unchanged?
- [ ] Would you be confident handing this class to a teammate who has never seen the original
      messy version, with no explanation needed?
