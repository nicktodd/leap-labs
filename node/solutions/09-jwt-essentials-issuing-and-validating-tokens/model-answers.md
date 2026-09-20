# Lab 9 Model Answers

## Verified Output

```
--- A normal token, issued and validated ---
{
  sub: 'dave',
  roles: [ 'MISSION_OPERATOR' ],
  iat: 1784230327,
  exp: 1784233927
}

--- An already-expired token ---
TokenExpiredError: jwt expired

--- A tampered token ---
JsonWebTokenError: invalid signature
```

## Key Points

- **TODO 1**: `issueToken` is a thin wrapper around `jwt.sign` - the payload shape
  (`{ sub, roles }`) and the algorithm (`"HS256"`) are fixed, matching the Spring week's
  `auth-stub`; only `expiresIn` varies per call, which is exactly what lets this same
  function issue both the normal 1-hour token and the deliberately-expired one.
- **TODO 2**: `validateToken` is a one-line pass-through to `jwt.verify` - the whole
  point of TODO 2 is resisting the urge to add a `try`/`catch` inside it, since
  swallowing the error there is exactly what the reflection question asks about.

## The Reflection Question

If `validateToken` caught every error and returned `null` (or `{ valid: false }`)
instead of letting it propagate, the CALLER would lose the ability to tell WHICH of
the three failure modes actually happened - and those three modes genuinely call for
different responses in a real system:

- **`TokenExpiredError`** - a normal, expected event. The client should silently use
  its refresh token to get a new access token (Module 7's `refresh` flow) - no
  alarm needed.
- **`JsonWebTokenError`** (tampered signature, or verified with the wrong secret) -
  NOT normal. Either someone is actively attempting to forge a token, or there's a
  real configuration bug (mismatched secrets between services). This deserves
  logging and investigation, not a silent retry.

Collapsing both into a single `null` throws away exactly the information needed to
tell "please refresh, nothing is wrong" apart from "something is actively wrong here"
- which is the entire reason `jsonwebtoken` throws differently-named errors in the
first place, rather than one generic `InvalidTokenError`.
