# Lab 12 Model Answers

## Verified Output

```bash
curl -X POST http://localhost:3000/auth/login -H "Content-Type: application/json" \
  -d '{"username":"dave","password":"mission123"}'
```
```
{"accessToken":"stub-access-token-for-dave-7z0jy5ec","refreshToken":"stub-refresh-token-for-dave-ab172gqo"}
```

Identical shape to the plaintext starter's response — that's deliberate. The migration
only changes what happens INSIDE the service.

## Key Points

- **TODO 1**: `bcrypt.hash(password, SALT_ROUNDS)` must be `await`ed, which is why
  `register` needs `async` — it was already declared `async` in the starter, but the
  body needed the actual hashing call added. `passwordHash` replaces `password`
  everywhere `StoredUser` is referenced, including the `refresh`/`findByRefreshToken`
  logic that never touches passwords at all but shares the same interface.
- **TODO 2**: `bcrypt.compare(password, user.passwordHash)` returns a `Promise<boolean>`
  — `login` needs to `await` it before checking the result, not treat it as a
  synchronous boolean the way the `!==` check was.

## The Reflection Question

Two users registering with the identical password get DIFFERENT `passwordHash`
values — verified directly:

```
hash 1: $2b$10$LO5/.um2t/lkK./f6P4h7uVIJVpfbxFCiR8gbF/R/xvDG3.q.cH4S
hash 2: $2b$10$i9DCNkBmYDEk/b9jD4viCOu568cBpZMXDPIOB9fD.r9FaeJNYwF8K
```

This matters directly for a real data breach: if a stolen user table showed two users
with IDENTICAL hash values, an attacker instantly knows those two accounts share a
password, without ever cracking either hash — useful information for a "credential
stuffing" attack even before any hash is broken. Different salts (baked automatically
into each `bcrypt.hash` call) mean identical passwords never produce identical stored
values, closing that leak entirely, on top of making each individual hash itself hard
to reverse.
