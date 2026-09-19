# Sprint 9 — Project Friday Guidance

## Context

This week's teaching covers HTML, CSS, JavaScript in the browser, fetch/HTTP, Angular
fundamentals, project structure and tooling, components, services and dependency injection, HTTP
communication, connecting to the Spring Boot backend, OpenAPI-generated clients, reactive forms,
routing, authenticated flows and testing with Playwright.

This week's deliverable is the trading UI: sign-in, a dashboard, an order ticket and an order
history, wired up to your own real backend from Sprints 6 and 8, not a mock. BR-10, BR-11 and
BR-13 are what it has to show, and section 6's Joanna persona, not a trading professional, is
who it has to work for.

## The trap to avoid

- BR-06/BR-07 already established that accepting an order and executing it are separate steps.
  The response your UI gets back from placing an order is not the final outcome. What does your
  interface do with an order that's been accepted but not yet resolved, render it as if
  something's broken, or as genuinely still working? Section 9.2 needs a client who never
  wonders whether their action registered, how does your design deliver that?
- Client-side validation isn't enforcement. The rules you built into your Sprint 5 and Sprint 6
  services still have to hold regardless of what this form does. Treat validation here as
  helping Joanna avoid an easy mistake, per section 9.5, not as a second place the business
  rules live.
- Every error your backend can return has to reach the screen as something Joanna can act on,
  not raw or internal text. Branch on whatever error codes your own services define, and decide
  what a non-technical user needs to be told for each one.
- A session token belongs only with your own services. If anything in this UI calls a
  third-party API directly, from the browser, a market data source or anything else, that's
  worth a second look: should that call be happening here at all, or somewhere server-side that
  can hold the credential instead?
- Nothing secret belongs in a browser bundle, no API key, no signing secret, nothing you'd mind
  a user reading in dev tools, because they can.

## Suggested Friday session

- Walk your screens as a team against the requirements spec and the customer meeting from
  Sprint 2, does what you're building actually show what the customer said they needed, and
  would Joanna manage it without help?
- Agree the component and state boundaries before building spreads across the team, so the
  login, dashboard, order ticket and blotter don't each reinvent how they talk to the backend.
- Decide how you're generating or writing your API calls against your own Sprint 6 and Sprint 8
  contracts, and keep it consistent across the team.
- Work through the questions above and agree your answers.
- Plan your test coverage: what's a unit test, what needs Playwright, and who owns which.
- This is the first sprint with something a non-technical person can actually use rather than
  read about. Show it to your customer instructor before Friday's over, place an order in front
  of them if you can, and bring back what they made of it, not just whether it worked.
- This is the last sprint before the applied project week, refine the backlog with that in
  mind, what has to be true of the platform end to end before Sprint 10's gap-closing can start
  from a solid base rather than a shaky one?

## What to present to the class

- A demo of the UI against the real backend, not a mock.
- What your customer instructor thought when they saw it, praise, confusion or otherwise.
- How you're handling an order that's accepted but not yet resolved.
- Your test coverage and what it does and doesn't catch.
- An updated backlog, and what you're carrying into the applied project week.
