# Week 6 Mission: Retiring the Stub

Since Week 4, Module 9, the mission service (Spring Boot) has trusted JWTs signed by
`shared/auth-stub` - a deliberately minimal Express server with two hardcoded users and one
`/login` endpoint. It did its job: it let the mission service's `SecurityConfig` be built and
tested against something real, without the class needing its own identity system yet.

Week 6 replaces it for real. `sprint8-auth-service`, a NestJS application, becomes the actual
identity provider: real user registration, real password hashing, real database-backed lookups
against the Week 2 Postgres schema, and JWTs issued and validated the same way the stub's were
- same claims shape, same shared-secret trust model - so the mission service's `SecurityConfig`
from Week 4 needs **zero changes** to accept tokens from the new service.

## What Changes, and What Doesn't

**Doesn't change:**
- The mission service's `SecurityConfig` (Week 4, Module 9) - it validates a JWT's signature
  against a shared secret; it has never cared which service issued the token, only that it's
  signed correctly
- The Week 2 Postgres schema - extended with a `users` table, not replaced
- The mission service's business logic (Weeks 3 and 4) - completely untouched

**Changes:**
- `shared/auth-stub` (two hardcoded users, no real password checking) is replaced by
  `sprint8-auth-service` (real registration, real bcrypt/argon2 hashing, real Postgres lookups)
- Login now issues a token backed by a genuine credential check, not a hardcoded string match
- The auth service gets its own OpenAPI-documented contract (Module 11), continuing Week 4's
  contract-first pattern into a second language and framework

## Why NestJS, and What This Week Builds On

The Angular week (Week 5) already introduced JavaScript and TypeScript. This week builds on that
foundation: asynchronous JavaScript (Module 2), Node.js itself (Module 3) and the TypeScript
build process (Module 4) come first, before NestJS is introduced (Module 5 onward), the same way
Week 4 built on the Java from Week 3.

## Non-Goals

No changes to the mission service's business rules, its persistence layer, or its container
setup. This week is entirely about what issues the tokens the mission service already knows
how to check - not about anything the mission service itself does with them.
