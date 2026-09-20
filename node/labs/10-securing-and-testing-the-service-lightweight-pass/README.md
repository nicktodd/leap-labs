# Lab 10: Securing & Testing the Service - Lightweight Pass

## Setup

```bash
npm install
```

## Task

`auth.service.ts` is given and already works (it's Module 9's finished JWT-issuing
`AuthService`, unchanged). `auth.service.spec.ts` has three Jest tests, each ending in
a `throw` marking the TODO. Make all three pass:

1. **TODO 1 (`auth.service.spec.ts`)** - log in as `carol` with the correct password,
   then assert `accessToken` and `refreshToken` are both strings, and that they are
   **not** equal to each other.
2. **TODO 2 (`auth.service.spec.ts`)** - log in, then verify `accessToken` with
   `jwt.verify(accessToken, JWT_SECRET)` and assert the decoded payload's `sub` is
   `"carol"` and `roles` is `["MISSION_OPERATOR"]`.
3. **TODO 3 (`auth.service.spec.ts`)** - assert that
   `service.login("carol", "wrong-password")` rejects (hint:
   `expect(...).rejects.toThrow()`).
4. **TODO 4 (`auth.service.ts`, inside `login`)** - call
   `logAuthEvent("login_success", username)` right after the password check succeeds,
   before the function returns. Do **not** log the password or either token -
   `logAuthEvent`'s signature (in `logger.ts`) doesn't even accept them.

Run this now, before changing anything:

```bash
npm test
```

All three tests fail with `TODO n: not implemented` - that's the starting point.

## Expected Output (once all four TODOs are done)

```
console.log
    [auth] login_success username=carol

Test Suites: 1 passed, 1 total
Tests:       3 passed, 3 total
```

## A Question Worth Sitting With

Your `logAuthEvent` call only fires on a **successful** login. If you added a similar
call inside the `if (!user || !passwordMatches)` branch to log failed attempts too,
what one extra field would matter most to a real security team investigating a
credential-stuffing attack - and why doesn't this lightweight pass ask you to add it?
