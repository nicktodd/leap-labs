# Module 17 Demo Guide — Mission Build: Wiring Up Remaining Features, UX Review & Sprint 9 Wrap-up

**Duration:** 30 minutes
**Prerequisite:** Module 16's test suite. Same running backends.

## Part 0: A Gap That Sixteen Modules of Testing Didn't Catch (5 min)

Module 16 built a whole test suite - unit tests, an end-to-end suite - and it all passes. That
doesn't mean the app is finished. Log in and place a real order:

```
Before: Portfolio: 34,070.00
        ULVR.L - 500 @ 42.1
```

Submit a BUY order for 5 more shares of ULVR.L at 46, then look at the Holdings screen.

Real output, before any fix:

```
Portfolio: 34,070.00   <- unchanged
ULVR.L - 500 @ 42.1    <- unchanged
```

The order genuinely succeeded - `OrderResponseDto` came back with `status: ACCEPTED` and a real
`newHoldingQuantity` - but nothing in `PlaceOrder` or `MissionApi` ever did anything with that
number. `Holdings` (Module 9's service, still holding its original two hardcoded rows) had no
idea an order had even been placed. This is exactly the kind of gap Module 16's tests don't
catch, because no test ever asserted that placing an order should change the holdings list -
the two features were built independently, in different modules, and never wired together.

## Part 1: Making the Order Response the Source of Truth (8 min)

```typescript
// mission-api.ts
submitOrder(order: OrderRequestDto): void {
  this.error.set(null);
  this.submitting.set(true);

  this.orderApi
    .submitOrder(ACCOUNT_ID, order)
    .pipe(
      catchError((error: HttpErrorResponse) => {
        const serverMessage = error.error?.message;
        this.error.set(`Order failed: ${serverMessage ?? error.message}`);
        return of(null);
      }),
    )
    .subscribe((response) => {
      this.submitting.set(false);
      if (response) {
        this.lastOrder.set(response);
        if (response.newHoldingQuantity !== undefined) {
          this.holdings.setQuantity(order.ticker, response.newHoldingQuantity, order.price ?? 0);
        }
      }
    });
}
```

```typescript
// holdings.ts - a new method, not a rewrite of the service
setQuantity(ticker: string, quantity: number, price: number): void {
  this.holdings.update((current) => {
    const existing = current.find((h) => h.ticker === ticker);
    if (existing) {
      return current.map((h) => (h.ticker === ticker ? { ...h, quantity, price } : h));
    }
    return [...current, { ticker, quantity, price }];
  });
}
```

`newHoldingQuantity` is the authoritative figure - the backend already did the arithmetic
(existing position plus or minus this order), so the front end sets it directly rather than
re-deriving it from the order side and quantity.

## Part 2: Verified — The Fix, For Real (5 min)

Same order, same starting state, after the fix:

```
Before: Portfolio: 34,070.00
        ULVR.L - 500 @ 42.1

Submitted: BUY 5 ULVR.L @ 46
Order result: ACCEPTED - fee 0.45, new holding quantity 539

After:  Portfolio: 37,814.00
        ULVR.L - 539 @ 46
```

`portfolio-badge` and `holdings-summary` both read from the same `Holdings.totalValue`
computed signal - neither component changed at all. Fixing one shared service's data was
enough for both to update correctly, which is the whole reason Module 9 put holdings behind a
service in the first place.

## Part 3: A Small UX Gap, Also Found by Actually Using the App (5 min)

Submit an order and watch the button. Nothing tells the user a request is in flight - on a slow
network, a learner could click Submit Order twice.

```typescript
// mission-api.ts
readonly submitting = signal(false);
```

```html
<!-- place-order.html -->
<button type="submit" [disabled]="submitting()">
  {{ submitting() ? 'Submitting...' : 'Submit Order' }}
</button>
```

A one-line template change, but it closes a real gap: without it, `HttpClient`'s async request
gives no feedback during the round trip, and the form stays clickable the whole time.

## Part 4: Verified — Nothing Broke (5 min)

```bash
npx ng test --watch=false
```

```
Test Files  11 passed (11)
     Tests  15 passed (15)
```

```bash
npx playwright test
```

```
  ✓  an unauthenticated visitor is redirected to /login
  ✓  logging in navigates to /holdings and shows the current user
  ✓  logging in with the wrong password shows an error and does not navigate
  ✓  logging out returns to /login and re-blocks protected routes

  4 passed
```

Module 16's whole suite still passes unchanged - the fix touched `MissionApi` and `Holdings`,
neither of which either test suite directly asserts against, which is itself worth noting: the
suite catching a broken guard in Module 16 doesn't mean it catches every kind of gap, only the
kind it was written to look for.

## Part 5: UX Review — What Sixteen Modules Left Unfinished

A short walk through the whole app, looking at it as a user rather than as a stream of modules:

- The holdings list still has "Add BP.L", "Load From API", and "Simulate API Error" buttons
  left over from Modules 9 and 10's demos - useful for teaching, not for a real user.
- There's no way to view past orders - `lastOrder` shows only the most recent one, then it's
  gone on refresh (deliberately, per Module 15 - no persistence layer was ever built).
- Form validation messages (Module 13) only appear after a field is touched - correct
  behaviour, but worth confirming out loud that everyone in the room understands why.

None of this gets fixed today - the point of a UX review is to look honestly at what's there,
not to file a mile of new tickets in the last hour of a training course.

## Key Message

Every module this sprint tested one thing in isolation and verified it worked. Nothing until
today verified that two independently-correct features - order submission and the holdings
display - actually agreed with each other once wired together. Integration gaps like this are
exactly what unit tests, by design, cannot see; they only turn up when someone uses the whole
app end to end, which is what today's first ten minutes did before writing a single line of
code.

## Transition to the Lab

Learners do their own UX pass over their own `mission-ui`: find one real gap (a component that
doesn't reflect a change another component made, a missing loading state, a leftover demo
button), fix it, and verify the fix the same way - live, against the real running app.
