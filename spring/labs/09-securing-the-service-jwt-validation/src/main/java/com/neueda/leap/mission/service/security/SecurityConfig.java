package com.neueda.leap.mission.service.security;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.oauth2.jwt.JwtDecoder;
import org.springframework.security.web.SecurityFilterChain;

// KATA A - wire JWT validation into this service.
@Configuration
public class SecurityConfig {

    @Value("${jwt.shared-secret}")
    private String sharedSecret;

    @Bean
    public JwtDecoder jwtDecoder() {
        // TODO: build a NimbusJwtDecoder using sharedSecret as an HMAC-SHA256
        // key (a SecretKeySpec, algorithm "HmacSHA256"). This is the same
        // secret the Node auth stub signs tokens with.
        throw new UnsupportedOperationException("TODO: implement jwtDecoder");
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        // TODO:
        //  - disable CSRF (this is a stateless API, not a browser form)
        //  - permit /public with no authentication required
        //  - require authentication for every other request
        //  - enable oauth2ResourceServer().jwt() (the default JwtAuthenticationConverter
        //    is fine for this kata - you don't need to customise the roles claim)
        throw new UnsupportedOperationException("TODO: implement filterChain");
    }
}
