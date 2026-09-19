# Lab 16 Model Answers

## Verified Output

Run for real, against `solutions/mission-ui` and the real backends:

- `npx ng test --watch=false` before any changes: **1 failure** — `app.spec.ts` expected
  "Hello, mission-ui", the CLI's default scaffold text, which Module 8 replaced with
  "Mission Control" and nobody had updated the test for since. Fixed the assertion.
- `TokenStore`'s new tests (`isAuthenticated`/`getToken`/`currentUsername`, before and after
  `setToken`/`clear`): **all pass**.
- `npx playwright test`, real browser against the real running app and real backends:
  **4 passed** — unauthenticated redirect, successful login, invalid-credentials error, and
  logout re-blocking.
- Deliberately broke `authGuard` (replaced its body with `return true;` unconditionally),
  then reran both suites:
  - `ng test`: **still 15 passed** — nothing in the unit test suite touches the guard.
  - `npx playwright test`: **2 failed** — "an unauthenticated visitor is redirected to
    /login" and "logging out returns to /login and re-blocks protected routes" both failed,
    with the real error `Expected pattern: /\/login$/, Received string:
    "http://localhost:4200/holdings"`.

## Key Points

- **The stale `app.spec.ts` assertion**: a real, unplanned finding — not a contrived example.
  It sat unnoticed since Module 8 because nothing ran the test suite in between.
- **Unit tests for `TokenStore`**: no HTTP, no DOM, no router — a fake token string is enough
  to exercise every branch of the service's own logic.

## The Reflection Questions

**What the unit-tests-pass/e2e-fails split reveals**: `TokenStore`'s unit tests only ever
call `TokenStore` directly — they have no idea a guard, a router, or a route even exist.
Breaking `authGuard` doesn't touch any code path those tests execute, so they have no way to
notice. The Playwright suite is the only test that actually drives a browser through the real
route configuration, so it's the only one positioned to notice that visiting `/holdings`
unauthenticated no longer redirects. This is precisely why relying on unit tests alone would
let this exact regression ship: a broken guard is invisible to every test that doesn't
exercise routing end-to-end, and `TokenStore`'s own correctness (which the unit tests
genuinely do verify) says nothing about whether anything actually *uses* it correctly.

**Mocking the backend instead of hitting the real one**: a mocked backend would make the
suite faster and independent of whether the real auth/mission services happen to be running
— useful for CI environments where standing up a full Postgres + Spring Boot + NestJS stack
per test run is expensive. What's lost is coverage of the actual integration: a mock that
always returns a canned successful login response can't catch a real CORS misconfiguration, a
real backend contract change (a renamed field in `LoginResponse`), or the exact kind of
mission-service `produces` bug Module 12 found. Today's suite caught a real, undiagnosed
regression precisely because it exercises the genuine network path; a fully mocked version
would have passed with the guard broken, the same blind spot the unit tests already have.
