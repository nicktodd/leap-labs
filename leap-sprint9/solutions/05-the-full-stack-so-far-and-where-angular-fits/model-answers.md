# Module 5 — Model Answers

There's no code for this module — this is what a strong whiteboard sketch should
contain. Modules 1-4 already built a rough, hand-written version of Scenario A (a
static HTML form, styled, wired up with a manual `fetch()` call) — this sketch is
about what changes once Angular replaces that by-hand version.

## Scenario A — Logging in through the UI

1. **Angular sends**: the username and password the trader typed into a login form
   (Module 13), as a `POST` to `sprint8-auth-service`'s `/auth/login` — the exact same
   request body Module 4's `fetch()` call sent, and today's demo sent again with
   `curl`.
2. **Comes back and is stored**: `{ accessToken, refreshToken }`. The Angular service
   layer (Module 9) holds the access token in memory (a signal or a service field, not
   `localStorage` by default — worth a brief tangent on XSS risk if a pair proposes
   `localStorage`), so a JWT interceptor (Module 15) can attach it to every later
   request without every component needing to know it exists.
3. **While in flight / on failure**: a loading indicator (Module 17), and on a `401`
   from the login call specifically, a message that distinguishes "wrong username or
   password" from a network failure — not a generic "something went wrong."

## Scenario B — Submitting an order through the UI

1. **Angular sends**: the order form's values (Module 13's reactive form), as a `POST`
   to the mission service's `/accounts/{id}/orders`, with the access token from
   Scenario A attached via `Authorization: Bearer <token>` — added automatically by
   Module 15's interceptor, not typed by hand anywhere in the component.
2. **Signature check**: the mission service (`SecurityConfig`, unchanged since Sprint
   6). **Never sees the password**: the mission service — only `sprint8-auth-service`
   ever compares a password to a hash. **Never sees raw SQL**: the mission service's own
   controller code — MyBatis mappers (Sprint 6) parameterise every query underneath it.
3. **On `401`/`403`**: distinct messages — `401` means the interceptor's token is
   missing or expired (Module 15's guard should have redirected to login before this
   request was even sent); `403` means a real, authenticated trader without the right
   role, and the UI should say so plainly rather than showing a generic failure (Module
   17's actual subject matter).
4. **On success**: the holding row Postgres already has (`account_id`, `instrument_id`,
   `quantity`) updates in place — exactly the row today's demo confirmed by direct
   query. The trader finds out because the component re-fetches (or the response body
   already carries) the updated `newHoldingQuantity` and re-renders it, not because they
   reload the page and hope.

## The five boxes

- **Angular app** (Sprint 9, this sprint) — initiates login once, attaches the token to
  every subsequent request, renders both success and failure states. Does **not** check
  the token's signature itself, and does not talk to Postgres directly.
- **`sprint8-auth-service`** (Sprint 8) — the only box that ever sees a password. Called
  once per login, not once per request.
- **Mission service** (Sprint 5/6/7) — checks the token's signature and the trader's
  role on every request; queries Postgres via parameterised MyBatis mappers. Never
  checks a password, never calls the auth service back.
- **Postgres** (Sprint 3) — stores the real data. Only ever reached through the mission
  service.
- **Token storage** (Sprint 9, Module 9/15) — the one genuinely new piece of state this
  sprint introduces: something has to hold the token between the login response and the
  next request, and that something is Angular application state, not a cookie the
  browser manages for you by default. Modules 1-4 got away without this entirely — a
  hand-written `fetch()` call has nowhere to persistently store anything between page
  loads without deliberately reaching for `localStorage` or a cookie.

## Talking points for facilitators

- The most common mistake: an arrow from Angular straight to Postgres, or a note saying
  "Angular validates the token." Angular never talks to the database, and validating a
  JWT's signature happens on the SERVER that receives it, never in the browser — a
  client-side "validation" of a token it can't keep secret proves nothing.
- A second common gap: treating the login call and every subsequent call as the same
  shape. Login is the one request that does NOT carry a bearer token (there isn't one
  yet); every request after it should. A diagram that puts `Authorization: Bearer` on
  the login arrow has the sequence backwards.
- If a team's diagram shows the interceptor as a manual step inside every component
  ("component reads the token, adds the header"), that's worth flagging now: Module 15
  builds the interceptor specifically so no component ever has to know the token
  exists. It's a preview worth planting, not a mistake worth over-correcting today —
  it's also exactly the kind of repetitive-by-hand code Module 4's `fetch()` call
  would otherwise need to duplicate on every single request.
