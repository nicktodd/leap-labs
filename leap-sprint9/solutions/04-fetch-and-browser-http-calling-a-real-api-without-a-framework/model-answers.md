# Lab 4 Model Answers

## Verified Output

Ran headlessly with Playwright against a real, running `sprint8-auth-service`
(CORS-enabled, port 3000), page served on `http://localhost:8000`:

- `alice` / `mission123` produced `Logged in. Token starts: eyJhbGciOiJIUzI1NiIs...` — a
  real JWT, not a placeholder.
- `alice` / `wrongpass` produced `Login failed: invalid username or password` — the real
  401 body from the service, surfaced through the `response.ok` branch, not `catch`.

## Key Points

- **TODO 1**: the callback passed to `addEventListener` has to be `async` itself —
  `await` is illegal inside a non-`async` function, and marking the *listener*, not
  `showMessage()` or any other helper, is what matters here.
- **TODO 2**: `fetch()`'s second argument (`method`, `headers`, `body`) is a plain object,
  not a class instance — `body` specifically has to be a *string*, which is why
  `JSON.stringify()` wraps the request object even though the server ultimately parses it
  back into JSON.
- **TODO 3**: `response.ok` is `true` for any 2xx status, `false` otherwise —
  `response.status === 200` would miss a legitimate `201 Created` elsewhere in a real API,
  so `.ok` is the more general check.
- **TODO 4**: `data.accessToken.slice(0, 20)` is purely a display choice — the full token
  is already sitting in `data.accessToken`, unslic­ed, ready for Module 15 to actually
  store and use it.
- **TODO 5**: `submitBtn.disabled = true` and the "Logging in..." message belong *before*
  the `try` block, not inside it — they need to run regardless of which branch of the
  `try`/`catch` ends up executing, and `finally`'s re-enable is the only code guaranteed to
  run no matter what.

## The Reflection Questions

**Why distinguish `response.ok` from `catch` internally, even though both show the same
kind of red message**: because the two failures mean genuinely different things, and a
real application (or Module 10's `HttpClient`-based Angular services) often needs to react
differently — a 401 might prompt "check your password," while a network failure might
prompt "check your connection" or trigger a retry. Collapsing both into one `catch` block
would work today because `showMessage()` happens to be generic enough to cover either, but
it would throw away information a more capable UI would want. It's also *correctness*, not
just UX: a `try` block that never checks `response.ok` will silently treat a 401 as success,
because `fetch()` genuinely did not throw — that bug is invisible until someone tests with
bad credentials specifically.

**What's safe to hardcode in front-end JavaScript**: a *URL* is fine — it's public
information the moment the browser sends a request to it anyway, visible in the Network tab
regardless of whether it's hardcoded or not. What must never appear here is anything secret
that authorizes access on its own: an API key, a database password, a signing secret (like
`sprint8-auth-service`'s own `JWT_SECRET`). The username/password typed into this form are
sent *to* the server, not stored *in* the JavaScript — that's the difference. Anything
committed into `script.js` ships to every visitor's browser, readable via "View Source," so
the front end can only ever hold things that are safe to be public or that the user
themself just typed in.
