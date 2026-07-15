# Lab 10 Model Answers

## Verified Output

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

## Key Points

- **TODO 1**: `@IsEmail()` from `class-validator` is the decorator for email format —
  `@IsString()` alone would accept `"not-an-email"` since it IS a string, just not a
  valid email address. Both checks are needed together on most fields; `@IsEmail()`
  happens to imply "is a string" on its own.
- **TODO 2**: same pattern as Module 9's lab — both `RegisterController` (so the route
  exists) and `RegisterService` (so the controller's constructor injection resolves)
  need to be added.

## The Reflection Question

```bash
curl -X POST http://localhost:3000/register -H "Content-Type: application/json" \
  -d '{"username":"grace","password":"secret123","email":"grace@example.com","isAdmin":true}'
```

Verified real result:

```
{"message":["property isAdmin should not exist"],"error":"Bad Request","statusCode":400}
```

The whole request is rejected — `forbidNonWhitelisted: true` refuses to silently drop
`isAdmin`, it refuses the request outright. This matters far more for `/register` than
for a read-only `GET` endpoint because a WRITE endpoint's body can attempt to set
fields the client should never control. `isAdmin` is the textbook example — a
real attacker sending exactly this payload against a real registration endpoint is
attempting a **mass assignment** attack: hoping the server blindly accepts and stores
every field in the request body, including ones granting elevated privilege. A
`GET` endpoint has no body to smuggle a field into in the first place, so
`forbidNonWhitelisted` is protecting something that specifically only exists on
write operations.
