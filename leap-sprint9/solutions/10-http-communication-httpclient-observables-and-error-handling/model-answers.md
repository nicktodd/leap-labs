# Lab 10 Model Answers

## Verified Output

Built and run for real against `solutions/mock-server.js` (`node mock-server.js`) and
`solutions/mission-ui`:

- "Load From API" click: holdings list changed from the seeded `ULVR.L`/`AZN.L` to the mock
  server's real `VOD.L - 800 @ 0.72` / `HSBA.L - 300 @ 6.4`, total value `2,496.00`, header
  badge matching.
- "Simulate API Error" click (fresh page load): error text
  `Could not load holdings: Http failure response for
  http://localhost:3500/api/holdings/error: 500 Internal Server Error`, with the original
  seeded holdings still showing unchanged, total value still `34,070.00`.

## Key Points

- **`provideHttpClient()`**: registered once in `app.config.ts`, the same pattern as
  `provideRouter` — an application-wide provider, not something each component sets up
  individually.
- **`inject(HttpClient)`**: identical pattern to `inject(Holdings)` from Module 9 — DI isn't
  special-cased for framework-provided services versus your own.
- **`.pipe(catchError(...))`**: `catchError`'s callback receives the actual `HttpErrorResponse`
  — `error.message` is real, not constructed, which is why the verified error text above
  matches Angular's own wording exactly.
- **`.subscribe()`**: nothing happens — no request is even sent — until this is called. This
  is the core Observable-vs-Promise distinction Module 4's `fetch()` didn't have to teach.

## The Reflection Questions

**Why `of(null)` + `if (data)`, not `of([])` + unconditional `.set()`**: if `catchError`
returned `of([])` and `subscribe` always called `.set(data)`, a failed request would silently
**replace** the existing holdings with an empty list — the user would see "no holdings" and
have no way to tell whether that's real (an empty portfolio) or a failure being hidden as if
it were a legitimate answer. `of(null)` plus the `if (data)` guard means a failure changes
*nothing* about what's already on screen except surfacing the error message — the UI stays
in its last known-good state, which is almost always what a real user wants from a failed
refresh.

**Why `.subscribe()` being skipped matters practically**: because Observables are *lazy*
(nothing runs until subscribed), a bug that constructs `this.http.get<Holding[]>(url)` but
never calls `.subscribe()` on it results in **no HTTP request being sent at all** — not a
silent failure, not a hung request, literally nothing happens over the network. This is a
genuinely common Angular bug (usually from refactoring code that used to subscribe and
forgetting to keep the `.subscribe()` call), and it's easy to miss because nothing throws an
error — the code just quietly does nothing. Module 4's `fetch()` can't have this exact bug:
the request fires the instant `fetch()` is called, whether or not anything ever `await`s the
result.
