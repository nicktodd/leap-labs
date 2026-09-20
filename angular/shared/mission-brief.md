# This Week's Mission: Giving the Trading Platform a Face

Since the Spring week, the mission service (Spring Boot) has been fully real - persisted,
secured, containerised - but only reachable by `curl`, a REST client, or the Spring week's
own integration test script. Nobody has actually *seen* it work as an application yet.

This week builds `mission-ui`, an Angular application that is the next piece: a login screen
that authenticates against a small auth stub (`shared/auth-stub`, this week's own copy of the
same idea the Spring week used), and at least two working views that call the mission service
for real, through a real JWT that service already accepts unchanged.

The Node week, later in the programme, replaces this stub with a full, production-shaped
identity service in NestJS. Nothing here is written to look like a preview of that - it's a
small, honest stand-in that does exactly one job (issue a real JWT) so this week can focus on
Angular.

## What Changes, and What Doesn't

**Doesn't change:**
- The mission service's `SecurityConfig`, business logic, and persistence (from the Java and
  Spring weeks) - completely untouched
- The auth stub's login contract - the Angular app is simply its first real client
- The Data Systems week's Postgres schema - read and written via the mission service exactly
  as before, never queried directly from Angular

**Changes:**
- A real Angular application, `mission-ui`, replaces `curl` as how a person actually uses the
  mission
- Forms replace hand-typed JSON request bodies
- A JWT interceptor and route guard replace manually pasting a bearer token into every request

## Why Day 1 Is HTML/CSS/Browser JS, Not Angular

Nobody has touched HTML, CSS, or the browser yet at this point in the programme. Without a
day spent on the raw platform first, Module 8 (Components & Templates) would be the first
time anyone had touched an HTML tag or a stylesheet. Modules 1-4 build a static page, style
it, make it interactive, and call a real backend with `fetch()` - all by hand, no framework -
so that when Angular is introduced in Module 6, every abstraction it offers (components,
`HttpClient`, reactive forms) has something concrete to be an improvement *over*, not a new
set of ideas learned in a vacuum.

## Why Module 6 Opens With a TypeScript Primer

Nobody has seen TypeScript yet either - the Node week, where it's normally taught properly,
comes later in the programme now. Module 6 opens with a short, focused primer (types,
interfaces, classes, generics) before touching Angular at all, and everything after that
folds Angular-specific TypeScript usage (decorators, typed component properties, generics in
`HttpClient`) into the components and HTTP modules where it naturally comes up, rather than
teaching it as one long separate block. Module 15 combines the login form, the JWT
interceptor, and the route guard into one module rather than three, because a login form
without the interceptor and guard is non-functional - splitting them apart would mean testing
incomplete pieces at every step instead of one working flow.

## Non-Goals

No changes to the mission service's business rules, persistence layer, or security config.
Angular and its auth stub are the only new things this week; the mission service it talks to
already exists and already works.
