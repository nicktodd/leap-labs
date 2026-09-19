# Lab 8 — Components & Templates: Standalone Components & Signals

## Setup

Your own `mission-ui` from Module 7, with `ng serve` working.

## Task

Build a `holdings-summary` component, the same shape as today's demo, in your own project:

1. Generate it:

   ```bash
   npx ng generate component holdings-summary --standalone
   ```

2. In `holdings-summary.ts`, add:
   - An `interface Holding` with `ticker: string`, `quantity: number`, `price: number`.
   - A `signal<Holding[]>` called `holdings`, seeded with at least two starter rows of your
     choice (any tickers, quantities, prices).
   - A `computed()` called `totalValue` that sums `quantity * price` across every holding.
   - A method `addHolding()` that appends one new holding to the signal via `.update()`.
   - A method `removeHolding(ticker: string)` that removes a holding by ticker, also via
     `.update()`.

3. In `holdings-summary.html`, render the list with `@for`/`@empty`, a Remove button per row
   (calling `removeHolding`), the computed total, and an Add button (calling `addHolding`).
   Use the `number` pipe (`{{ totalValue() | number: '1.2-2' }}`) for the total — remember it
   needs importing (`DecimalPipe` from `@angular/common`) in the component's own `imports`
   array, since this is a standalone component.

4. Add `<app-holdings-summary />` to `app.html`, and import `HoldingsSummary` into `app.ts`'s
   `imports` array.

## Verify

1. `ng serve`, open the browser: your two seeded holdings appear, with a correct total value
   (calculate it by hand once to check).
2. Click Add: a new row appears, and the total updates **without you writing any code that
   directly recalculates it** — that's `computed()` doing its job.
3. Click Remove on a row: it disappears, and the total updates again, the same way.
4. Open DevTools' Console tab — no errors at any point in this flow.

## A Question Worth Sitting With

`addHolding()` and `removeHolding()` both use `.update()` with a callback that returns a
**new** array (spread or `.filter()`), rather than mutating `this.holdings()` in place. Try
it: change `addHolding()` to mutate in place instead —

```typescript
this.holdings.update((current) => {
  current.push({ ticker: 'BP.L', quantity: 200, price: 4.8 });
  return current; // same array reference as before
});
```

Click "Add BP.L" a few times and watch closely. The new row *does* appear in the list each
time — but does "Total value" change? Run it and see for yourself before reading on. The
result is stranger than either "everything breaks" or "everything works," and explaining
*why* the list and the total disagree is the actual point of this question.

A second question: `holdings` and `totalValue` are both marked `protected readonly`. What
would break — for the component itself, not for anything outside it — if `totalValue` were
declared as a plain signal (`signal(0)`) that `addHolding()`/`removeHolding()` manually
`.set()` after modifying `holdings`, instead of a `computed()`?
