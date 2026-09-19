# Lab 17 — Mission Build: Wiring Up Remaining Features, UX Review & Sprint 9 Wrap-up

## Setup

Your own `mission-ui`, wherever you left it at the end of Module 16. Same running backends.

## Task

### Part 1: Find a real integration gap

Sixteen modules built `mission-ui` piece by piece, each verified on its own. Today's job is to
look at the whole app as a user would, not module by module, and find at least one place where
two pieces were each built correctly but don't actually agree with each other. To get started,
try this:

1. Log in, note the portfolio total and a holding's quantity on the Holdings screen.
2. Go to Place Order, submit a real order for a ticker you already hold (check
   `mission-service-openapi.json` or ask your trainer which tickers the backend recognises).
3. Go back to Holdings. Did the quantity or portfolio total change to reflect the order you
   just placed?

If it didn't, that's the gap: `MissionApi.submitOrder()` gets a real `OrderResponseDto` back
with a real `newHoldingQuantity`, but nothing does anything with it. Fix it - make a successful
order update the same `Holdings` service the Holdings screen and portfolio badge already read
from.

### Part 2: A UX polish pass

Pick at least one more real, small gap and fix it. Some candidates, if you want inspiration
rather than a free choice:

- No feedback while an order request is in flight - a user could double-click Submit Order on
  a slow connection.
- The generated `place-order` fields don't distinguish a required-and-empty ticker from one
  that's simply untouched clearly enough.
- Anything else you notice using the app yourself that a real user would find rough.

### Part 3: Verify nothing broke

1. `npx ng test --watch=false` - confirm all existing unit tests still pass.
2. `npx playwright test` - confirm the Module 16 login-journey suite still passes.
3. Manually re-run the Part 1 steps and confirm the fix actually holds - screenshot or note the
   before/after numbers, don't just assert it worked.

## A Question Worth Sitting With

Module 16's test suite was passing the whole time this gap existed. What does that tell you
about what a passing test suite does and doesn't guarantee about an application - and what
would it have taken (a new test, not a new feature) to have caught this gap automatically
before today?

## Sprint 9 Retrospective

In pairs or as a group, spend ten minutes on:

- What was the single most useful thing you learned this sprint - not the flashiest, the one
  you're most confident you'll actually reach for again?
- What's one thing about Angular, or about testing, or about wiring a front end to a real
  backend, that's still fuzzy? Say it out loud - if it's fuzzy for you, it's probably fuzzy for
  someone else in the room too.
