# Module 8 Demo Guide - Secure DB Access & Password Hashing

Module 7's skeleton flagged two gaps explicitly. This module closes the first one:
plain-text passwords. It also covers the OTHER half of "secure DB access" - how a
database is QUERIED matters as much as how data is STORED in it, demonstrated with a
real, working SQL injection.

## Part 1: A Real SQL Injection

```bash
node sql-injection-demo.mjs
```

This runs against a REAL SQLite database (in-memory, no server needed) - not a
simulation. A vulnerable query, built by concatenating a string:

```javascript
function findUserUnsafe(username) {
  const sql = `SELECT * FROM users WHERE username = '${username}'`;
  return db.prepare(sql).all();
}
```

Verified real output for a normal lookup:

```
Executing: SELECT * FROM users WHERE username = 'alice'
[ { username: 'alice', password: 'mission123' } ]
```

Now a malicious username - not a made-up example, a REAL SQL injection payload that
closes the quote early and adds a condition that's always true:

```javascript
const maliciousInput = "x' OR '1'='1";
findUserUnsafe(maliciousInput);
```

Verified real output:

```
Executing: SELECT * FROM users WHERE username = 'x' OR '1'='1'
[
  { username: 'alice', password: 'mission123' },
  { username: 'bob', password: 'wrongpermissions' }
]
```

**Every user in the table came back** - including their passwords - from a query that
was only ever supposed to look up one specific username. The injected `OR '1'='1'`
turned the `WHERE` clause into something that matches every row.

The fix - a **parameterized query**:

```javascript
function findUserSafe(username) {
  return db.prepare("SELECT * FROM users WHERE username = ?").all(username);
}
```

Verified real output, same malicious input:

```
[]
```

Empty - correctly treated as "no user literally named `x' OR '1'='1'`", because the
`?` placeholder is never interpreted as SQL syntax, only ever as a single data value.
**Compare to Java:** this is exactly why `PreparedStatement` exists instead of
`Statement` with string-built SQL - same vulnerability, same fix, same reason.

## Part 2: Real Password Hashing with bcrypt

Module 7's `AuthService` stored `password: "mission123"` directly. This module
replaces it:

```typescript
async register(username: string, password: string) {
  const passwordHash = await bcrypt.hash(password, SALT_ROUNDS);
  this.users.set(username, { passwordHash, refreshToken: null });
  return { username, registered: true };
}

async login(username: string, password: string) {
  const user = this.users.get(username);
  const passwordMatches = user ? await bcrypt.compare(password, user.passwordHash) : false;
  if (!user || !passwordMatches) {
    throw new UnauthorizedException("invalid username or password");
  }
  // ...
}
```

`bcrypt.hash` generates a random **salt** internally and folds it into the result -
verified real output, hashing the SAME password twice:

```
hash 1: $2b$10$LO5/.um2t/lkK./f6P4h7uVIJVpfbxFCiR8gbF/R/xvDG3.q.cH4S
hash 2: $2b$10$i9DCNkBmYDEk/b9jD4viCOu568cBpZMXDPIOB9fD.r9FaeJNYwF8K
different: true
```

Two calls, same input, completely different output - this is what stops two users
who happen to choose the same password from having identical rows in a database, which
would otherwise leak "these two accounts share a password" even without ever cracking
either hash.

`bcrypt.compare` doesn't reverse the hash - there's no way to. It re-hashes the
SUBMITTED password using the SAME salt embedded in the stored hash, then compares the
two resulting hashes:

```
compare h1 vs mission123: true
compare h2 vs mission123: true
```

Both hashes correctly verify against the same original password, despite being
different strings - the salt is stored INSIDE the hash string itself (`$2b$10$...`),
not separately.

**Never write your own hashing/salting scheme.** `bcrypt` (and its relatives, `argon2`,
`scrypt`) exist specifically because getting this right by hand is a genuinely hard
cryptography problem, not a five-line function.

## Part 3: Verified End to End

```bash
curl -X POST http://localhost:3000/auth/login -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"mission123"}'
```

```
{"accessToken":"stub-access-token-for-alice-8jxu8hrz","refreshToken":"stub-refresh-token-for-alice-rdi9egi9"}
```

Nothing about this response is any different from Module 7's - that's the point.
The API contract hasn't changed at all; only what happens INSIDE `login` and
`register` has. Wrong password, register-then-login for a new user - every flow
Module 7 already verified still behaves identically, now backed by real hashing.

## A Running Comparison

| Node/NestJS | Java |
|---|---|
| `bcrypt.hash(password, 10)` | Spring Security's `BCryptPasswordEncoder.encode(...)` |
| `bcrypt.compare(password, hash)` | `BCryptPasswordEncoder.matches(...)` |
| `db.prepare("... WHERE x = ?").all(value)` | `PreparedStatement` with `?` placeholders |
| String-concatenated SQL (vulnerable) | `Statement` with string-built SQL (same vulnerability) |

## Transition to the Lab

Learners take a plaintext-password `AuthService` (Module 7's exact skeleton) and
migrate it to real bcrypt hashing themselves - `register` hashing on the way in,
`login` comparing on the way out - verified against the exact same login/register
flows Module 7 already proved worked, now backed by real hashing instead of a
plaintext `Map`.
