# Lab 13 Model Answers

## Verified Output

Built and run for real against the actual mission service, auth service, and
`sprint6-postgres`:

- Blanking the quantity field and moving focus away: `field-error` "Quantity must be greater
  than 0." appeared without any submission happening.
- A valid `BUY` order: real `ACCEPTED` response, fee `0.04`, new holding quantity
  incrementing by exactly the submitted quantity each time (511 → 512 across two runs).
- A `SELL` order for `999999` shares of `ULVR.L`: real `422`, with the message
  `cannot sell more than the current holding` — Sprint 5's `OrderValidator`, unchanged,
  firing for real.
- Stopping the mission service entirely and submitting: a real network failure, surfaced as
  `Http failure response for http://localhost:8090/accounts/1/orders: 0 Unknown Error` — the
  `error.error?.message` optional chain correctly found nothing and fell back to
  `error.message`, rather than throwing.

## Key Points

- **`Validators.min(0.01)` vs `OrderValidator`'s `quantity <= 0` check**: these look similar
  but check fundamentally different things — one is a property of the *input's shape*
  (client-checkable, instantly, no network round-trip), the other depends on *server-side
  state* the client has no access to (the account's current holding).
- **`markAllAsTouched()`**: without this, submitting a completely untouched, all-invalid form
  would show zero error messages, because `.touched` only becomes `true` once a control has
  been interacted with — a real, easy-to-miss reactive-forms gotcha.
- **`error.error?.message`**: reads the real response body Sprint 6's
  `GlobalExceptionHandler` (Module 10) always returns on a 4xx/5xx — `error.message` alone is
  just Angular's own generic wrapper text.

## The Reflection Questions

**Is the server-side check now redundant?** No — arguing otherwise repeats exactly the
mistake Module 4's `novalidate` discussion warned against: client-side validation is
something the *browser* enforces, and nothing stops a request from reaching the real
mission service through any other path — a different client, a mobile app built later, a
`curl` command, or a browser with JavaScript disabled or tampered with via DevTools. The
client-side `Validators.min(0.01)` check exists purely for immediate user feedback (no
network round-trip needed to tell someone "type a positive number"); the server-side check in
`OrderValidator` exists because the server is the only thing that can't be bypassed by
whoever is calling it. Removing the server check wouldn't just be redundant — it would remove
the *only* enforcement of that rule that actually matters for correctness.

**When would `error.error` not have a `.message`?** Verified directly: stopping the mission
service and submitting produces exactly this — `error.error` is not a parsed JSON object at
all in a genuine network failure (connection refused, CORS block, timeout), because there was
never a response body to parse. In that case `error.error?.message` evaluates to `undefined`,
and the code's `?? error.message` fallback supplies Angular's own generic wrapper text
instead (`Http failure response for ... 0 Unknown Error`) — the UI still shows *something*
reasonable rather than crashing on `Cannot read properties of null`, which is exactly why the
optional chain was written that way rather than assuming `error.error.message` always exists.
