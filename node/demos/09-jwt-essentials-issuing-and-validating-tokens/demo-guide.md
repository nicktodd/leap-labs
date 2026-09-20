# Module 9 Demo Guide - JWT Essentials: Issuing & Validating Tokens

Module 7's skeleton flagged two gaps. Module 8 closed the first (plain-text
passwords). This module closes the second: `issueStubToken` returning a random
string is replaced with `jwt.sign` issuing a real, signed JSON Web Token - the exact
mechanism the Spring week's real `auth-stub` already uses.

## Part 1: What a JWT Actually Is

```bash
node jwt-basics-demo.mjs
```

Issue one, using the EXACT `jwt.sign` call the Spring week's `auth-stub` uses:

```javascript
const token = jwt.sign(
  { sub: "alice", roles: ["MISSION_OPERATOR"] },
  SECRET,
  { algorithm: "HS256", expiresIn: "1h" },
);
```

Verified real output (a real token, truncated here for space):

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGljZSIs...
```

**A JWT is three base64url-encoded parts, separated by dots** - header, payload,
signature. Split it apart and decode the first two directly:

```javascript
const [header, payload, signature] = token.split(".");
Buffer.from(header, "base64url").toString();
```

Verified real output:

```
decoded header:  {"alg":"HS256","typ":"JWT"}
decoded payload: {"sub":"alice","roles":["MISSION_OPERATOR"],"iat":1784227871,"exp":1784231471}
```

**This is worth stating plainly, because it surprises people: a JWT is encoded, not
encrypted.** Anyone holding a token - including a browser's dev tools, or `curl`, or
this demo script - can read `sub` and `roles` directly, no secret required. The
SECRET only protects the SIGNATURE, not the contents. Never put anything in a JWT
payload that the token's holder shouldn't be able to read.

## Part 2: Verifying - What the Signature Actually Buys You

```javascript
const decoded = jwt.verify(token, SECRET);
```

Verified real output:

```
{ sub: 'alice', roles: [ 'MISSION_OPERATOR' ], iat: 1784227871, exp: 1784231471 }
```

Now three ways a REAL verification genuinely fails:

**Tampering with the payload** (adding an `"ADMIN"` role, re-encoding, keeping the
original signature):

```
JsonWebTokenError: invalid signature
```

The signature is computed over the header AND payload together - change either one
by a single byte and the signature no longer matches. This is the entire point of
signing: the payload is READABLE but not WRITABLE without the secret.

**Verifying with the wrong secret:**

```
JsonWebTokenError: invalid signature
```

Same error - from the verifier's point of view, a tampered token and a token signed
with a different secret look identical: "the signature doesn't match what I'd
compute."

**An already-expired token:**

```
TokenExpiredError: jwt expired
```

A different, more specific error - `exp` is checked separately from the signature,
so `jwt.verify` can tell you WHICH thing failed.

## Part 3: Real Tokens, Wired Into the Auth Service

```typescript
private issueAccessToken(username: string, roles: string[]): string {
  return jwt.sign({ sub: username, roles }, JWT_SECRET, {
    algorithm: "HS256",
    expiresIn: "15m",
  });
}
```

```bash
curl -X POST http://localhost:3000/auth/login -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"mission123"}'
```

Verified real output (`accessToken` decodes to a real `{ sub, roles, iat, exp }`
payload - try it, exactly like Part 1):

```
{"accessToken":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...","refreshToken":"7285624e75..."}
```

**One deliberate asymmetry, worth naming:** `accessToken` is now a real JWT;
`refreshToken` stays an OPAQUE random string, not a JWT. This is a common,
deliberate real-world pattern, not an oversight - an access token is self-contained
and short-lived (`expiresIn: "15m"` here); a refresh token is long-lived and only
useful in combination with SERVER-SIDE state (the `users` map), which is exactly
what lets Module 7's `logout` revoke it. A signed JWT alone can't be revoked before
its own expiry - there's no server-side state to delete.

## Why JWT_SECRET Has to Match Exactly

```typescript
const JWT_SECRET = process.env.JWT_SECRET ||
  "mission-control-shared-secret-key-32-bytes-minimum";
```

Read directly from the Spring week's real `auth-stub/server.js` - same variable name, same
fallback string. This is what makes the Spring week's mission service (Java, validating
tokens with the SAME secret) able to accept tokens issued by THIS service, unchanged
- the whole reason Module 7 called this the "eventual replacement."

## A Running Comparison

| Node/jsonwebtoken | Java |
|---|---|
| `jwt.sign(payload, secret, { algorithm, expiresIn })` | `Jwts.builder().claim(...).signWith(...).compact()` (jjwt) |
| `jwt.verify(token, secret)` | `Jwts.parser().verifyWith(...).build().parseSignedClaims(token)` |
| `JsonWebTokenError` | `SignatureException` / `MalformedJwtException` |
| `TokenExpiredError` | `ExpiredJwtException` |

## Transition to the Lab

Learners add a SHORT expiry and a real expiry check to a JWT-issuing function of
their own, following this demo's exact `jwt.sign`/`jwt.verify` pattern - verified by
issuing a token, waiting past its expiry, and confirming `jwt.verify` throws the
right named error.
