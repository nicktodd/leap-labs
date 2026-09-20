# Lab 8: Secure DB Access & Password Hashing

## Setup

```bash
npm install
```

## Task

`register`/`login` are given, but store and compare passwords in PLAIN TEXT - Module
7's exact skeleton. Two TODOs migrate them to real bcrypt hashing:

1. **`auth.service.ts`, `register`** - import `bcrypt`, make `register` hash the
   password with `bcrypt.hash(password, SALT_ROUNDS)` before storing it. Rename the
   `StoredUser.password` field to `passwordHash` (and update every place that refers
   to it) so the field name honestly describes what it now holds.
2. **`auth.service.ts`, `login`** - use `bcrypt.compare(password, user.passwordHash)`
   instead of the `!==` comparison - a hash can never be compared directly against
   the plain-text password that produced it.

Run this now, before changing anything:

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

This WORKS - that's the trap. The starter is functionally correct and insecure at the
same time; nothing about the API response tells you passwords are stored in plain
text. Do both TODOs, rebuild, and confirm the exact same `curl` command still produces
the exact same shape of response - the whole point of this migration is that the
external behavior doesn't change at all.

## Expected Output (once both TODOs are done - identical to before)

```
{"accessToken":"stub-access-token-for-dave-...","refreshToken":"stub-refresh-token-for-dave-..."}
```

## A Question Worth Sitting With

Before your fix, run this in a Node REPL (or a scratch script) using your OWN
`register`/`login` code:

```javascript
// Register the same password twice, under two different usernames
```

Compare the two stored `passwordHash` values for two users who register with the
IDENTICAL password. Are they the same string or different? Why does that answer
matter for a real system where a data breach exposes the whole user table?
