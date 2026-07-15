# Lab 10: DTOs & Validation in NestJS

## Setup

```bash
npm install
```

## Task

`VerificationController`/`VerificationService`/`VerifyCredentialsDto` are given,
complete, unchanged — the exact demo pair. `RegisterController`/`RegisterService` are
also given, complete. Two TODOs:

1. **`register.dto.ts`** — import and add `class-validator` decorators so
   `RegisterDto` enforces: `username` is a non-empty string, at least 3 characters;
   `password` is a string, at least 8 characters; `email` is a string AND a valid
   email address (there's a decorator specifically for this).
2. **`app.module.ts`** — add `RegisterController` to `controllers` and
   `RegisterService` to `providers`, alongside the `Verification` pieces already
   there.

Build and run this now, before changing anything:

```bash
npm run build
npm run start
```

```bash
curl -X POST http://localhost:3000/verify -H "Content-Type: application/json" \
  -d '{"username":"dave"}'
```

```
{"username":"dave","verified":true}
```

```bash
curl -X POST http://localhost:3000/register -H "Content-Type: application/json" \
  -d '{"username":"grace","password":"pw","email":"not-an-email"}'
```

```
{"message":"Cannot POST /register","error":"Not Found","statusCode":404}
```

That 404 is TODO 2 — the route isn't registered at all yet. Do TODO 2 first, rebuild,
and the request above should return a real validation error instead — with the
`password` and `email` problems both caught, once TODO 1 is also done.

## Expected Output (once both TODOs are done)

```bash
curl -X POST http://localhost:3000/register -H "Content-Type: application/json" \
  -d '{"username":"grace","password":"pw","email":"not-an-email"}'
```

```
{"message":["password must be longer than or equal to 8 characters","email must be
an email"],"error":"Bad Request","statusCode":400}
```

```bash
curl -X POST http://localhost:3000/register -H "Content-Type: application/json" \
  -d '{"username":"grace","password":"secret123","email":"grace@example.com"}'
```

```
{"username":"grace","email":"grace@example.com","registered":true}
```

## A Question Worth Sitting With

The global `ValidationPipe` in `main.ts` has `forbidNonWhitelisted: true`. Send a
`/register` request with a valid body PLUS an extra field like `"isAdmin": true`.
What's the real, verified result — and why does that specific behavior matter more
for a `/register` endpoint than it would for, say, a harmless `GET` endpoint that
just reads data?
