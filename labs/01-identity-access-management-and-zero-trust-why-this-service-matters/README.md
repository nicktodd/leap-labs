# Module 1 Lab — Identity, Access Management & Zero-Trust: Why This Service Matters

## Objectives

By the end of this lab you will have:

- Sketched a complete request flow from a client, through a real auth service, to a protected
  mission-service route
- Named, specifically, which parts of that flow are authentication and which are authorization

## Format

A 15-minute paired whiteboard exercise. No code, no repo changes — a diagram (on paper, a
whiteboard, or a shared doc) is the deliverable.

## The Scenario

A trader wants to submit an order through the mission service. The mission service's
`/accounts/{id}/orders` endpoint is protected — Sprint 6's `SecurityConfig` rejects any request
without a valid JWT.

By Module 15, `sprint8-auth-service` (real registration, real password hashing, real Postgres
lookups) will replace `shared/auth-stub` as the thing that issues that JWT.

## Task

With a partner, sketch the request flow for two scenarios:

### Scenario A — First-time login

1. What does the trader's client send to the auth service, and with what?
2. What does the auth service need to check before it issues anything?
3. What, specifically, is inside the token the auth service returns?
4. What does the client do with that token next?

### Scenario B — Using the token

1. What does the client send to the mission service, and how does it attach the token?
2. What does the mission service check about the token — and just as importantly, what does it
   **not** need to do (hint: does it call the auth service at this point)?
3. If the token is invalid or missing, what should happen — and does that match what you saw in
   the demo's `401` result?
4. If the token is valid but the trader's role is `GUEST`, not `MISSION_OPERATOR` — should the
   request succeed? Where in the flow would that decision get made?

## Deliverable

A diagram (client, auth service, mission service, Postgres, as boxes; arrows labelled with what's
actually sent) covering both scenarios, plus one sentence per box explaining what that component
is responsible for **and explicitly not** responsible for.

## Acceptance criteria

- Authentication (proving identity) and authorization (checking role/permission) are labelled as
  distinct steps, not conflated into one "login checks everything" box
- The diagram correctly shows the mission service NOT calling the auth service at request time —
  if your diagram has that arrow, be ready to explain why it's there, or remove it
- Both failure cases from Scenario B (no token, wrong role) are shown, not just the happy path
