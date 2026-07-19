# Module 14 Demo Guide — Securing & Testing the Service: Lightweight Pass

**Duration:** 10 minutes
**Prerequisite:** Module 13's `AuthService` (register/login/refresh, bcrypt, JWT
issuance) — this module adds nothing new to it except one log line and a test suite.

This module is deliberately narrow. It is NOT an OWASP-style security review and NOT a
full testing-patterns module — it's an awareness-level pass over two pitfalls, plus one
real, focused Jest suite. Say that explicitly to the class: the goal is confidence, not
completeness.

## Part 1: Two Security Pitfalls, at Awareness Level (4 min)

```bash
npm run pitfalls-demo
```

Verified real output:

```
--- 1. The pitfall: logging the whole request body ---
login attempt: { username: 'alice', password: 'mission123' }

--- 2. The fix: log the event and username only ---
[auth] login_attempt username=alice

--- 3. The other half of 'weak secrets': a hardcoded fallback ---
JWT_SECRET in use:                mission-control-shared-secret-key-32-bytes-minimum
Was JWT_SECRET set via env var?   false
```

**Pitfall 1: token/credential leakage through logs.** Section 1's output is the
single most common real-world mistake in this space: logging an entire request or
response object "for debugging" without noticing it contains a password. Logs
routinely live longer, get replicated to more places (aggregators, support
dashboards, third-party monitoring tools), and are read by more people than the
database itself — so anything logged is effectively leaked more broadly than a
database breach alone. Section 2's `logAuthEvent(event, username)` fixes this
structurally, not by discipline: its signature has no parameter for a password or a
token, so there's nothing to accidentally pass through, even under deadline pressure.

**Pitfall 2: weak or hardcoded secrets.** Section 3 points directly at
`auth.service.ts`'s own `JWT_SECRET` line, already on screen from Module 13:

```typescript
export const JWT_SECRET = process.env.JWT_SECRET || "mission-control-shared-secret-key-32-bytes-minimum";
```

`Was JWT_SECRET set via env var? false` is the demo's whole point: right now, in this
training environment, the fallback string IS the secret in active use. That's fine for
a classroom. In a real deployment, forgetting to set `JWT_SECRET` in production
config is a genuinely common real-world incident report — the service starts up fine,
looks like it's working, and is quietly signing every token with a string anyone can
read directly from the source code.

## Part 2: Writing the Jest Suite (6 min)

```bash
npm test
```

Verified real output:

```
console.log
    [auth] login_success username=carol

      at logAuthEvent (src/logger.ts:7:11)

  console.log
    [auth] login_success username=carol

      at logAuthEvent (src/logger.ts:7:11)

Test Suites: 1 passed, 1 total
Tests:       3 passed, 3 total
```

Walk through `src/auth.service.spec.ts` live, one test at a time:

```typescript
it("logs in and receives a valid access token and refresh token", async () => {
  await service.register("carol", "mission123", ["MISSION_OPERATOR"]);
  const { accessToken, refreshToken } = await service.login("carol", "mission123");
  expect(typeof accessToken).toBe("string");
  expect(typeof refreshToken).toBe("string");
  expect(accessToken).not.toEqual(refreshToken);
});
```

**The login happy path.** `new AuthService()` in `beforeEach` gives every test a
fresh, isolated instance — no shared state, no test ordering dependencies. Note there
is no NestJS `TestingModule` here: `AuthService` has no constructor dependencies, so
`new AuthService()` is simpler and just as valid. Point out to the class that reaching
for NestJS's full dependency-injection testing machinery when a plain constructor call
works is over-engineering a lightweight pass.

```typescript
it("issues an access token that validates and carries the right claims", async () => {
  await service.register("carol", "mission123", ["MISSION_OPERATOR"]);
  const { accessToken } = await service.login("carol", "mission123");
  const decoded = jwt.verify(accessToken, JWT_SECRET) as jwt.JwtPayload;
  expect(decoded.sub).toBe("carol");
  expect(decoded.roles).toEqual(["MISSION_OPERATOR"]);
});
```

**The token-validation happy path.** This is the second explicit outline requirement,
distinct from the first test: it doesn't just check that a token exists, it actually
validates the signature via `jwt.verify` (the exact call Module 13's demo used) and
checks the payload's claims. `JWT_SECRET` is exported from `auth.service.ts`
specifically so this test can do that without duplicating the secret.

```typescript
it("rejects login with an incorrect password", async () => {
  await service.register("carol", "mission123", ["MISSION_OPERATOR"]);
  await expect(service.login("carol", "wrong-password")).rejects.toThrow();
});
```

**The one failure case.** `expect(promise).rejects.toThrow()` is Jest's idiom for an
`async` function that should reject — worth contrasting briefly with JUnit's
`assertThrows` from Sprint 5 if anyone asks how this compares.

## Key message

A lightweight security-and-testing pass isn't a lesser version of a full review — it's
a deliberately scoped one: fix the two pitfalls that bite hardest in practice
(credential leakage in logs, weak secrets), and prove the core paths work with a small,
real Jest suite, rather than chasing exhaustive coverage this late in the sprint.

## Transition to the Lab

Learners are given the same working `AuthService` and a `auth.service.spec.ts` with
three tests, each currently throwing a `TODO n: not implemented` error. They complete
all three tests following this demo's exact patterns, then add ONE `logAuthEvent` call
inside `login` itself — verified by re-running `npm test` and seeing all three tests
pass plus the log line print.
