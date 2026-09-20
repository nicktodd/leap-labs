# Lab 10 Model Answers

## Verified Output

```bash
npm test
```
```
console.log
    [auth] login_success username=carol

      at logAuthEvent (src/logger.ts:7:11)

Test Suites: 1 passed, 1 total
Tests:       3 passed, 3 total
```

The log line prints twice because two of the three tests each perform their own
`register` + `login` in isolation (`beforeEach` creates a fresh `AuthService`, so
there's no shared state between tests to cause an unexpected third print).

## Key Points

- **TODO 1**: `accessToken` and `refreshToken` are both real values returned from
  `login`, but they come from two different generators - `jwt.sign` for the access
  token, `randomBytes(32).toString("hex")` for the refresh token - so beyond both
  being strings, asserting they're *not equal* is a cheap guard against a copy-paste
  bug that accidentally returns the same value twice.
- **TODO 2**: `jwt.verify(accessToken, JWT_SECRET)` both validates the signature and
  returns the decoded payload in one call - if the token were tampered with or signed
  with a different secret, this line would throw before the `expect` assertions ever
  ran, which is exactly the "validates" half of this test's name.
- **TODO 3**: `expect(promise).rejects.toThrow()` is Jest's idiom for asserting an
  `async` function throws - `await`-ing the rejected promise directly inside a `try`/
  `catch` works too, but `rejects.toThrow()` reads as a single assertion and is the
  more common pattern in real NestJS test suites.
- **TODO 4**: `logAuthEvent("login_success", username)` sits after
  `user.refreshToken = refreshToken;` and before the `return` - late enough that it
  only fires once the login has genuinely succeeded, early enough that a future
  change to the return statement can't accidentally skip it.

## The Reflection Question

The field that matters most for a real security team is the **source IP address** (or
equivalent request-origin identifier) of the failed attempt - a single failed login is
noise, but the same source IP failing against many different usernames in a short
window is the actual signature of credential stuffing, and username alone can't
distinguish that from an ordinary user who mistyped their own password.

This lightweight pass doesn't ask for it because `AuthService.login` has no visibility
into the request at all - it's a plain class method called with just a username and
password, with no access to the HTTP request object IP data lives on. Adding IP-aware
failed-login logging is a controller/middleware-level change, not a service-level one,
which is exactly the kind of scope the outline flags as deliberately left out of this
"awareness level, not exhaustive OWASP-style review" pass.
