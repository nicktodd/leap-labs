# Lab 4 — Fetch & Browser HTTP: Calling a Real API Without a Framework

## Setup

No build tools, no npm, for the page itself. Edit `script.js` in any plain-text editor.

Two things have to be running, exactly as in today's demo:

1. **`sprint8-auth-service`** on `http://localhost:3000`, with CORS enabled for your page's
   origin (`app.enableCors({ origin: "http://localhost:8000" })` in `main.ts` - ask your
   trainer if this isn't already set up on the class copy).
2. **This lab's page served over HTTP, not opened as a `file://` URL** - run
   `python3 -m http.server 8000` from this folder, then visit `http://localhost:8000` in a
   browser. Fetch's CORS rules only make sense with a real origin; today's demo showed
   exactly what goes wrong otherwise.

## Task

Complete the five TODOs in `script.js`:

1. **TODO 1** — mark the submit handler `async`, keep `event.preventDefault()` first.
2. **TODO 2** — `await fetch(AUTH_URL, ...)` with a `POST`, JSON headers, and a JSON body
   built from both input values.
3. **TODO 3** — check `response.ok`; on failure, read the error body and show it.
4. **TODO 4** — on success, read the body and show the token (truncated).
5. **TODO 5** — wrap it all in `try`/`catch`/`finally`: `catch` handles a network-level
   failure, `finally` re-enables the submit button.

Run this now, before changing anything: submit the form. Nothing happens beyond a "Logging
in..." message that never resolves — no `fetch()` call exists yet. That's the starting
point.

## Verify

Test all three outcomes, the same way today's demo did:

1. **Valid login** — `alice` / `mission123`. A green message should appear showing the
   start of a real JWT.
2. **Invalid credentials** — `alice` / anything else (8+ characters, so the client-side
   `minlength` doesn't block it first). A red message should read something like "Login
   failed: invalid username or password" — this comes from `response.ok` being `false`,
   not from `catch`.
3. **Network failure** — stop `sprint8-auth-service` (or temporarily remove
   `enableCors()`), then submit. A red message should still appear, but this time it's
   `catch` that caught it — check DevTools' Console tab for a logged `fetch() rejected:
   TypeError` matching today's demo's own CORS failure.

In all three cases, the submit button should always end up re-enabled — that's `finally`
doing its job regardless of which path executed.

## A Question Worth Sitting With

TODO 3 and TODO 5's `catch` block both end up showing a red error message via
`showMessage()`. Given that both paths look identical to the user, why does the code still
need to distinguish them internally with a `response.ok` check *inside* `try`, rather than
letting every failure — HTTP or network — fall through to one `catch` block?

A second question: `AUTH_URL` is hardcoded as `http://localhost:3000/auth/login` in
`script.js`, visible to anyone who views the page's source. What does that imply about what
kind of information is safe to reference directly in front-end JavaScript, versus what
should never appear there at all?
