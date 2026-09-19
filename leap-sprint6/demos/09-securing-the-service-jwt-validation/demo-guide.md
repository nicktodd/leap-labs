# Module 9 Demo Guide — Securing the Service: JWT Validation

Today the mission brief's promise from Day 1 arrives: a separate Node.js auth service, and the
mission service that trusts its tokens without ever talking to it directly.

## Start Both Services

```bash
# Terminal 1 - the auth stub
cd shared/auth-stub
npm install
npm start        # http://localhost:4000

# Terminal 2 - the mission service
cd demos/09-securing-the-service-jwt-validation
mvn spring-boot:run    # http://localhost:8080
```

## Get a Token, Then Use It

```bash
curl -X POST http://localhost:4000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"mission123"}'
# {"token": "eyJhbGc..."}

curl http://localhost:8080/public
# No token required - anyone can see this.

curl -i http://localhost:8080/mission
# 401 - no Authorization header at all

curl -H "Authorization: Bearer eyJhbGc..." http://localhost:8080/mission
# Classified mission data - authorised for alice
```

**Say this explicitly**: the mission service never calls `localhost:4000`. It has no idea alice's
password is `mission123`, and doesn't want to. It only knows one thing — the shared secret — and
uses that to check whether a token's signature could only have come from something that knows the
same secret.

## The Shared Secret Is the Entire Trust Relationship

Open `application.properties` (`jwt.shared-secret=...`) next to `shared/auth-stub/server.js`
(`const SECRET = ...`). Same string, two unrelated codebases (Java and Node), two different
languages, two different JWT libraries. **This is what "the two services agree on a secret"
means in practice** — not a metaphor, an actual string that has to match exactly.

Break it live if there's time: change one character in `application.properties`, restart, and
try a token that worked a second ago. It fails — not because the token changed, but because the
service verifying it now expects a different signature.

## `SecurityConfig`: Two Beans Do All the Work

Open `SecurityConfig.java`.

- **`jwtDecoder()`** — builds a decoder from the shared secret. This is the only place the secret
  is used; nothing else in the app touches it.
- **`filterChain()`** — `.requestMatchers("/public").permitAll()` then
  `.anyRequest().authenticated()`, plus `.oauth2ResourceServer(oauth2 -> oauth2.jwt(...))` to tell
  Spring Security *how* to authenticate: by validating a bearer JWT with the decoder above.

Point at the `JwtGrantedAuthoritiesConverter` block: the auth stub's tokens carry roles as
`"roles": ["MISSION_OPERATOR"]`, not Spring Security's default `"scope"` claim — this converter is
what teaches Spring Security to read *our* claim shape instead of assuming a default.

## An Honest Bug: the Confusing Stack Trace

Before `@AuthenticationPrincipal` was added to `MissionController`, calling `/mission` with a
**valid** token produced:

```
java.lang.IllegalArgumentException: tokenValue cannot be empty
	at org.springframework.security.oauth2.core.AbstractOAuth2Token.<init>
	at org.springframework.web.bind.ServletRequestDataBinder.construct
```

**Walk through why, live**: a bare `Jwt jwt` controller parameter, with no
`@AuthenticationPrincipal`, isn't resolved by Spring Security at all — Spring MVC treats it as a
regular object it needs to construct from request parameters (the same machinery that builds
`@RequestBody` DTOs), tries to call `Jwt`'s constructor with no arguments, and fails. **The stack
trace mentions nothing about authentication, security, or JWTs by name** — this is exactly the
kind of error worth handing to GenAI to interpret before touching the code, which is what the lab
asks learners to do.

## Transition to the Lab

Kata A: implement `SecurityConfig` from TODOs — the app won't even start until it's right. Kata B:
`MissionController` has this exact bug baked in — hit it with a real token, interpret the stack
trace (with GenAI's help), then fix it yourself.
