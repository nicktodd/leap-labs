# Lab 11 Model Answers

## Verified Output

Run for real against the actual Sprint 6 mission service (CORS-enabled, port 8090 in this
setup), Sprint 8 auth service (CORS-enabled, port 3000), and `sprint6-postgres`:

- Before clicking: `ULVR.L` holding quantity `503.0000` (queried via `psql`).
- After clicking "Submit Test Order" (BUY 1 ULVR.L @ 40.0): browser showed
  `ACCEPTED - fee 0.04, new holding quantity 504`.
- Re-querying Postgres: `ULVR.L` holding quantity `504.0000` — the exact `+1` the test order
  submitted, confirmed independently of what the browser claimed.

## Key Points

- **CORS on two different servers**: the mission service (Spring Boot) and the auth service
  (NestJS) each needed their own CORS fix — there's no single place this gets configured
  once for "the backend," because from the browser's perspective they're two entirely
  separate origins.
- **`switchMap`**: takes the login response and returns a *new* Observable (the order
  request) that depends on it — this is how a genuinely sequential, dependent chain of two
  HTTP calls is expressed with Observables, without manually nesting `.subscribe()` calls.
- **Nothing new in the component**: `PlaceOrder` uses exactly Module 9's `inject()` pattern
  and Module 8's signal-reading pattern — proof that a service's *internals* can grow
  significantly more complex (two chained real HTTP calls, an external system on the other
  end) without the component that uses it needing to change shape at all.

## The Reflection Questions

**Why `switchMap` in one `.pipe()`, not nested subscribes**: with nested subscribes, an
error from the *second* (order) call would land in that inner `.subscribe()`'s own error
handling — completely separate from any `catchError` attached to the outer login call. You'd
need to write error handling twice, once per call, and keep both in sync by hand. With
`switchMap` inside one `.pipe()`, both calls are part of the *same* stream, so a single
`catchError` at the end catches a failure from either step — a failed login or a failed
order both flow through the identical error path this lab already wrote once. This is also
why `switchMap` is preferred generally in Angular code over manual nesting: it composes with
every other RxJS operator (retry, timeout, further chaining) the same way a single call
would, where nested subscribes don't compose at all — they're just imperative code hiding
inside a callback.

**Is hardcoding `alice`/`mission123` a problem, and why is it acceptable here**: in a real
shipped application, yes — credentials should never be embedded in front-end source, for
exactly the reason Module 4 raised: anything in `script.js`/`.ts` ships to every visitor's
browser. It's acceptable *here* specifically because Module 11's whole scope is deliberately
narrow — "prove the mission service call itself works" — and Module 15 is explicitly
described as building the real login form, JWT interceptor, and route guard that replace this
exact hardcoded call. This is a temporary stand-in with an explicit, named successor, not a
production shortcut — the comment in `mission-api.ts` says so directly, and a real code
review should treat any hardcoded credential without that kind of explicit, dated
replacement plan as a genuine problem.
