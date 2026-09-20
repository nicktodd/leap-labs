# Sprint 5 - Project Friday Guidance

## Context

This week's teaching covers core Java, OO principles, OOAD, UML class and sequence diagrams,
SOLID, clean code, TDD and JUnit.

This week's deliverable is the trading domain in Java: the entities, rules and lifecycle that
decide whether an order is accepted. You modelled this same domain as tables in Sprint 3. This
week it's objects, and the two aren't quite the same exercise, a table stores state, an object
owns the behaviour that changes it.

## The trap to avoid

A week of UML and OOAD makes it tempting to design the class diagram that looks right on a
whiteboard, then move on. Before you do, put it under some pressure from what you already know
about this platform, not a hint about what's coming, just what you've already committed to:

- One of the programme's own objectives is that the firm can extend this platform later without
  rebuilding what came before. Other parts of your own system, over the coming sprints, are
  going to need to ask "is this order allowed?" How does your design hold up if something other
  than what you're building this week needs to ask that same question? Does answering it require
  a database, a framework, or a specific way of being called, or could it, in principle, be
  answered in isolation?
- BR-05 and BR-06 need an answer here, not just a passing mention: what sequence of checks
  does "checked against the firm's trading rules" actually resolve to, and what does "recorded as
  a commitment before execution" imply about the states an order can be in? Decide the lifecycle
  deliberately, which states exist and which are genuinely terminal, rather than letting it fall
  out of whatever code gets written first.
- How are you representing monetary values? It's worth actually testing what happens to a balance
  across many small operations with whatever type you've chosen, rather than assuming it'll be
  fine.

None of this has one right answer. What matters is that the decision was made on purpose and your
team can explain why, not that you land on any particular structure.

## Suggested Friday session

- Walk a candidate class diagram as a team before anyone writes code. Every member should be
  able to explain why a class exists and where a rule lives, not just the person who drew it.
- Pressure-test it against SOLID: where would a new instrument type or a new order rule force a
  change, and is that change contained or does it ripple?
- Work through the questions above as a team and agree your answers before coding.
- Agree your TDD approach for the week, tests first, and who's pairing with whom.
- Refine the backlog against the domain model you now have, does anything in it need rewording
  now that the rules are concrete?

## What to present to the class

- A walkthrough of your class diagram and the buy/sell rules it encodes.
- The reasoning behind how coupled or independent your rules are from any one caller, and how
  you're representing money, and why.
- A SOLID decision you made deliberately, and what you'd do differently under a different
  requirement.
- An updated backlog.
