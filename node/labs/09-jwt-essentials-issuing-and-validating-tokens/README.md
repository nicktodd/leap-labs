# Lab 9: JWT Essentials - Issuing & Validating Tokens

## Setup

```bash
npm install
```

## Task

1. **TODO 1** - implement `issueToken(username, roles, expiresIn)` using
   `jwt.sign(...)`, matching the demo's exact call: payload
   `{ sub: username, roles }`, `algorithm: "HS256"`, and the given `expiresIn`.
2. **TODO 2** - implement `validateToken(token)` using `jwt.verify(token, SECRET)`,
   returning its result. Let errors propagate - don't catch them inside
   `validateToken` itself.

Run this now, before changing anything:

```bash
node report.mjs
```

It throws at TODO 1. That's the starting point.

## Expected Output (once both TODOs are done)

```
--- A normal token, issued and validated ---
{
  sub: 'dave',
  roles: [ 'MISSION_OPERATOR' ],
  iat: ...,
  exp: ...
}

--- An already-expired token ---
TokenExpiredError: jwt expired

--- A tampered token ---
JsonWebTokenError: invalid signature
```

(the `iat`/`exp` numbers will be different each run - that's expected, they're real
timestamps)

## A Question Worth Sitting With

`validateToken` is deliberately written to let `jwt.verify`'s errors propagate
unchanged, rather than catching them and returning something like `null` or
`{ valid: false }`. What would be lost if `validateToken` swallowed the error and
returned `null` on any failure - specifically, thinking back to the demo's THREE
different failure modes (tampered, wrong secret, expired), each with a different
named error?
