# Module 5 Demo Guide — The Full Stack So Far & Where Angular Fits

**Duration:** 10 minutes
**Prerequisite:** `sprint6-postgres` running with the Sprint 3 schema, Sprint 6/7's mission
service, and Sprint 8's `sprint8-auth-service`. Modules 1-4 (HTML, CSS, DOM, Fetch)
complete — this module assumes their static page and its `fetch()` call to
`sprint8-auth-service` already exist.

This module introduces no new code and no new service. Say that explicitly: the whole
point is closing out Day 1 by proving the three boxes behind what learners just built
by hand — Postgres, the mission service, the auth service — already work, together, for
real, and then naming exactly what Angular is about to take over from Modules 1-4's
manual HTML/CSS/JS.

## From M4's fetch() to the Whole Stack (10 min)

Module 4's lab called `sprint8-auth-service`'s real `/auth/login` with `fetch()` and
rendered the token (or a rejected-login message) into the DOM by hand. That was one
hop of a much longer chain. Today's demo runs the WHOLE chain, live:

```bash
# No token
curl -X POST http://localhost:8081/accounts/1/orders \
  -H "Content-Type: application/json" \
  -d '{"ticker":"ULVR.L","instrumentType":"EQUITY","quantity":1,"price":40.0,"side":"BUY"}'
```

Verified real output:

```
401
```

```bash
# Login - Sprint 8's real auth service, not a stub
curl -X POST http://localhost:3000/auth/login -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"mission123"}'
```

Verified real output:

```
{"accessToken":"eyJhbGciOiJIUzI1NiIs...","refreshToken":"38dc6b8fdf80bb9b..."}
```

```bash
# That token, against the real Spring Boot mission service
curl -H "Authorization: Bearer $TOKEN" -X POST http://localhost:8081/accounts/1/orders \
  -H "Content-Type: application/json" \
  -d '{"ticker":"ULVR.L","instrumentType":"EQUITY","quantity":1,"price":40.0,"side":"BUY"}'
```

Verified real output:

```
{"status":"ACCEPTED","fee":0.04,"newHoldingQuantity":502.0}
```

```bash
# Not just trusting the HTTP response
docker exec sprint6-postgres psql -U postgres -d mission -c \
  "SELECT h.account_id, i.ticker, h.quantity FROM holdings h JOIN instruments i ON h.instrument_id=i.instrument_id WHERE h.account_id=1 AND i.ticker='ULVR.L';"
```

Verified real output:

```
 account_id | ticker | quantity
------------+--------+----------
          1 | ULVR.L |  502.0000
```

**Land the point**: every one of these four steps is real — a real Postgres row, a real
signed JWT, a real Spring Boot security filter. Nothing here is a mock, a stub, or a
diagram. The ONLY thing standing between this working system and something a trader
could actually use is a UI. That gap is what Sprint 9 closes.

## Where Angular Fits

Draw the picture live: **Browser → Angular app → sprint8-auth-service → mission service
→ Postgres**, then walk backward through what already exists at each box:

- **Postgres**: Sprint 3. Untouched since.
- **Mission service**: Sprint 5/6/7. Untouched since Sprint 6, Module 13.
- **sprint8-auth-service**: Sprint 8. Untouched since Sprint 8, Module 15.
- **The Angular app**: doesn't exist. Modules 1-4's static page, hand-written CSS, and
  manual DOM/`fetch()` code are the only "front end" that exists right now.

Name specifically what Angular replaces, module by module: components and signals
replace M3's manual `document.querySelector`/DOM-update code (Module 8); services and
`HttpClient` replace M4's raw `fetch()` call (Modules 9-10); an OpenAPI-generated client
replaces a hand-written HTTP call entirely (Module 12); reactive forms replace M1's
plain HTML form (Module 13); routing gives the app more than one screen (Module 14);
and Module 15 rebuilds this exact login-then-protected-request sequence — the same
sequence M4 already did by hand once — as real, running Angular code, with an
interceptor and a guard doing automatically what a learner would otherwise have to
remember to do on every request.

## Key message

Nothing in this stack is aspirational. Every claim in `shared/mission-brief.md` about
what already works is one this demo just proved, live, with real output — and M1-M4
already proved a browser CAN talk to it, by hand. Angular's job for the rest of this
sprint is narrower and more concrete because of that: replace hand-written HTML, CSS,
and `fetch()` calls with something that scales past one page and one request, not
build something new and hope it works.

## Transition to the Lab

In pairs, learners trace this same four-step flow themselves on a whiteboard, adding
the Angular app as a fifth box and working out exactly what it sends and receives at
each hop — before writing a single line of Angular code.
