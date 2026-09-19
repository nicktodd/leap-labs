# Lab 15 — Mission Build: OpenAPI Docs & Replacing the Sprint 7 Stub

This is the last technical lab of Sprint 8. It has two parts: documenting the auth
service's contract, and proving it can replace the stub for real.

## Objectives

By the end of this lab you will have:

- Generated a live, browsable OpenAPI document for the auth service, continuing Sprint
  7's contract-first pattern into a second language and framework
- Completed an end-to-end integration test that proves a real token, issued by the
  NestJS auth service you have built since Module 8, authenticates a real, unmodified
  Spring Boot mission service route

## Setup

- Docker Desktop, Node.js, and a working checkout of your own Sprint 6/7 mission
  service (this lab does not include a copy of it - see `shared/mission-brief.md`)
- The Sprint 3 Postgres container running: `docker start sprint6-postgres`
- Given, don't modify: `auth.service.ts`, `health.controller.ts`, `app.module.ts`,
  `Dockerfile` (all unchanged since Module 14/12), and everything under your own
  mission service checkout

## Part 1 — Complete the OpenAPI Documentation

Three `TODO`s, all about decorators - no behaviour changes:

1. **TODO 1 (`login.dto.ts`, `register.dto.ts`)** — add `@ApiProperty(...)` above each
   field, with an `example` and a short `description`.
2. **TODO 2 (`auth.controller.ts`)** — add `@ApiTags("auth")` above the class, and
   `@ApiOperation`/`@ApiResponse` above each route.
3. **TODO 3 (`main.ts`)** — build a `DocumentBuilder`, call
   `SwaggerModule.createDocument`, then `SwaggerModule.setup("api", app, document)`.

Run this now, before changing anything:

```bash
npm install
npm run build && npm start
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000/api
```

`404` - Swagger isn't wired up yet. That's the starting point.

### Verify

Complete the three TODOs, then rebuild and restart:

```bash
npm run build && npm start
```

Open `http://localhost:3000/api` in a browser - both routes should be documented, with
examples and response codes, not just bare paths. `GET /health` should NOT appear
(`@ApiExcludeController` on `HealthController` keeps operational plumbing out of the
public contract).

## Part 2 — Complete the Integration Test

`integration-test.sh` has the network/image-build/container-run staging already
written (Sprint 6, Module 12/13's mechanics, reused). Four `TODO`s remain:

4. **Wait for both containers** to be ready - the same retry-loop shape as Sprint 6,
   Module 13, against the auth service's `/health` and the mission service's
   `/accounts/1/orders`.
5. **Smoke test**: a request with no token must return `401`.
6. **End-to-end**: log in against the *containerised* auth service, use the real token
   to submit a real order to the *containerised, completely unmodified* mission
   service.
7. **Confirm**: query Postgres directly to prove the order actually persisted.

Set `MISSION_SERVICE_DIR` to point at your own Sprint 6/7 checkout before running:

```bash
export MISSION_SERVICE_DIR=/path/to/your/sprint6-or-7/mission-service
chmod +x integration-test.sh
./integration-test.sh
```

Every stage should print `PASS`, ending with `== ALL STAGES PASSED ==`.

## The Point of This Lab

Nothing in your mission service changes. `SecurityConfig` validates a JWT's signature
against a shared secret - it has never cared which service issued the token. If this
script passes, you have proven the mission brief's central claim end to end, not just
read it.

## Deliverable

`main.ts`, `login.dto.ts`, `register.dto.ts`, and `auth.controller.ts` with OpenAPI
decorators added, plus `integration-test.sh`, fully implemented and passing.

## Acceptance criteria

- `http://localhost:3000/api` shows both routes, documented, with `/health` excluded
- `./integration-test.sh` exits `0` and prints `== ALL STAGES PASSED ==`
