# Module 9 Lab — Securing the Service: JWT Validation

## Objectives

By the end of this lab you will have:

- Wired JWT validation into a Spring Boot service, trusting a separate identity service's tokens
  without ever calling it directly
- Verified protected endpoints correctly reject unauthenticated requests
- Practiced using GenAI to interpret an unfamiliar security stack trace, before fixing the
  underlying bug yourself

## Setup

- Java 21, Maven, and Node.js installed
- Start the shared auth stub (leave it running for the whole lab):

  ```bash
  cd shared/auth-stub
  npm install
  npm start        # http://localhost:4000
  ```
- Given, don't modify: `MissionServiceApplication.java`, `application.properties`
  (`jwt.shared-secret` already matches the auth stub's secret)

## Task

### Kata A — `SecurityConfig`

Two `@Bean` methods, both currently throwing `UnsupportedOperationException`:

- **`jwtDecoder()`**: build a `NimbusJwtDecoder` from `sharedSecret`, treated as an HMAC-SHA256
  key (a `SecretKeySpec` with algorithm `"HmacSHA256"`).
- **`filterChain(HttpSecurity http)`**: disable CSRF, permit `/public` with no authentication,
  require authentication for everything else, and enable
  `.oauth2ResourceServer(oauth2 -> oauth2.jwt(...))` so Spring Security validates bearer tokens
  using the decoder above. The default `JwtAuthenticationConverter` is fine — you don't need to
  read the `roles` claim for this kata.

The app will not start at all until both are implemented — that's your first checkpoint.

### Verify Kata A

```bash
mvn spring-boot:run
```

```bash
curl http://localhost:8080/public
# should succeed with no token

curl -i http://localhost:8080/mission
# should be 401 - no Authorization header
```

### Kata B — the Confusing Stack Trace

Get a real token and try it against the protected endpoint:

```bash
TOKEN=$(curl -s -X POST http://localhost:4000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"mission123"}' | ...extract .token...)

curl -H "Authorization: Bearer $TOKEN" http://localhost:8080/mission
```

You should get a `500` with a stack trace that doesn't mention JWTs, tokens, or security by name
at all — something about `tokenValue cannot be empty` and Spring's data binder.

**Before changing any code**: paste the stack trace into GitHub Copilot Chat (or your GenAI tool
of choice) and ask it to explain what's actually happening and why. A reasonable starting prompt:

> "I'm getting this exception when I call a Spring Boot endpoint with a valid JWT bearer token.
> The endpoint method takes a parameter of type `Jwt`. Explain what Spring is trying to do when
> this exception is thrown, and why it's happening even though my token is valid."

Read the explanation critically — check it against what you already know about how Spring MVC
resolves controller method parameters (Module 2) versus how Spring Security's argument resolvers
work. Once you understand *why* (not just *what to type*), fix `MissionController.missionEndpoint`
yourself.

### Verify Kata B

```bash
curl -H "Authorization: Bearer $TOKEN" http://localhost:8080/mission
# Classified mission data - authorised for alice
```

## Deliverable

`SecurityConfig.java` and `MissionController.java`, both fully working.

## Acceptance criteria

- `mvn spring-boot:run` starts successfully
- `GET /public` succeeds with no `Authorization` header
- `GET /mission` returns `401` with no token, and `403`/`401` with a malformed one
- `GET /mission` returns `200` with the authorised username, given a real token from the auth stub
