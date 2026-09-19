# Module 14 Lab — Instructor Notes

No solution in the usual sense for Part 2 — it's a checklist. Part 1 (design rationale) has a
model answer at `model-design-rationale.md`. Notes on what good looks like and common gaps for
both.

## What good looks like — Design Rationale (Part 1)

- A strong rationale names **specific classes and modules**, not vague impressions ("things
  changed a bit because of SOLID"). If a delegate can't point to a specific Module 6 comment, a
  specific Module 7 kata, or a specific line in their Module 13 code, the reflection is too
  shallow to be useful.
- **At least one decision that *didn't* change is worth as much credit as one that did.**
  Delegates sometimes assume the exercise wants "here's everything I got wrong" — redirect them:
  a decision that survived three checkpoints unchanged (worksheet, diagram, real build) is
  genuinely informative too.
- Watch for rationales that only mention Module 13 changes without tracing back to *why* —
  "we changed it because it made more sense" isn't a rationale, it's a restatement. Push for the
  specific trigger (a test that failed, a peer review comment, a SOLID violation spotted).

## What good looks like — Assessment Checklist (Part 2)

- **Java & OOP**: a delegate who can point to a real private field protecting a real invariant
  (not just "I made it private") has actually internalised Module 2's `Holding` lesson, not just
  memorised the syntax.
- **OOAD & UML**: the aggregation-vs-composition question is the best diagnostic here — if a
  delegate can't explain *why* one edge in their own diagram is one and not the other, that's a
  Module 4 gap worth a two-minute refresher, not a pass.
- **SOLID & Clean Code**: "name all five" is table stakes; the harder, more useful check is
  pointing to a real class and explaining *which* principle it satisfies and *how*. Recitation
  without application is a common false positive here.
- **TDD, JUnit & Mocking**: the isolation question ("why does testing matter, and when is/isn't a
  mock the right tool") is the one delegates most often answer with a memorised definition rather
  than genuine understanding — ask a follow-up ("would you mock `Holding` in a test of itself?
  why not?") to check.
- **Mission Build**: "point to a class reused unchanged from an earlier module" is the single
  best signal that the whole sprint actually connected for this delegate, rather than each module
  being learned in isolation.

## Common gaps and quick fixes

| Gap | Likely cause | Quick fix |
|---|---|---|
| Design rationale only lists Module 13 changes, no "why" | Reflection done too quickly, right before the deadline | Ask them to open their actual Module 6 review comments and find the one that matches |
| Can't distinguish aggregation from composition in their own diagram | Module 4 checklist applied mechanically rather than understood | Re-ask with the "does the part outlive the whole" question, on their own classes |
| Can name SOLID principles but can't apply them to their own code | Passive exposure (slides) rather than active application | Have them find one class in their Module 13 build and name its single responsibility, out loud |
| Vague answer on isolation/mocking | Module 11's Mockito section covered a lot of ground quickly | Walk through one `verify()` example from the Module 11 demo again, live |
| No class reused unchanged across modules | Genuinely possible if their design diverged a lot by Module 13 — not automatically a problem | Discuss it as its own data point for their design rationale, not just a checklist failure |

## Running the session

Twenty to twenty-five minutes: ten for the design rationale (best done individually, quietly,
before any pairing), the rest for the checklist walkthrough and closing gaps. This module runs
longer than other sprints' wrap-ups because of Part 1 — don't compress it to fit the usual
fifteen-minute slot.
