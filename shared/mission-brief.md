# Sprint 8 Mission: Retiring the Stub

Since Sprint 6, Module 9, the mission service (Spring Boot) has trusted JWTs signed by
`shared/auth-stub` — a deliberately minimal Express server with two hardcoded users and one
`/login` endpoint. It did its job: it let the mission service's `SecurityConfig` be built and
tested against something real, without the class needing its own identity system yet.

Sprint 8 replaces it for real. `sprint8-auth-service`, a NestJS application, becomes the actual
identity provider: real user registration, real password hashing, real database-backed lookups
against the Sprint 3 Postgres schema, and JWTs issued and validated the same way the stub's were
— same claims shape, same shared-secret trust model — so the mission service's `SecurityConfig`
from Sprint 6 needs **zero changes** to accept tokens from the new service.

## What Changes, and What Doesn't

**Doesn't change:**
- The mission service's `SecurityConfig` (Sprint 6, Module 9) — it validates a JWT's signature
  against a shared secret; it has never cared which service issued the token, only that it's
  signed correctly
- The Sprint 3 Postgres schema — extended with a `users` table, not replaced
- The mission service's business logic (Sprint 5/6/7) — completely untouched

**Changes:**
- `shared/auth-stub` (two hardcoded users, no real password checking) is replaced by
  `sprint8-auth-service` (real registration, real bcrypt/argon2 hashing, real Postgres lookups)
- Login now issues a token backed by a genuine credential check, not a hardcoded string match
- The auth service gets its own OpenAPI-documented contract (Module 10), continuing Sprint 7's
  contract-first pattern into a second language and framework

## Why NestJS, and Why This Sprint Assumes No Prior JavaScript/TypeScript

Nobody on this cohort has written JavaScript or TypeScript yet. Days 1–2 build that foundation
from zero — plain JavaScript first (Modules 2–4), then TypeScript on top of it (Modules 5–7) —
before Node and NestJS are introduced at all (Module 8 onward). This is a genuine, deliberate
two-day investment, not a skipped step: everything from Module 8 onward assumes the vocabulary
and mental models Days 1–2 built, the same way Sprint 6 assumed Java from Sprint 1–5.

## Non-Goals

No changes to the mission service's business rules, its persistence layer, or its container
setup. This sprint is entirely about what issues the tokens the mission service already knows
how to check — not about anything the mission service itself does with them.
