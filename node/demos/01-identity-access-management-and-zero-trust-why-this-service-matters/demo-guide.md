# Module 1 Demo Guide - Identity, Access Management & Zero-Trust: Why This Service Matters

No JavaScript yet today - this module is entirely conceptual, grounded in a system that already
exists and already works. The point is to see it working, understand exactly what it's currently
missing, and understand what this week replaces before writing a single line of code.

## Stand Up the Current System

The Spring week's fully containerised mission service + auth stub, run exactly as the Spring week left it:

```bash
cd ../../../spring/solutions/13-mission-build-containerise-integration-test-wrap-up
bash integration-test.sh
```

Verified real output:

```
== Stage: Smoke Test - No Token Is Rejected ==
PASS: unauthenticated request rejected (401)

== Stage: End-to-End Authenticated Order ==
Order response: {"status":"ACCEPTED","fee":0.04,"newHoldingQuantity":619.0}
PASS: real token from the containerised auth stub was accepted by the containerised mission service

== Stage: Confirm It Actually Landed in Postgres ==
 account_id | ticker | quantity
------------+--------+----------
          1 | ULVR.L | 619.0000
```

**Walk through what just happened, live:**

1. A request with no token to a protected mission-service endpoint was rejected - `401`, not a
   crash, not silently allowed. Point at this directly: rejection is the DEFAULT, not an
   afterthought.
2. A request to `shared/auth-stub`'s `/login`, with a username and password, returned a signed
   JWT.
3. That same token, attached to a request to the mission service, was accepted - and the order
   genuinely landed in Postgres, confirmed by a direct query, not just trusting the HTTP response.

## What's Actually Wrong With This Picture

Open `shared/auth-stub/server.js` together and read it aloud:

```javascript
const USERS = {
  alice: { password: 'mission123', roles: ['MISSION_OPERATOR'] },
  bob: { password: 'wrongpermissions', roles: ['GUEST'] },
};
```

Two hardcoded users. Plaintext passwords, visible in source code. No registration. No database.
This has worked, genuinely, across multiple weeks - because its only job was to prove `SecurityConfig`
could validate a real, signed token. It was never meant to be a real identity system, and it
isn't one.

## Identity & Access Management, Named

- **Authentication** - proving who you are (the `/login` call, checking a password)
- **Authorization** - what you're allowed to do once identified (the `roles` claim -
  `MISSION_OPERATOR` vs `GUEST` - is what the mission service actually checks per-endpoint)
- **A credential store** - where real usernames, real hashed passwords, and real roles actually
  live (today: a JavaScript object; by Module 8: a real Postgres table)

## Zero-Trust, Named

The mission service **never calls the auth service at request time.** It doesn't ask "is this
token still valid, right now?" - it checks the token's signature itself, using a secret both
services already agree on. This is worth stating precisely:

- **Old model ("castle and moat")**: once inside the network perimeter, a request is trusted.
- **Zero-trust**: nothing is trusted by default - including a request that's already "inside" -
  every request proves itself, every time, via a token whose signature can be checked without a
  network call back to whoever issued it.

This is *why* the mission service's `SecurityConfig` was built the way it was in the Spring week: not
because JWTs are trendy, but because verifying a signature locally is faster, doesn't create a
dependency on the auth service being up, and doesn't trust the network path in between.

## Transition to the Lab

In pairs, sketch how a request SHOULD flow from a client, through the real auth service this
week builds, to a protected mission-service route - before any of that code exists. The
sketch from today becomes the target Module 7 actually builds toward.
