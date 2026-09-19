# Design Review Checklist

Use this checklist when reviewing a partner's Module 3-5 artefacts (worksheet, class diagram,
sequence diagram). Not every item applies to every design — use judgement — but check all of them
before deciding approve vs. request changes.

## Responsibility and cohesion (preview of Module 7-8's SOLID)

- [ ] Does any one class do noticeably more than the others — validation, execution, reporting,
      and notification all in one place?
- [ ] Could you describe each class's job in a single sentence, without using "and"?
- [ ] Is there a class that exists just to hold data, with no behaviour, when it should have some
      (or vice versa — a class with behaviour that should really be state)?

## Encapsulation (recap of Module 2)

- [ ] Are fields private, with access through methods, or are they exposed as public data?
- [ ] Is there anywhere state could become invalid because nothing is checking it?

## Reuse of existing work

- [ ] Does the design reuse `Instrument`/`Feeable` (Modules 1-2) for fee calculation, or does it
      reinvent that logic somewhere new?
- [ ] Is there a class in this design that duplicates something the mission brief already gives a
      name to?

## Relationships (recap of Module 4)

- [ ] Is every association actually a permanent reference, or should some be dependencies?
- [ ] Is every "has a" correctly aggregation or composition, not just drawn as a plain association?
- [ ] Does inheritance appear anywhere it isn't clearly justified by an "is a kind of" relationship?

## Behaviour (recap of Module 5)

- [ ] Does the sequence diagram's happy path match the class diagram's relationships — no message
      sent to a class that has no association with the sender?
- [ ] Is the validation/rejection branch (or an equivalent conditional path) actually modelled with
      `alt`, or just implied?

## Traceability back to requirements

- [ ] Does every class and responsibility trace back to something in `shared/mission-brief.md`?
- [ ] Is there anything in the mission brief's requirements that doesn't appear anywhere in the
      design?

## Leaving your review

- Leave at least **two written comments**, each specific enough that the author knows exactly
  what to change and why — "this class does too much" is a start, but "OrderManager validates,
  executes, reports, and sends email — consider splitting validation and reporting into their own
  classes" is a review comment
- Finish with either an **Approve** or a **Request Changes**, not silence
