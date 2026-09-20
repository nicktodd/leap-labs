# Module 7 Demo Guide - Building the Auth Service Skeleton: Login, Register, Refresh

This is this week's actual mission, started for real. The Spring week's `mission-brief.md`
said it plainly: this NestJS service is the eventual REPLACEMENT for
`shared/auth-stub` - same job, same contract, built with everything this week has
taught instead of the Spring week's small hand-rolled Express script. Today's version is
deliberately a SKELETON, incomplete in two specific, flagged ways:

- Passwords are stored in **plain text**. Module 8 (Secure DB Access & Password
  Hashing) replaces this.
- Tokens are **random strings, not real JWTs**. Module 9 (JWT Essentials) replaces
  this - matching the exact shape the Spring week's real `auth-stub` already uses.

Building it in this order is deliberate: get the REQUEST/RESPONSE SHAPE right first,
verified end-to-end, before adding the security-critical pieces on top of a shape
that's already proven correct.

## Part 0: What This Replaces

The Spring week's real `shared/auth-stub/server.js` - read it directly, it's short:

```javascript
app.post('/login', (req, res) => {
  const { username, password } = req.body || {};
  const user = USERS[username];
  if (!user || user.password !== password) {
    return res.status(401).json({ error: 'invalid username or password' });
  }
  const token = jwt.sign({ sub: username, roles: user.roles }, SECRET, { ... });
  res.json({ token });
});
```

One hardcoded user, `alice` / `mission123`, one endpoint. This module's skeleton
preloads the exact same `alice` / `mission123` pair - the Spring week's mission service must
eventually be able to log in against THIS service, unchanged, so the test data has to
match exactly, not just "look similar."

## Part 1: Three DTOs, Three Contracts

```typescript
export class LoginDto {
  @IsString() @IsNotEmpty() username!: string;
  @IsString() @IsNotEmpty() password!: string;
}

export class RegisterDto {
  @IsString() @IsNotEmpty() @MinLength(3) username!: string;
  @IsString() @MinLength(8) password!: string;
}

export class RefreshDto {
  @IsString() @IsNotEmpty() refreshToken!: string;
}
```

Module 6's exact pattern, three times. `RegisterDto` is deliberately STRICTER than
`LoginDto` (a minimum username/password length) - a real system enforces password
strength when an account is CREATED, not on every subsequent login attempt.

## Part 2: The Service - Where the Skeleton's Two Gaps Live

```typescript
private readonly users = new Map<string, StoredUser>([
  ["alice", { password: "mission123", refreshToken: null }],
]);

register(username: string, password: string) {
  if (this.users.has(username)) {
    throw new ConflictException(`${username} is already registered`);
  }
  this.users.set(username, { password, refreshToken: null });
  return { username, registered: true };
}

login(username: string, password: string) {
  const user = this.users.get(username);
  if (!user || user.password !== password) {
    throw new UnauthorizedException("invalid username or password");
  }
  const accessToken = this.issueStubToken("access", username);
  const refreshToken = this.issueStubToken("refresh", username);
  user.refreshToken = refreshToken;
  return { accessToken, refreshToken };
}
```

`ConflictException` and `UnauthorizedException` are Nest built-ins - throwing one
inside a provider automatically produces the right HTTP status code and JSON error
shape, without the controller ever touching a status code directly.

`refresh(refreshToken)` looks up which user currently holds that exact refresh token
and issues a fresh access token - the REAL version (Module 9) will decode and verify
a signed JWT instead of a plain string lookup, but the CONTRACT - "give me a valid
refresh token, get a new access token back" - is already correct.

## Part 3: Three Real Flows, Verified End to End

```bash
curl -X POST http://localhost:3000/auth/login -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"mission123"}'
```

```
{"accessToken":"stub-access-token-for-alice-p626vyec","refreshToken":"stub-refresh-token-for-alice-auzcbr9k"}
```

Wrong password - real `401`:

```
{"message":"invalid username or password","error":"Unauthorized","statusCode":401}
```

Register a new user, then log in as them:

```bash
curl -X POST http://localhost:3000/auth/register -H "Content-Type: application/json" \
  -d '{"username":"grace","password":"secret123"}'
```

```
{"username":"grace","registered":true}
```

Registering `alice` again - real `409`, not a silent overwrite:

```
{"message":"alice is already registered","error":"Conflict","statusCode":409}
```

Refresh, using the refresh token from a real login response:

```bash
curl -X POST http://localhost:3000/auth/refresh -H "Content-Type: application/json" \
  -d '{"refreshToken":"stub-refresh-token-for-alice-oprcxqox"}'
```

```
{"accessToken":"stub-access-token-for-alice-mv5beipi"}
```

A bogus refresh token - real `401`, same as a bad login:

```
{"message":"invalid or expired refresh token","error":"Unauthorized","statusCode":401}
```

## Why Build It in This Order

Everything above is genuinely testable RIGHT NOW, with `curl`, without a database,
without real cryptography - because the skeleton separates "does the API shape work"
from "is the security implementation correct." Getting the shape wrong AND the
security wrong at the same time makes debugging either one harder. This module fixes
the shape first, with the two remaining gaps named explicitly, so Modules 8 and 9
each have exactly one thing to get right, on top of something already proven to work.

## Transition to the Lab

Learners add a fourth endpoint to this same skeleton - `POST /auth/logout`, which
invalidates a user's stored refresh token - following the same
DTO → service method → controller route pattern used for all three endpoints here,
verified by confirming a refresh token stops working immediately after logout.
