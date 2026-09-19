# Lab 14 — Routing Fundamentals: Routes, Lazy Loading & Navigation

## Setup

Your own `mission-ui` from Module 13, with `HoldingsSummary` and `PlaceOrder` both currently
shown together in `app.html`.

## Task

1. In `app.routes.ts`, define at least two routes using `loadComponent`:

   ```typescript
   export const routes: Routes = [
     { path: '', redirectTo: 'holdings', pathMatch: 'full' },
     { path: 'holdings', loadComponent: () => import('./holdings-summary/holdings-summary').then((m) => m.HoldingsSummary) },
     { path: 'orders', loadComponent: () => import('./place-order/place-order').then((m) => m.PlaceOrder) },
   ];
   ```

2. Remove the direct `<app-holdings-summary />`/`<app-place-order />` tags from `app.html`
   and their imports from `app.ts` — they're routed now, not embedded.

3. Add a `<nav>` with two `routerLink`s (and `routerLinkActive`) to `app.html`, and import
   `RouterLink`/`RouterLinkActive` into `app.ts`'s `imports` array.

## Verify

1. `ng build`. Confirm your two lazy component names appear under **Lazy chunk files**, not
   in the initial `main.js` bundle.
2. `ng serve`. Loading the bare `/` should redirect you to `/holdings` automatically.
3. Click your "Place Order" link. Confirm the URL changes to `/orders`, the page does **not**
   reload, and the active link's styling moves to match.
4. Open DevTools' Network tab, clear it, then click between your two nav links a few times.
   Confirm each lazy chunk is only ever requested **once** — Angular caches it after the
   first visit, it doesn't re-fetch on every navigation back to a route already visited.

## A Question Worth Sitting With

`pathMatch: 'full'` is set on the `''` route's redirect, not on `'holdings'` or `'orders'`.
What would go wrong — specifically, what would happen when you tried to navigate to
`/orders` — if `pathMatch: 'full'` were removed from the `''` route entirely?

A second question: `loadComponent` fetches a component's code the first time its route is
visited, not when the app first loads. What's the practical trade-off here — name one
concrete situation where lazy loading a route makes the *user's* experience worse, not
better, and explain why.
