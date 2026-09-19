# Module 14 Lab — Sprint 5 Wrap-up, Design Rationale & Assessment Prep

## Objectives

By the end of this lab you will have:

- Written a design rationale comparing your Module 3-4 first-draft design to what you actually
  built in Module 13, and explained what changed and why
- Worked through an assessment checklist covering Modules 1-13
- Peer-checked a partner's understanding and repo against that checklist
- Identified and closed any remaining gaps before the sprint assessment

## Setup

- Everything from Modules 01-13, nothing new
- Your Module 3 worksheet, Module 4 `mission-model.mmd`, and Module 13 mission build
- A partner, ideally not someone you paired with for Module 13
- `design-rationale-template.md` from this lab

## Part 1 — Design Rationale

This is the sprint's own retrospective, not a generic one. Compare three points in time:

1. **Module 3**: your first-draft worksheet — candidate entities, responsibilities, relationships
2. **Module 4**: your class diagram — the same design, made precise
3. **Module 13**: what you actually built

For at least **three** specific decisions, answer: did this survive unchanged, get revised, or
get dropped entirely — and what caused the change? Name the module responsible each time (a
peer-review comment from Module 6, a SOLID violation caught in Module 7-8, a requirement that
turned out to mean something different once you tried to test it in Module 12, and so on).

Use `design-rationale-template.md` to structure your answer.

## Part 2 — Assessment Checklist

Work through this with your partner. For each item, *show* the thing — a real file, a real test
run, a real diagram — not just describe it from memory.

### Java & OOP Foundations (Modules 1-2)

- [ ] Can explain one Java concept by directly comparing it to its Python equivalent
- [ ] Can show a class with a genuinely private field protecting a real invariant (not "private
      out of habit")
- [ ] Can explain, with a real example, when composition was chosen over inheritance, and why

### Design: OOAD & UML (Modules 3-6)

- [ ] Can show a real Module 3 worksheet with at least 8 candidate entities and reasoning
- [ ] Can show a Module 4 class diagram using all five relationship types correctly (association,
      aggregation, composition, inheritance, implements)
- [ ] Can show a Module 5 sequence diagram with an `alt` fragment for a genuinely conditional path
- [ ] Can show at least two specific, actionable review comments left on a partner's Module 4-5
      design in Module 6

### SOLID & Clean Code (Modules 7-9)

- [ ] Can name all five SOLID principles and give a one-sentence definition of each, unprompted
- [ ] Can point to a real class in their own code and say which SOLID principle it satisfies, and how
- [ ] Can show a before/after refactor from Module 9, and explain what checklist item each change addressed

### TDD, JUnit & Mocking (Modules 10-12)

- [ ] Can explain red-green-refactor without notes, in their own words
- [ ] Can show a TDD log with at least 4 real cycles from Module 10 or 12
- [ ] Can name three JUnit features beyond @Test and assertEquals, and what each is for
- [ ] Can explain, in one sentence, why testing in isolation matters, and when a mock is (and
      isn't) the right tool

### Mission Build (Module 13)

- [ ] Can run `mvn test` on their Module 13 solution and show it passing
- [ ] Can point to one class in the mission build that was reused, completely unchanged, from an
      earlier module, and explain why that was possible
- [ ] Can explain, concretely, how a rejected order is guaranteed to leave the portfolio unchanged

## Task Sheet

1. Complete Part 1 (design rationale) individually first — this needs your own honest reflection,
   not a partner's opinion.
2. Pair up and work through Part 2's checklist together, partner by partner.
3. Write down specific gaps, not vague ones ("couldn't show a real alt fragment," not "UML stuff").
4. Use remaining time to close your own gaps.

## Acceptance criteria

- A completed `design-rationale-template.md`, with at least three specific decisions traced
  across Modules 3, 4, and 13
- Every checklist item has been shown, not just claimed, to a partner
- A specific, written list of any remaining gaps, each with a plan to close it before assessment
