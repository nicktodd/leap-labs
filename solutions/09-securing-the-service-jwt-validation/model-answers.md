# Module 9 — Model Answers & Notes

## Kata A — `SecurityConfig`

```java
@Bean
public JwtDecoder jwtDecoder() {
    SecretKeySpec key = new SecretKeySpec(
            sharedSecret.getBytes(StandardCharsets.UTF_8), "HmacSHA256");
    return NimbusJwtDecoder.withSecretKey(key).build();
}

@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http
            .csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(auth -> auth
                    .requestMatchers("/public").permitAll()
                    .anyRequest().authenticated())
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(jwt -> {}));
    return http.build();
}
```

(The reference solution additionally customises the `JwtAuthenticationConverter` to read the
`roles` claim — not required by the kata, but useful if you want `hasRole("MISSION_OPERATOR")`
checks later.)

## Kata B — the Stack Trace, Explained

```
java.lang.IllegalArgumentException: tokenValue cannot be empty
	at org.springframework.security.oauth2.core.AbstractOAuth2Token.<init>
	at org.springframework.web.bind.ServletRequestDataBinder.construct
```

**What's actually happening**: `Jwt` is a real class with real fields (`tokenValue`, claims,
etc.) and *no* no-args constructor Spring can call safely. A bare `Jwt jwt` parameter on a
`@RequestMapping` method, with no `@AuthenticationPrincipal`, isn't special-cased by Spring
Security at all — as far as Spring MVC is concerned, it's just an unrecognised object type, and
MVC's default behaviour for unrecognised object parameters is to try to **construct one from
request data** (`ServletRequestDataBinder`, the same machinery used for query-parameter binding
and `@ModelAttribute`). It tries to build a `Jwt` from an essentially empty request, hits `Jwt`'s
required-fields validation (`tokenValue cannot be empty`), and throws.

**The fix**:

```java
public String missionEndpoint(@AuthenticationPrincipal Jwt jwt) {
```

`@AuthenticationPrincipal` tells Spring MVC to resolve this parameter from
`SecurityContextHolder`'s current `Authentication` instead of from request data — the actual JWT
that Spring Security's resource server filter already validated earlier in the chain.

## Why This Is a Good GenAI-Interpretation Exercise

The stack trace's top frames are all Spring internals with no obvious connection to security or
JWTs — `AbstractOAuth2Token`, `ServletRequestDataBinder`. A learner pattern-matching on "JWT
endpoint + error" might reasonably (and wrongly) suspect the `SecurityConfig` they just wrote, the
shared secret, or the auth stub's token itself. GenAI is genuinely useful here for explaining
*Spring's request-parameter resolution machinery* in general — that's real, transferable
knowledge — but the learner still has to connect that explanation back to *this specific*
missing annotation themselves. That connection is the actual skill being practiced, not the stack
trace lookup.
