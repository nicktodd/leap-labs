# Module 9 Demo Guide - The Full Stack So Far & Where Angular Fits

**Duration:** 10 minutes
**Prerequisite:** `missionservice-postgres` running with the Data Systems week's schema, the
Spring week's mission service, and this week's auth stub. Modules 1-8 (HTML, CSS,
JavaScript, TypeScript) complete - this module assumes their static page and its `fetch()` call to the auth
stub already exist.

This module introduces no new code and no new service. Say that explicitly: the whole
point is closing out this opening stretch by proving the three boxes behind what learners just built
by hand - Postgres, the mission service, the auth service - already work, together, for
real, and then naming exactly what Angular is about to take over from Modules 1-8's
manual HTML/CSS/JS/TypeScript.

## From M6's fetch() to the Whole Stack (10 min)

Module 6's lab called the auth stub's real `/auth/login` with `fetch()` and
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
# Login - this week's auth stub, a real signed JWT back
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
docker exec missionservice-postgres psql -U postgres -d mission -c \
  "SELECT h.account_id, i.ticker, h.quantity FROM holdings h JOIN instruments i ON h.instrument_id=i.instrument_id WHERE h.account_id=1 AND i.ticker='ULVR.L';"
```

Verified real output:

```
 account_id | ticker | quantity
------------+--------+----------
          1 | ULVR.L |  502.0000
```

**Land the point**: every one of these four steps is real - a real Postgres row, a real
signed JWT, a real Spring Boot security filter. The auth stub issuing that JWT is
deliberately small (the Node week later builds the production-shaped version), but the
token it produces and the way the mission service checks it are not a mock or a diagram.
The ONLY thing standing between this working system and something a trader could actually
use is a UI. That gap is what this week closes.

## Where Angular Fits

Draw the picture live: **Browser → Angular app → auth stub → mission service →
Postgres**, then walk backward through what already exists at each box:

- **Postgres**: from the Data Systems week. Untouched since.
- **Mission service**: from the Java and Spring weeks. Untouched since the Spring week,
  Module 13.
- **Auth stub**: built fresh for this week, this module's own Module 6 fix. It stays as-is
  for the rest of the week.
- **The Angular app**: doesn't exist. Modules 1-8's static page, hand-written CSS, and
  manual DOM/`fetch()`/typed code are the only "front end" that exists right now.

Name specifically what Angular replaces, module by module: components and signals
replace M5's manual `document.querySelector`/DOM-update code (Module 12); services and
`HttpClient` replace M6's raw `fetch()` call (Modules 13-14); an OpenAPI-generated client
replaces a hand-written HTTP call entirely (Module 16); reactive forms replace M1's
plain HTML form (Module 17); routing gives the app more than one screen (Module 18);
and Module 19 rebuilds this exact login-then-protected-request sequence - the same
sequence M6 already did by hand once - as real, running Angular code, with an
interceptor and a guard doing automatically what a learner would otherwise have to
remember to do on every request.

## Key message

Nothing in this stack is aspirational. Every claim in `shared/mission-brief.md` about
what already works is one this demo just proved, live, with real output - and M1-M6
already proved a browser CAN talk to it, by hand. Angular's job for the rest of this
week is narrower and more concrete because of that: replace hand-written HTML, CSS,
and `fetch()` calls with something that scales past one page and one request, not
build something new and hope it works.

## Transition to the Lab

In pairs, learners trace this same four-step flow themselves on a whiteboard, adding
the Angular app as a fifth box and working out exactly what it sends and receives at
each hop - before writing a single line of Angular code.
