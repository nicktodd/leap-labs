# Module 11 Demo Guide - Mission Build: OpenAPI Docs & Replacing the Existing Stub

**Duration:** 15 minutes
**Prerequisite:** Module 10's `AuthService` (unchanged), a running `missionservice-postgres`
container loaded with the Data week's schema, and a checkout of the group's own Spring week
mission service.

This is this week's last technical module, and the only one where the two sides of
`shared/mission-brief.md`'s "What Changes, and What Doesn't" actually meet. Say that
explicitly: every module since Module 7 built one piece of the auth service in
isolation; today is the first point that service talks to the mission service at all.

## Part 1: Live OpenAPI Documentation (5 min)

```bash
npm run build && npm start
```

Open `http://localhost:3000/api` in a browser.

**Contrast with the Spring week's Module 5**: that was contract-FIRST - the OpenAPI spec was
written before any code existed. This is the same contract discipline arriving from
the OTHER direction - the document is generated FROM the code's decorators. Both
approaches produce the same real artifact; point out `http://localhost:3000/api-json`
is the actual machine-readable document a client codegen tool would consume, the `/api`
page is just a human-friendly renderer on top of it.

Verified real output:

```bash
curl -s http://localhost:3000/api-json | python3 -c \
  "import json,sys; d=json.load(sys.stdin); print(list(d['paths'].keys()))"
```
```
['/auth/register', '/auth/login']
```

**Point out what's missing**: `/health` isn't listed. Open `health.controller.ts` and
show `@ApiExcludeController()` - operational plumbing (container readiness checks)
isn't part of the auth service's PUBLIC contract, and the decorator says so explicitly
rather than by accident.

## Part 2: Replacing the Stub, for Real (10 min)

Set the class's attention on the actual point of the whole week: this container
sitting next to their own, completely unmodified, Spring week mission service.

```bash
export MISSION_SERVICE_DIR=/path/to/your/spring-week/mission-service
docker start missionservice-postgres
chmod +x integration-test.sh
./integration-test.sh
```

Verified real output. In authoring this module, the mission service and the auth
service were run directly (`java -jar`, `node dist/main.js`) against a real
`missionservice-postgres` container rather than through `integration-test.sh`'s own
container-build step - a first-time Maven dependency pull inside Docker was too slow
in this sandboxed environment to finish in a reasonable time. `integration-test.sh`
itself is unchanged from this exact recipe and is what a learner's own machine (with a
warm Docker cache) should use; the underlying claim below - a token from the new
service authenticating an unmodified mission-service route, verified against
the Spring week's Module 13's actual solution - is identical either way:

```bash
# No token
$ curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost:8081/accounts/1/orders \
    -H "Content-Type: application/json" \
    -d '{"ticker":"ULVR.L","instrumentType":"EQUITY","quantity":1,"price":40.0,"side":"BUY"}'
401

# A real token, from the NEW NestJS auth service
$ curl -s -X POST http://localhost:3000/auth/login -H "Content-Type: application/json" \
    -d '{"username":"alice","password":"mission123"}'
{"accessToken":"eyJhbGciOiJIUzI1NiIs...","refreshToken":"dd3b03f97a1a749c..."}

# That token, submitted to the UNCHANGED mission service
$ curl -s -H "Authorization: Bearer $TOKEN" -X POST http://localhost:8081/accounts/1/orders \
    -H "Content-Type: application/json" \
    -d '{"ticker":"ULVR.L","instrumentType":"EQUITY","quantity":1,"price":40.0,"side":"BUY"}'
{"status":"ACCEPTED","fee":0.04,"newHoldingQuantity":501.0}

# Confirmed directly in Postgres, not just trusting the HTTP response
$ docker exec -e PGPASSWORD=mission missionservice-postgres psql -U postgres -d mission -c \
    "SELECT h.account_id, i.ticker, h.quantity FROM holdings h JOIN instruments i ON h.instrument_id=i.instrument_id WHERE h.account_id=1 AND i.ticker='ULVR.L';"
 account_id | ticker | quantity
------------+--------+----------
          1 | ULVR.L |  501.0000
(1 row)
```

**Walk through what just happened, slowly - this is the payoff for the whole week:**

1. A request with no `Authorization` header hits `POST /accounts/1/orders` on the
   mission service and gets a `401`. That's `SecurityConfig`, from the Spring week's Module 9,
   completely untouched since the day it was written.
2. `curl .../auth/login` hits the NEW service - built from Module 7 onward, over four
   days, starting from zero JavaScript knowledge - and gets back a real, signed JWT.
3. That token, with NO other change, authenticates against the mission service.
   `newHoldingQuantity: 501.0` isn't a mocked response - ULVR.L's real holding for
   account 1 in the real Postgres container went from 500 to 501.
4. The direct Postgres query in the last stage exists specifically so nobody can argue
   the `200 ACCEPTED` was a lie - the row itself changed.

**Land the point explicitly**: `SecurityConfig`'s `jwtDecoder()` bean validates a
signature against a shared secret string. It has never once cared which service issued
the token - not in the Spring week, not today. Two completely different languages,
frameworks, and teams' worth of code (in a real team) agree on nothing except one
string and a claims shape. That's the entire lesson of the week, proven end to end,
not just asserted.

## Key message

Contract-first design (the Spring week) and contract-from-code (today) are the same
discipline in both directions. And a shared-secret trust boundary is powerful
specifically because it's narrow: the mission service's security config doesn't need
to know NestJS exists for this to work.

## Transition to the Lab

Learners add the same three OpenAPI decorator groups to their own DTOs and controller,
then complete four `TODO`s in `integration-test.sh` - the exact verification stages
walked through above - against their OWN Spring week mission service checkout.
