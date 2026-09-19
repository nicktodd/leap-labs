# Lab 11 Model Answers

## Verified Output

```
login: {"accessToken":"stub-access-token-for-dave-tcibqanz","refreshToken":"stub-refresh-token-for-dave-0adgqmo4"}
logout: {"loggedOut":true}
refresh (same token, after logout): {"message":"invalid or expired refresh token","error":"Unauthorized","statusCode":401}
```

## Key Points

- **TODO 1**: `logout` reuses the given `findByRefreshToken` helper — the exact same
  lookup `refresh()` already does — then sets `user.refreshToken = null` instead of
  issuing a new token. Setting it to `null` (not deleting the user, not clearing the
  password) is deliberate: logging out ends the SESSION, not the account.
- **TODO 2**: `logout()`'s controller route is a near-identical copy of `refresh()`'s
  — same `@Post`, same `@HttpCode(200)`, same `RefreshDto` body shape — because the
  REQUEST shape really is identical ("here is a refresh token"); only what the service
  does with it differs.

## The Reflection Question

One refresh token per user is a real, common design choice, not a bug by accident —
some systems (especially ones prioritising "if this account is compromised, kick
every other session out immediately") deliberately allow only one active session at a
time, and a new login intentionally invalidating the old one is the FEATURE, not a
side effect.

Supporting multiple concurrent sessions (phone AND laptop, both valid) would need
`refreshToken: string | null` to become a collection — `refreshTokens: Set<string>` or
similar — with `login` ADDING to it, `logout` removing just the ONE token being logged
out (not clearing all of them), and `findByRefreshToken` searching within each user's
set instead of comparing a single value. The trade-off: more state to manage, and a
compromised token now only invalidates one session unless the user (or an admin)
explicitly revokes all sessions — a real design decision a production auth service has
to make deliberately, not accidentally.
