# Module 16 Demo Guide — Testing Angular: Unit Tests & End-to-End Tests with Playwright

**Duration:** 30 minutes
**Prerequisite:** Module 15's login flow. Same running backends. `@playwright/test` installed
as a dev dependency (`npm install --save-dev @playwright/test`).

Every module this sprint has been verified by hand — a screenshot, a Postgres query, a
Network tab check. Today turns that same verification into code that runs itself, every time,
without a person re-clicking through the app.

## Part 0: Running the Existing Test Suite — a Real Failure (5 min)

`ng test` already runs on every generated component and service, whether anyone's written a
meaningful assertion yet or not. Run it, live:

```bash
npx ng test --watch=false
```

Real output, before touching anything:

```
FAIL mission-ui src/app/app.spec.ts > App > should render title
AssertionError: expected 'Mission Control' to contain 'Hello, mission-ui'
```

A real, previously-unnoticed failure: the CLI-generated `app.spec.ts` still expects the
default scaffold's "Hello, mission-ui" text — Module 8 changed `app.html` to "Mission Control"
and nobody updated this test. This is exactly what unit tests are for: catching a real
mismatch between what a template says and what a test still expects, months after the change
that caused it.

```typescript
// Fixed
it('should render the Mission Control heading', async () => {
  const fixture = TestBed.createComponent(App);
  await fixture.whenStable();
  const compiled = fixture.nativeElement as HTMLElement;
  expect(compiled.querySelector('h1')?.textContent).toContain('Mission Control');
});
```

## Part 1: A Meaningful Unit Test for a Service (8 min)

`TokenStore` (Module 15) is a good unit-test target: pure logic, no HTTP, no DOM — exactly
what a unit test should isolate.

```typescript
it('becomes authenticated once a token is set, and exposes the username', () => {
  service.setToken('fake-jwt-token', 'alice');

  expect(service.isAuthenticated()).toBe(true);
  expect(service.getToken()).toBe('fake-jwt-token');
  expect(service.currentUsername()).toBe('alice');
});

it('returns to unauthenticated after clear()', () => {
  service.setToken('fake-jwt-token', 'alice');
  service.clear();

  expect(service.isAuthenticated()).toBe(false);
});
```

No real HTTP call, no real backend — a fake token string is enough, because this test's whole
job is checking `TokenStore`'s own logic, not whether the auth service works. Run it:

```
Test Files  11 passed (11)
     Tests  15 passed (15)
```

## Part 2: Where Unit Testing Stops (4 min)

`TokenStore`'s unit test can't tell you whether a real login actually reaches the real auth
service, whether the interceptor actually attaches the token, or whether the guard actually
redirects. Each of those pieces was designed to be testable in isolation (Module 15's whole
point), but *whether they're wired together correctly* is a different question — one only a
real browser, driving the real running app, can answer.

## Part 3: A Playwright Test for the Login Journey (10 min)

```typescript
// e2e/login.spec.ts
test('an unauthenticated visitor is redirected to /login', async ({ page }) => {
  await page.goto('/holdings');
  await expect(page).toHaveURL(/\/login$/);
});

test('logging in navigates to /holdings and shows the current user', async ({ page }) => {
  await page.goto('/login');
  await page.fill('#username', 'alice');
  await page.fill('#password', 'mission123');
  await page.click('button[type=submit]');

  await expect(page).toHaveURL(/\/holdings$/);
  await expect(page.locator('.session')).toContainText('Logged in as alice');
});
```

This is the exact same tool, and largely the exact same pattern, used to verify every demo
this entire sprint — the difference is that it's now a committed file, run with one command,
instead of a script in a scratchpad thrown away afterward.

```
playwright.config.ts
export default defineConfig({
  testDir: './e2e',
  use: { baseURL: 'http://localhost:4200' },
});
```

## Part 4: Verified — Running It for Real (3 min)

With `ng serve` running (and the real auth/mission services up):

```bash
npx playwright test
```

Real output:

```
Running 4 tests using 1 worker

  ✓  an unauthenticated visitor is redirected to /login (329ms)
  ✓  logging in navigates to /holdings and shows the current user (286ms)
  ✓  logging in with the wrong password shows an error and does not navigate (260ms)
  ✓  logging out returns to /login and re-blocks protected routes (317ms)

  4 passed (2.7s)
```

Four real browser sessions, each driving the actual running app against the actual running
backends — not a mock, not a stub standing in for the auth service.

## Key message

Unit tests isolate one piece of logic and answer "does this one thing behave correctly on its
own." End-to-end tests answer a different question entirely: "does the whole system, wired
together, actually work the way a person experiences it." Neither replaces the other —
`TokenStore`'s unit test would still pass even if the login form never called it; the
Playwright test would still fail if it did.

## Transition to the Lab

Learners write one meaningful unit test of their own (for a component or service this sprint
built) and one Playwright test covering the login journey end-to-end — run for real, against
the real running app, not asserted to work.
