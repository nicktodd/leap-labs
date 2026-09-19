# Module 6 Demo Guide — Peer Review

A live, instructor-led review of a deliberately flawed design (`flawed-design.mmd`), using
`labs/06-peer-review/review-checklist.md`. The point isn't to find every flaw — it's to model
*how* to phrase a review comment so it's useful to the person receiving it.

## The Flawed Design

`OrderManager` does validation, execution, reporting, *and* sends email — and every field is
public. It doesn't reuse `Instrument`/`Feeable` from Modules 1-2 at all; fee calculation is
buried inside `calculateFee(order)` as one more method on the same class.

## Live Walkthrough

Go through the checklist section by section, and for each hit, **say the bad version out loud
first, then the good version**, so the contrast is explicit:

1. **Responsibility and cohesion** — "This is broken" is the bad version. "`OrderManager` has six
   public methods spanning five different responsibilities — validation, execution, holding
   updates, reporting, and notification. Consider splitting it into `OrderValidator`,
   `OrderExecutor`, and a separate reporting/notification path" is the useful version.

2. **Encapsulation** — every field on both classes is public. Ask: "what stops `orders` being
   mutated from anywhere in the codebase, with no validation at all?" Tie this back to Module 2's
   `Holding` — the fix is the same pattern, applied here.

3. **Reuse of existing work** — `calculateFee(order)` on `OrderManager` duplicates what
   `Instrument`/`Feeable` already do. This is worth a comment on its own: reinventing existing,
   tested logic is a specific, nameable problem, not just "messy design."

4. **Traceability** — `sendEmail(client)` doesn't trace to anything in `shared/mission-brief.md`.
   Ask the group: is this a hidden requirement someone remembered from a real system, or was it
   invented? Either way, it's worth a comment — an untraceable requirement is exactly the kind of
   thing that quietly expands scope.

## Modelling How to Receive a Review Comment

Pick one comment from the list above and role-play the response, live:

- **Defensive (what not to do):** "No, that's fine, it's only a training exercise."
- **Constructive:** "Good catch — I put fee calculation there because I hadn't connected it back
  to `Feeable` yet. I'll move it to reuse `Instrument.calculateFee()` instead."

## Points to Make Explicitly

- **A review comment without a suggested direction is just criticism.** "This class does too
  much" tells the author there's a problem; "consider splitting validation into its own class"
  tells them what to do about it.
- **Approve/Request Changes is a real decision, not a formality.** For a design with this many
  issues, "Request Changes" is the right call — approving it anyway to be polite defeats the
  point of review.
- **The goal is a better design, not a perfect first draft.** Nobody's Module 3-5 work should
  look like `flawed-design.mmd` by this point — but everybody's has *something* worth a comment.

## Transition to the Lab

Learners now swap their own Module 4 (class diagram) and Module 5 (sequence diagram) with a
partner and review each other's, using the same checklist.
