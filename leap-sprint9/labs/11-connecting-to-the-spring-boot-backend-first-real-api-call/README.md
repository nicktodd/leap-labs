# Lab 11 — Connecting to the Spring Boot Backend: First Real API Call

## Setup

1. `sprint6-postgres` running (the same container used since Sprint 3/Sprint 8).
2. Sprint 6/7's mission service, running with CORS enabled for `http://localhost:4200` (add
   the `CorsConfigurationSource` bean from today's demo to `SecurityConfig.java` if your copy
   doesn't have it yet).
3. Sprint 8's `sprint8-auth-service`, running with CORS enabled for `http://localhost:4200`
   (Module 4's own fix — `app.enableCors({ origin: "http://localhost:4200" })` in `main.ts`).
4. Your `mission-ui` from Module 10, served on port 4200 specifically (`ng serve` defaults to
   this — don't override it with `--port` this time, since both backend services are
   configured to only allow that exact origin).

Confirm both backends work with `curl` before touching Angular — log in against the auth
service, then use that token against the mission service's `/accounts/1/orders`, exactly as
Module 5's whiteboard traced.

## Task

1. Generate a service and a component:

   ```bash
   ng generate service mission-api
   ng generate component place-order --standalone
   ```

2. In `mission-api.ts`, add `submitOrder(order: OrderRequest): void` that:
   - `POST`s to the auth service's `/auth/login` with `alice`/`mission123`.
   - Uses `switchMap` to chain a second `POST` to the mission service's
     `/accounts/1/orders`, attaching `Authorization: Bearer <token>` from the first call's
     response.
   - Uses `catchError` (Module 10's pattern, unchanged) to set an `error` signal and keep the
     stream alive with `of(null)`.
   - `.subscribe()`s and sets a `lastOrder` signal with the response on success.

3. In `PlaceOrder`, `inject(MissionApi)`, add a button that submits a fixed test order (any
   real ticker/quantity/price your Postgres schema has), and show `lastOrder()`/`error()` in
   the template.

4. Add `<app-place-order />` to `app.html`.

## Verify

1. Query Postgres directly for your test account's holding, **before** clicking anything:

   ```bash
   docker exec -e PGPASSWORD=mission sprint6-postgres psql -U postgres -d mission -c \
     "SELECT h.account_id, i.ticker, h.quantity FROM holdings h JOIN instruments i ON h.instrument_id=i.instrument_id WHERE h.account_id=1 AND i.ticker='ULVR.L';"
   ```

2. Click your submit button in the running app. A real `ACCEPTED` response (with a fee and
   a new holding quantity) should appear.

3. Run the exact same `psql` query again. The quantity should have changed by exactly the
   amount your test order submitted — not asserted, queried twice, same as today's demo.

4. Open DevTools' Network tab and find both real requests — the login `POST` and the order
   `POST` — confirm the second one's request headers actually carry the
   `Authorization: Bearer ...` header your code attached.

## A Question Worth Sitting With

`switchMap` was used here instead of two separate, sequential `.subscribe()` calls (subscribe
to the login, and inside that callback, subscribe to the order). Both approaches would
technically work. What does chaining with `switchMap` inside one `.pipe()` give you that
nested subscribes don't — think specifically about `catchError`, and whether it would still
catch an error from the *second* call if the two were nested instead of piped.

A second question: this lab hardcodes `alice`/`mission123` directly in `mission-api.ts`,
visible to anyone who reads the source. Given Module 4's reflection question about what's
safe to hardcode in front-end code, is this actually a problem here — and if so, why is it
acceptable for *this* module specifically, given what Module 15 is described as building?
