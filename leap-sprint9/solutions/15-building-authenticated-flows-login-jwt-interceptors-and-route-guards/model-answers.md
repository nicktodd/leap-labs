# Lab 15 Model Answers

## Verified Output

Built and run for real against the actual mission service, auth service, and
`sprint6-postgres`:

- Visiting `/holdings` with no prior login redirected to `/login` — the guard blocked the
  route before its component ever loaded.
- Logging in with `alice`/`mission123` moved the URL to `/holdings` and showed "Logged in as
  alice" in the header.
- Submitting a real order: the request to `http://localhost:8090/accounts/1/orders` carried a
  real `Authorization: Bearer ...` header, attached by the interceptor — confirmed directly
  from the network layer, not by reading the component's code. Postgres confirmed the holding
  quantity changed by exactly the submitted amount, the same check every module since 11 has
  used.
- Logging out cleared the token and returned the URL to `/login`; visiting `/holdings` again
  immediately redirected back, confirming the guard re-engaged without needing a page reload.

## Key Points

- **`TokenStore` as the one shared source of truth**: the login form, the interceptor, and the
  guard never reference each other directly — all three only know about `TokenStore`, which is
  what actually connects the flow.
- **The interceptor's URL check**: it decides *which* requests get the header attached, not
  *whether* a token exists.
- **The guard runs before the route's component loads**: an unauthenticated visitor never
  downloads the protected component's lazy chunk at all, not just fails to see it rendered.

## The Reflection Questions

**What breaks if the URL check is removed, verified directly**: removed the
`req.url.startsWith(MISSION_SERVICE_BASE)` check (leaving just `if (token)`), then logged in
twice in a row within the same running app instance (a second click of the same login form,
no page reload). The first login request correctly carried no `Authorization` header — no
token existed yet. The **second** login request — a call to the auth service's own
`/auth/login`, needing no token at all — carried a real, stale
`Authorization: Bearer eyJhbGciOiJIUzI1NiIs...` header, attached by the interceptor because a
token now existed in `TokenStore` from the first login. This is a genuinely confusing failure
mode in a real system: sending a leftover token to an endpoint whose entire purpose is
*issuing* tokens, which — depending on how strictly a real auth service parsed unexpected
headers — could range from harmless to actively confusing to debug. The URL check exists
specifically to keep "does a token exist" and "does *this* request need it" as two separate
questions.

**What changes if the session must survive a refresh**: `TokenStore` would need to persist
the token somewhere that survives a page reload — `localStorage` or a cookie — and read it
back on app startup instead of always starting `null`. The new risk this introduces is exactly
the one Module 4's `novalidate` and Module 13's server-message discussions kept returning to:
anything in `localStorage` is readable by any JavaScript running on the page, including a
successful XSS injection from an unrelated bug elsewhere in the app. An in-memory-only token
is invisible to anything except the running application's own JavaScript heap; a
`localStorage`-persisted token is one XSS vulnerability away from being readable by an
attacker's injected script. A cookie marked `HttpOnly` avoids that specific exposure (client
JavaScript can't read it at all) but shifts the problem to CSRF protection instead, since the
browser then attaches it automatically to every request to that domain, cross-site requests
included, unless explicitly guarded against.
