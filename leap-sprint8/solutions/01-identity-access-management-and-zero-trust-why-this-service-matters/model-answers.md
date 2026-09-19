# Module 1 — Model Answers

There's no code for this module — this is what a strong whiteboard sketch should contain.

## Scenario A — First-time login

1. **Client sends**: a username and password (eventually, in Module 11, to
   `sprint8-auth-service`'s `POST /login`) — exactly the same shape as today's demo's call to
   `shared/auth-stub`.
2. **The auth service checks**: does a user with that username exist, and does the submitted
   password match the STORED, HASHED password (Module 12 — never a plaintext comparison like
   today's stub does).
3. **Inside the token**: a subject claim (who — the username or user ID), a roles/permissions
   claim (what they're allowed to do), an expiry, and a signature — identical in shape to what
   `shared/auth-stub` already issues, which is exactly why the mission service needs zero changes
   to accept it.
4. **The client**: stores the token (in practice, often in memory or a secure cookie) and attaches
   it to every subsequent request to a protected endpoint.

## Scenario B — Using the token

1. **Client sends**: the token in an `Authorization: Bearer <token>` header, alongside the actual
   order request body — exactly matching the demo's `curl -H "Authorization: Bearer $TOKEN"`.
2. **The mission service checks**: the token's SIGNATURE, using the shared secret it already has
   — proving the token could only have been issued by something that knows that secret. It does
   **not** call the auth service to ask "is this still valid" — that's the zero-trust point:
   trust is established by the signature check alone, with no network round-trip back to the
   issuer.
3. **If invalid or missing**: `401 Unauthorized` — exactly what the demo's smoke test verified
   live, before any real credential logic existed anywhere in this sprint's own code.
4. **If valid but wrong role**: the request should be rejected too, but with `403 Forbidden`, not
   `401` — the token proved WHO the trader is (authentication succeeded), but the mission
   service's own authorization check on that endpoint should reject the role. This decision
   happens inside the mission service, using the roles claim already inside the token — not a
   separate call anywhere.

## The one sentence per box

- **Client**: initiates login, stores the token, attaches it to every subsequent request. Does
  NOT decide what it's allowed to do — it finds that out from the responses it gets back.
- **Auth service**: the ONLY place a password is ever checked. Issues tokens. Does NOT get asked
  "is this token still good?" after the fact — signature verification doesn't need it.
- **Mission service**: verifies signatures and enforces per-endpoint role checks. Does NOT store
  passwords, does NOT call the auth service per-request, and does NOT know or care how the token
  holder logged in.
- **Postgres**: stores real user records (Module 12 onward) and the mission service's own
  business data — two genuinely separate concerns, not one shared table doing both jobs.

## Talking points for facilitators

- The most common mistake in this sketch: an arrow from the mission service back to the auth
  service on every protected request ("check if the token is valid with the auth service"). This
  is the request-driven pattern Sprint 7, Module 3 already taught as the wrong default when an
  event-driven or self-verifying alternative exists — worth connecting explicitly if a pair drew
  that arrow.
- A second common gap: treating `401` and `403` as interchangeable. They're not — `401` means
  "I don't know who you are," `403` means "I know who you are, and the answer is no." Getting
  this distinction right here sets up Module 13's real JWT validation guard correctly.
