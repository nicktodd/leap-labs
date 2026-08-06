# Module 13 Lab — Mission Build: Containerise, Integration Test & Wrap-up

This is the last technical lab of Sprint 6. It has two parts: finishing the integration test
script, and a short written wrap-up.

## Objectives

By the end of this lab you will have:

- Completed an end-to-end integration test that builds and runs BOTH the mission service and the
  Node auth stub as containers, alongside Postgres, and proves a real authenticated request works
  across all three
- Reflected on the sprint as a whole — which design decisions from Days 1-2 survived unchanged
  into the finished service, and which changed once persistence, security, and error handling
  were wired in

## Setup

- Access to your Linux Docker host — connect in your preferred way (see Sprint 1 Module 3) —
  with Java 21, Maven, and Node.js installed
- The Sprint 3 Postgres container running: `docker start sprint6-postgres`
- Given, don't modify: everything under `src/` (Module 11's assembled service), `Dockerfile`
  (Module 12's), and `shared/auth-stub/Dockerfile` (containerising the auth stub itself, given —
  not part of this kata)

## Part 1 — Complete the Integration Test

`integration-test.sh` has the network/build/run staging already written (Module 12's mechanics).
Six `TODO`s remain, covering the actual verification:

1. **Wait for both containers** to be ready — a retry loop against the auth stub's `/health` and
   the mission service's `/accounts/1/orders`.
2. **Smoke test**: a request with no token must return `401`.
3. **End-to-end**: a real token from the *containerised* auth stub, used to submit a real order to
   the *containerised* mission service, must succeed.
4. **Confirm**: query Postgres directly to prove the order actually persisted — not just that the
   HTTP response claimed success.

Each currently-stubbed stage exits with an error if you run the script without implementing it —
that's deliberate, so an untouched script can't silently report success.

### Verify

```bash
chmod +x integration-test.sh
./integration-test.sh
```

Every stage should print `PASS`, ending with `== ALL STAGES PASSED ==`.

## Part 2 — Sprint Wrap-up (Written)

Sprint 5's Module 14 asked you to trace design decisions from a first draft through to what you
actually built. Sprint 6's mission brief asked the same question in its Non-Goals section. Answer
it now, in **3-5 sentences per point**:

1. **Pick one design decision from Module 4's REST design or Module 5's OpenAPI spec.** Did it
   survive unchanged into Module 11's assembled service? If it changed, what forced the change —
   persistence (M7), security (M9), or error handling (M10)?
2. **The mission brief's "What Changes, and What Doesn't" section** claimed Sprint 5's business
   logic wouldn't need rewriting. Was that true? Point at the actual file (`domain/OrderValidator`
   or similar) as evidence.
3. **Name the one deliberate simplification** Module 11 made (portfolio valuation) and explain,
   in your own words, why it was a reasonable trade-off for a training sprint rather than a
   shortcut you'd ship to production unmentioned.

## Deliverable

`integration-test.sh`, fully implemented and passing, plus your three written answers.

## Acceptance criteria

- `./integration-test.sh` exits `0` and prints `== ALL STAGES PASSED ==`
- All three wrap-up answers reference specific modules or files, not general impressions
