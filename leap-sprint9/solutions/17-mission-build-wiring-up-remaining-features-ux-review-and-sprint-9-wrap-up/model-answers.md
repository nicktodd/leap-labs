# Lab 17 Model Answers

## Verified Output

Run for real, against `solutions/mission-ui` and the real backends:

- Before the fix: submitted a real BUY order for 5 ULVR.L @ 46 while holding 500 @ 42.1.
  Order response came back `ACCEPTED - fee 0.45, new holding quantity 539`, but the Holdings
  screen still showed `500 @ 42.1` and the portfolio badge still showed `34,070.00`.
- After the fix (`MissionApi.submitOrder` now calls `Holdings.setQuantity` with the response's
  `newHoldingQuantity`): the same order updated Holdings to `539 @ 46` and the portfolio badge
  to `37,814.00` - screenshotted via Playwright against the real running app.
- `npx ng test --watch=false` after the fix: **15 passed (15)** - unchanged from Module 16.
- `npx playwright test` after the fix: **4 passed** - Module 16's login-journey suite,
  unchanged.
- Added a `submitting` signal to `MissionApi`, bound to `[disabled]` on the submit button, so a
  second click can't fire while the first request is still in flight.

## Key Points

- **The gap was real, not contrived**: `MissionApi` and `Holdings` were both individually
  correct - the order endpoint really does return the right new quantity, and `Holdings`'s
  `computed()` total really does derive from its own signal correctly. Neither was ever told
  about the other.
- **`newHoldingQuantity` as the source of truth**: the fix sets the holding directly from the
  backend's own arithmetic, rather than re-deriving it client-side from the order's side and
  quantity - the backend already did that arithmetic once, correctly, so there's no reason to
  duplicate it and risk it drifting out of sync.

## The Reflection Question

**What a passing test suite does and doesn't guarantee**: Module 16's suite passing the whole
time this gap existed proves the suite verifies exactly what it was written to verify - that a
guard blocks an unauthenticated route, that `TokenStore`'s own logic behaves correctly - and
nothing more. A test suite is not a general claim that "the app works"; it is a specific claim
about the behaviours someone thought to write assertions for. This gap sat between two features
built in different modules, and nobody had written a test that submits an order and then checks
the holdings list, because nobody had connected those two ideas yet. Catching it automatically
would have needed a new integration-style test - something like a Playwright scenario that logs
in, places an order, navigates to Holdings, and asserts the displayed quantity actually changed
- which is a genuinely different kind of test from anything Module 16 wrote, not a stricter
version of an existing one.
