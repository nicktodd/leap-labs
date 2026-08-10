# Lab 1 — Auth Request Flow

## Scenario A — First-time login

```
Client                  Auth Service              Postgres
  |                          |                        |
  |-- POST /auth/login ------>|                        |
  |   {username, password}   |                        |
  |                          |-- SELECT user WHERE -->|
  |                          |   username=?           |
  |                          |<-- {hashedPassword} ---|
  |                          |                        |
  |                          | bcrypt.compare()       |
  |                          | (local check, no DB)   |
  |                          |                        |
  |<-- 200 { accessToken } --|
  |    JWT signed with       |
  |    secret key            |
```

1. Client sends `POST /auth/login` with `{ username, password }` in the body
2. Auth service looks up the user in Postgres, runs `bcrypt.compare()` on the password
3. The JWT contains: `sub` (user ID), `username`, `role`, `iat` (issued at), `exp` (expiry)
4. Client stores the token (memory or localStorage) and attaches it to future requests

## Scenario B — Using the token

```
Client                  Mission Service           Auth Service
  |                          |                        |
  |-- GET /accounts/1/orders->|                        |
  |   Authorization:         |                        |
  |   Bearer <token>         |                        |
  |                          | jwt.verify(token,      |
  |                          | secret)                |
  |                          | (local, NO call to --->X  NOT called)
  |                          | auth service)          |
  |                          |                        |
  |                          | Check role claim       |
  |                          | in token payload       |
  |                          |                        |
  |<-- 200 orders ------------|
```

1. Client sends the request with `Authorization: Bearer <token>` header
2. Mission service verifies the JWT signature locally using the shared secret — it does **not** call the auth service
3. Missing/invalid token → `401 Unauthorized` immediately (matches Sprint 6 demo)
4. Valid token but role is `GUEST` not `MISSION_OPERATOR` → `403 Forbidden` — the decision is made in mission service's `SecurityConfig` after the token is verified

## Component responsibilities

| Component | Responsible for | NOT responsible for |
|---|---|---|
| **Client** | Storing the token, attaching it to requests | Validating the token, checking roles |
| **Auth Service** | Verifying credentials, issuing JWTs | Protecting routes, checking what the user can do |
| **Mission Service** | Verifying JWT signature, enforcing role-based access | Calling auth service at request time, storing passwords |
| **Postgres** | Persisting user records and hashed passwords | Any request-time auth logic |

## Authentication vs Authorization

- **Authentication** (proving identity): steps in Scenario A — verifying password, issuing JWT
- **Authorization** (checking permission): steps in Scenario B — checking role claim in the token against the required role for the route
