# Lab 10 — HTTP Communication: HttpClient, Observables & Error Handling

## Setup

Your own `mission-ui` from Module 9, with the `Holdings` service and `PortfolioBadge`
working. Copy `mock-server.js` from this folder into your workspace (anywhere outside
`mission-ui`'s own `src/` is fine) and run it:

```bash
node mock-server.js
```

No dependencies — plain Node. Confirm it's up with `curl http://localhost:3500/api/holdings`
before touching Angular.

## Task

1. Register `HttpClient` once, in `app.config.ts`:

   ```typescript
   import { provideHttpClient } from '@angular/common/http';
   // add provideHttpClient() to the providers array
   ```

2. In `holdings.ts`, `inject(HttpClient)` and add a `loadError` signal (`signal<string |
   null>(null)`).

3. Add a method `loadFromApi(url: string): void` that:
   - Calls `this.http.get<Holding[]>(url)`.
   - Uses `.pipe(catchError(...))` to catch a failed request, set `loadError` to a message
     built from the real error, and return `of(null)` to keep the stream alive.
   - `.subscribe()`s to the result — if it's not `null`, clear `loadError` and `.set()` the
     holdings signal with the new data.

4. In `HoldingsSummary`, add two buttons: one calling `loadFromApi('http://localhost:3500/api/holdings')`,
   one calling `loadFromApi('http://localhost:3500/api/holdings/error')` — and show
   `loadError()` in the template when it's set (an `@if` block is enough).

## Verify

1. Click "Load From API" (or whatever you named it). The two Module 8/9 seeded holdings
   should be **replaced** by the mock server's real response (`VOD.L`, `HSBA.L`) — and the
   header badge from Module 9 should update too, with zero code connecting the two components
   directly.
2. Click the error-simulating button. A real error message should appear (something like
   `Http failure response for ... 500 Internal Server Error`) — and the **existing** holdings
   should stay exactly as they were, not get wiped out.
3. Open DevTools' Network tab while clicking both buttons — confirm you can see the real
   requests and their real 200/500 responses.

## A Question Worth Sitting With

`catchError`'s callback returns `of(null)` rather than, say, `of([])`. The `subscribe`
callback then checks `if (data)` before calling `.set()`. Trace through what would happen on
a failed request if `catchError` instead returned `of([])` and `subscribe` unconditionally
called `this.holdings.set(data)` — what would the user see, and why is that worse than what
the current code does?

A second question: `HttpClient`'s `.get()` doesn't send a request until something calls
`.subscribe()` on it. Module 4's `fetch()` sends its request the moment it's called, `await`
or not. What practical difference could this make if a component created a `.get()` call but
a bug meant `.subscribe()` was never called on it?
