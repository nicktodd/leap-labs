# Lab 9 — Services & Dependency Injection in Angular

## Setup

Your own `mission-ui` from Module 8, with the `HoldingsSummary` component working.

## Task

### Part 1: Extract the service

1. Generate it:

   ```bash
   npx ng generate service holdings
   ```

2. Move `holdings`, `totalValue`, and the add/remove logic out of `HoldingsSummary` and into
   the generated `Holdings` class:
   - Keep the `holdings` signal `private`.
   - Expose a **read-only** view of it (`readonly all = this.holdings.asReadonly();`) rather
     than the raw writable signal.
   - Keep `totalValue` as a `computed()`, unchanged in spirit from Module 8.
   - Turn `addHolding`/`removeHolding` into plain methods (`add`/`remove`) that call
     `.update()` the same immutable way Module 8 did.

3. Update `HoldingsSummary` to `inject(Holdings)` instead of holding its own signals, and
   delegate its `addHolding()`/`removeHolding()` methods to the service. The `.html` template
   should need **no changes** — `holdings()` and `totalValue()` are still callable signals,
   just sourced differently now.

4. Rebuild and rerun. Confirm the component behaves *identically* to Module 8 — this step is
   a refactor, not a feature change.

### Part 2: Prove it's actually shared

5. Generate a second component:

   ```bash
   npx ng generate component portfolio-badge --standalone
   ```

6. Have it `inject(Holdings)` too, and display just `totalValue` — something like
   `Portfolio: {{ totalValue() | number: '1.2-2' }}`.

7. Add `<app-portfolio-badge />` to `app.html`, somewhere visibly separate from
   `<app-holdings-summary />` (the header is a good spot).

## Verify

1. Both the badge and the holdings list's own total show the *same* value on first load.
2. Click "Add" (or "Remove") in the holdings list. Both numbers update **together**, from
   one click, with no code in either component referencing the other.
3. Open DevTools' Console — no errors.
4. Open `holdings.ts` and confirm `holdings` itself is `private` — try (then undo) making it
   `public` and calling `.set()` directly from `PortfolioBadge`. Does anything stop you? What
   does that tell you about what `private` and `.asReadonly()` are each actually protecting
   against?

## A Question Worth Sitting With

Both `HoldingsSummary` and `PortfolioBadge` call `inject(Holdings)` independently, with no
constructor arguments passed between them and no shared parent component wiring them
together. Given that, explain in your own words *why* they end up sharing the exact same
data — what specifically guarantees `inject(Holdings)` doesn't hand each component its own
separate copy?

A second question: `add()` and `remove()` live on the service, not the component. If a third,
future component also needed to add a holding, what would that component need to do
differently from what `HoldingsSummary` already does? (Try to answer without looking at the
model answer — the honest answer is shorter than it might seem.)
