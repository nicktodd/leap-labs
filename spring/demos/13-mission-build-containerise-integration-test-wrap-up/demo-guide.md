# Module 13 Demo Guide - Mission Build: Containerise, Integration Test & Wrap-up

The week's last piece: for the first time, the Node auth stub gets containerised too, and both
services run alongside Postgres with nothing hardcoded to `localhost`.

## Run the Whole Thing

```bash
chmod +x integration-test.sh
./integration-test.sh
```

Watch the staged output - it's deliberately structured like the Jenkinsfiles from the Foundations and Pipelines weeks:
`Network`, `Build Images`, `Run Containers`, `Wait`, `Smoke Test`, `End-to-End`, `Confirm`,
`Teardown`. Each stage either passes cleanly or fails loudly - no silent partial success.

## Point at the Auth Stub's Dockerfile

Open `shared/auth-stub/Dockerfile`.

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package.json .
RUN npm install --omit=dev
COPY server.js .
EXPOSE 4000
CMD ["node", "server.js"]
```

Single-stage - unlike the Java Dockerfile, there's no separate "compile" step for Node, nothing
to discard between a build stage and a runtime stage. But the same *caching* idea from Module 12
still applies: `package.json` copied and `npm install` run before `server.js` is copied, so a
change to the auth stub's logic doesn't force a full dependency reinstall.

## The Real Point: A Genuine Three-Service Integration Test

Point at the moment the script gets a token from `localhost:$AUTH_PORT` (the *containerised* auth
stub, reached through its published port) and uses it against `localhost:$SERVICE_PORT` (the
*containerised* mission service). **Neither container knows about the other's existence at the
network level in this test** - the test process on the host is the only thing that talks to both.
That's intentional: it's the same principle Module 9 and Module 12 already established (the
mission service never calls the auth service directly), now demonstrated with both sides actually
running in containers instead of one on the host.

Then point at the very last verification step - the direct `psql` query against
`missionservice-postgres`. **This is the step that actually matters.** The HTTP response claiming
`"status":"ACCEPTED"` is what a client would see; querying the database directly is what proves
the write really happened, independent of whether the response body might be lying (a bug that
returns success without actually persisting is a real, if rare, category of bug this step would
catch and the HTTP check alone would not).

## Wrap-up: What Actually Held Up

This is a good moment to walk the group back through the arc of the week, module by module, and
ask: **which piece never had to change once it was integrated?**

- The Java week's `OrderValidator`, `HoldingUpdater`, fee hierarchy (Module 11) - unchanged
- Module 7's `AccountMapper` queries - used as-is by Module 11
- Module 9's `SecurityConfig` - used as-is by Modules 11 and 12
- Module 10's `GlobalExceptionHandler` - used as-is by Module 11

**None of that was luck.** Each of those modules was built and *verified independently* before
being assembled - the actual argument for building software this way, not a coincidence of how
this course happened to be sequenced.

## Transition to the Lab

Learners complete the same integration test script from six `TODO`s, then write three short,
specific answers tracing design decisions across the week - the same reflective exercise the Java week's
Module 14 asked for, adapted to this week's own arc.
