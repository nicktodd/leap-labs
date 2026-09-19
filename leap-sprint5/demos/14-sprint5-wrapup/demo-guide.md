# Demo: Module 14 — Sprint 5 Wrap-up, Design Rationale & Assessment Prep

**Duration:** 10 minutes
**Prerequisite:** none, this is a recap plus a modelled retrospective. No new tooling or commands.

## Part 1: Why this module has a retrospective, not just a checklist (2 min)

Narration: every other sprint wrap-up in this programme is a straight checklist. Sprint 5 gets
one extra thing first, because this sprint's whole arc was different — Module 3 asked you to
design something before you knew SOLID, clean code, or TDD; Module 13 asked you to actually build
it once you did. The gap between those two points is worth examining deliberately, not just
noted in passing.

## Part 2: Model the design rationale exercise (5 min)

Walk through `solutions/14-sprint5-wrapup/model-design-rationale.md` live — pick one decision
from it and narrate the full arc:

```text
"Module 3's worksheet said Confirmation could go either way — a status field on Order,
 or its own class. We picked the status field, for YAGNI reasons.

 Module 4's class diagram kept it as a status field — nothing changed yet, because
 nothing had tested that decision yet.

 Module 13's actual build: still a status field, unchanged. This decision genuinely
 survived the whole sprint. But we CAN now say why with more confidence than we could
 in Module 3 - the mission never grew a second, independent reason to track a
 confirmation's lifecycle, so the simpler option kept being the right one all the way
 through."
```

Narration: notice this is a decision that *didn't* change — that's just as worth recording as one
that did. A design rationale isn't a list of mistakes; it's an honest account of what held up and
what didn't, and why.

Contrast with a decision that *did* change: `OrderManager` in Module 6's `flawed-design.mmd` was
a deliberately bad example, but ask the group — does anyone's own Module 4 diagram have a class
that quietly grew too many responsibilities before peer review caught it? That's the real version
of this exercise.

## Part 3: Model a peer-check (2 min)

Pick a volunteer pair. Run through a few checklist items live:

```text
"Show me your Module 4 class diagram — point to one aggregation and one composition edge,
 and tell me why each is the one it is, not the other."
"Show me a sequence diagram with an alt fragment — what's the condition?"
"Run mvn test on your Module 13 solution, live."
"Name a class in your mission build that came from an earlier module completely unchanged."
```

## Part 4: Naming this sprint's throughline (1 min)

Narration: Sprint 5 didn't teach you a single tool the way Docker or Jenkins did in Sprint 1. It
taught you a *sequence*: design something, get it reviewed, learn the vocabulary to name what's
wrong with it (SOLID), learn the discipline to build it correctly the first time (TDD), and then
actually build it. Nothing in Modules 7-13 works without Module 3's requirement or Module 4's
diagram underneath it — and nothing in Modules 3-6 would have mattered if Module 13 never
actually got built. That whole chain, not any single module, is what Friday's assessment is
really checking.

## Key message

This module has two jobs, not one: make the sprint's design evolution genuinely visible (not
just implied), and catch any remaining gaps while there's still time to close them.
