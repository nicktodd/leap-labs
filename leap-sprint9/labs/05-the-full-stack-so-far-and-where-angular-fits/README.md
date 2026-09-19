# Module 5 Lab — The Full Stack So Far & Where Angular Fits

## Objectives

By the end of this lab you will have:

- Traced a single request end to end through every layer of the mission stack, including
  the Angular app that doesn't exist yet
- Identified exactly which existing piece each future Angular module will build, and
  which parts of Modules 1-4's hand-written HTML/CSS/JS each one replaces

## Format

A 20-minute team whiteboard exercise. No code, no repo changes — a diagram (on paper, a
whiteboard, or a shared doc) is the deliverable.

## The Scenario

A trader opens `mission-ui` (the Angular app you'll spend the rest of this sprint
building), logs in, and submits an order. Modules 1-4 already built a rough version of
"logging in" by hand — a static HTML form, some CSS, and a `fetch()` call to
`sprint8-auth-service`. Today's demo proved every box past that point (the mission
service, Postgres) already works too, for real, against a real Postgres row.

## Task

With your team, sketch the request flow for two scenarios, this time with Angular as the
first box in the picture, not `curl`.

### Scenario A — Logging in through the UI

1. What does the trader type into the Angular app, and what does Angular send to
   `sprint8-auth-service`, and with what?
2. What comes back, and where in the Angular app does it get stored so later requests can
   use it?
3. What should the UI show the trader while that request is in flight, and if it fails?

### Scenario B — Submitting an order through the UI

1. What does the trader fill in on screen, and what does Angular send to the mission
   service's `/accounts/{id}/orders` — and how does the token from Scenario A get attached?
2. Which box checks the token's signature? Which box never sees the password, and which
   box never sees the raw SQL?
3. If the mission service returns `401` or `403`, what should the Angular app show the
   trader — and is "the API returned an error" ever an acceptable message to put on
   screen?
4. If the order succeeds, what changed in Postgres, and how does the trader find out
   their portfolio actually updated?

## Deliverable

A diagram with five boxes — Angular app, `sprint8-auth-service`, mission service,
Postgres, and the trader's browser session/token storage — arrows labelled with what's
actually sent at each hop, covering both scenarios. Next to each box, write which Sprint
9 module builds it (or "already built, Sprint N" for the three that aren't new).

## Acceptance criteria

- The diagram correctly shows Angular calling the auth service ONCE (login) and the
  mission service repeatedly (every subsequent request), not the other way round
- Every arrow into the mission service or auth service carries the token where the real
  demo's `curl` command did — no arrow "forgets" the `Authorization` header
- At least one failure state (invalid token, validation error, network failure) is shown
  with a specific, trader-facing UI response, not just "show an error"
- Each of the five boxes is labelled with the Sprint 9 module (or prior sprint) that owns
  it
