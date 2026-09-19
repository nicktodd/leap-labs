# Lab 11: Building the Auth Service Skeleton — Login, Register, Refresh

## Setup

```bash
npm install
```

## Task

`login`, `register`, and `refresh` are given, complete, unchanged — the exact demo
implementation, preloaded with `dave` / `mission123` instead of `alice`. Two TODOs
add a fourth endpoint, `POST /auth/logout`:

1. **`auth.service.ts`** — implement `logout(refreshToken)`. Use the given
   `findByRefreshToken` helper to find the user holding that token, set their
   `refreshToken` back to `null` (so it can never be used again), and return
   `{ loggedOut: true }`. If no user holds that token, throw the same
   `UnauthorizedException` `refresh()` throws.
2. **`auth.controller.ts`** — add the `POST /auth/logout` route itself, following
   `refresh()`'s exact shape.

Build and run this now, before changing anything:

```bash
npm run build
npm run start
```

```bash
curl -X POST http://localhost:3000/auth/login -H "Content-Type: application/json" \
  -d '{"username":"dave","password":"mission123"}'
```

```
{"accessToken":"stub-access-token-for-dave-...","refreshToken":"stub-refresh-token-for-dave-..."}
```

```bash
curl -X POST http://localhost:3000/auth/logout -H "Content-Type: application/json" \
  -d '{"refreshToken":"anything"}'
```

```
{"message":"Cannot POST /auth/logout","error":"Not Found","statusCode":404}
```

That 404 is TODO 2 — the route doesn't exist yet.

## Expected Behavior (once both TODOs are done)

```bash
# Log in, keep the real refreshToken from the response
curl -X POST http://localhost:3000/auth/login -H "Content-Type: application/json" \
  -d '{"username":"dave","password":"mission123"}'

# Log out with that exact token
curl -X POST http://localhost:3000/auth/logout -H "Content-Type: application/json" \
  -d '{"refreshToken":"<paste the real refreshToken here>"}'
```

```
{"loggedOut":true}
```

Then try to use that SAME refresh token again:

```bash
curl -X POST http://localhost:3000/auth/refresh -H "Content-Type: application/json" \
  -d '{"refreshToken":"<the same token>"}'
```

```
{"message":"invalid or expired refresh token","error":"Unauthorized","statusCode":401}
```

## A Question Worth Sitting With

This skeleton stores exactly one refresh token per user (`refreshToken: string |
null`), so a second `login` silently overwrites the first — logging in on a phone,
then a laptop, invalidates the phone's session. Is that a bug in this skeleton, or a
reasonable real-world trade-off some systems make on purpose? What would need to
change to support multiple active sessions per user?
