# Sprint 9 Mission: Giving the Trading Platform a Face

Since Sprint 6, the mission service (Spring Boot) has been fully real — persisted, secured,
containerised — but only reachable by `curl`, a REST client, or Sprint 6's own integration
test script. Sprint 8 gave it a real identity provider. Nobody has actually *seen* it work
as an application yet.

Sprint 9 builds `mission-ui`, an Angular application that is the final piece: a login screen
that authenticates against Sprint 8's `sprint8-auth-service`, and at least two working views
that call the Sprint 6/7 mission service for real, through the exact JWTs Sprint 8 already
proved that service accepts unchanged.

## What Changes, and What Doesn't

**Doesn't change:**
- The mission service's `SecurityConfig`, business logic, and persistence (Sprint 5/6/7) —
  completely untouched
- `sprint8-auth-service`'s login/register/refresh contract (Sprint 8) — the Angular app is
  simply its first real client
- The Sprint 3 Postgres schema — read and written via the mission service exactly as before,
  never queried directly from Angular

**Changes:**
- A real Angular application, `mission-ui`, replaces `curl` as how a person actually uses the
  mission
- Forms replace hand-typed JSON request bodies
- A JWT interceptor and route guard replace manually pasting a bearer token into every request

## Why Day 1 Is HTML/CSS/Browser JS, Not Angular

Sprint 8 taught JavaScript and TypeScript entirely in a Node.js context — no HTML, no
CSS, no DOM, no browser. Without a day spent on the raw platform first, Module 8
(Components & Templates) would be the first time anyone had touched an HTML tag or a
stylesheet. Modules 1-4 build a static page, style it, make it interactive, and call a
real backend with `fetch()` — all by hand, no framework — so that when Angular is
introduced in Module 6, every abstraction it offers (components, `HttpClient`, reactive
forms) has something concrete to be an improvement *over*, not a new set of ideas
learned in a vacuum.

## Why No TypeScript Refresher

TypeScript was taught properly in Sprint 8, so this sprint doesn't re-teach it —
Angular-specific TypeScript usage (decorators, typed component properties, generics in
`HttpClient`) is folded into the components and HTTP modules where it naturally comes up,
rather than taught as a separate block. Module 15 combines the login form, the JWT
interceptor, and the route guard into one module rather than three, because a login form
without the interceptor and guard is non-functional — splitting them apart would mean
testing incomplete pieces at every step instead of one working flow.

## Non-Goals

No changes to the mission service's business rules, persistence layer, or security config.
No changes to the auth service's contract. Angular is the only new codebase this sprint;
everything it talks to already exists and already works.
