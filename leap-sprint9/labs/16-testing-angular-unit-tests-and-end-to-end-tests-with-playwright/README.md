# Lab 16 — Testing Angular: Unit Tests & End-to-End Tests with Playwright

## Setup

Your own `mission-ui` from Module 15. Same running backends.

```bash
npm install --save-dev @playwright/test
npx playwright install chromium
```

## Task

### Part 1: A meaningful unit test

1. Run `npx ng test --watch=false` first, before changing anything. Read the output
   carefully — do all the generated tests actually pass? If any fail, don't skip past it:
   fix the underlying mismatch (a stale assertion, a template that changed since the test was
   generated), the same way today's demo found and fixed one for real.
2. Pick one component or service you're confident you understand well (`TokenStore` is a good
   choice if you want to follow the demo closely, but any service with real logic works) and
   write at least two meaningful test cases beyond the generated "should be created" — cases
   that would actually fail if the underlying logic were broken.

### Part 2: A Playwright test for the login journey

3. Create `playwright.config.ts` at the project root, with `testDir: './e2e'` and
   `use: { baseURL: 'http://localhost:4200' }`.
4. Create `e2e/login.spec.ts` with at least these cases:
   - Visiting a protected route while unauthenticated redirects to `/login`.
   - Logging in with valid credentials navigates to a protected route and shows the logged-in
     state.
   - Logging in with invalid credentials shows an error and does not navigate.
   - Logging out returns to `/login` and re-blocks the protected route.

## Verify

1. `npx ng test --watch=false` — confirm your new unit test(s) pass, and that the total test
   count went up.
2. With `ng serve` running (and both real backends up), run `npx playwright test`. Confirm
   all four scenarios pass — genuinely, against your real running app, not a mock.
3. Deliberately break something — comment out the `authGuard`'s redirect, or hardcode
   `isAuthenticated` to always return `true` — and rerun both suites. Confirm the Playwright
   suite catches it even though the unit tests (if they don't touch the guard directly) might
   not. Then undo the break.

## A Question Worth Sitting With

The lab's "deliberately break something" step asks you to disable the guard and rerun both
test suites. If your `TokenStore` unit tests still pass after that change, but your
Playwright suite fails, what does that tell you about what each kind of test was actually
checking — and why would relying on unit tests alone have let this specific bug ship?

A second question: today's Playwright tests hit the *real* auth service and mission service,
not a mock. What would you lose, and what would you gain, if these tests instead ran against
a mocked backend that always returned a canned successful login response?
