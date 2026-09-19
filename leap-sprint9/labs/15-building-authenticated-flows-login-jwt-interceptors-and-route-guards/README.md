# Lab 15 — Building Authenticated Flows: Login, JWT Interceptors & Route Guards

## Setup

Your own `mission-ui` from Module 14. Same running backends as Modules 11-14 (mission
service, auth service, `sprint6-postgres`).

## Task

### Part 1: Where the token lives

1. Generate a service: `ng generate service token-store`.
2. Give it a private `signal<string | null>` for the token and one for the username, an
   `isAuthenticated` computed, and `setToken()`/`getToken()`/`clear()` methods. Keep it
   in-memory only — no `localStorage`, no cookie.

### Part 2: The login form

3. Generate `ng generate service auth-api` with one method, `login(username, password)`,
   posting to the Sprint 8 auth service's `/auth/login` and returning the response.
4. Generate `ng generate component login-page --standalone`. Build a reactive form (Module
   13's pattern) with `username`/`password` fields. On submit, call `AuthApi.login()`; on
   success, call `TokenStore.setToken()` and navigate to `/holdings`; on failure, show an
   error message.

### Part 3: The interceptor

5. Generate `ng generate interceptor auth --functional`. Read the token from `TokenStore`,
   and if it's present *and* the request URL targets the mission service (not the auth
   service), clone the request with an `Authorization: Bearer <token>` header attached.
6. Register it: `provideHttpClient(withInterceptors([authInterceptor]))` in `app.config.ts`.
7. Remove any manual login/credential-setting code left over from Module 11/12 in
   `MissionApi` — the interceptor replaces it entirely.

### Part 4: The guard

8. Generate `ng generate guard auth --functional`. Return `true` if
   `TokenStore.isAuthenticated()`; otherwise navigate to `/login` and return `false`.
9. Add `canActivate: [authGuard]` to at least one route (both `/holdings` and `/orders` if
   you're following along with the demo).
10. Add a `/login` route (lazy-loaded, same as every other route this sprint).

## Verify

1. Visit a protected route directly, with nothing logged in yet. Confirm you land on
   `/login`, not a blank page.
2. Log in with valid credentials. Confirm the URL moves to the protected route.
3. Open DevTools' Network tab, submit a real order, and find the request to the mission
   service. Confirm its `Authorization` header is present — attached by the interceptor, not
   by any code in your component.
4. Query Postgres before and after, the same way every module since 11 has, to confirm the
   order actually landed.
5. Log out. Confirm you're returned to `/login`, and that visiting a protected route again
   redirects you back there — the guard is active again immediately.

## A Question Worth Sitting With

The interceptor checks `req.url.startsWith(MISSION_SERVICE_BASE)` before attaching the token.
What would go wrong — specifically, name the real request it would affect — if this check
were removed and the interceptor attached the header to every outgoing request unconditionally?

A second question: `TokenStore` holds the token in memory only, so a page refresh logs the
user out. What would need to change for a session to survive a refresh, and what new risk
would that change introduce that today's in-memory-only approach doesn't have?
