package com.neueda.leap.paysprint;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
import java.util.concurrent.atomic.AtomicInteger;

@RestController
public class LoginController {

    private static final org.slf4j.Logger log = org.slf4j.LoggerFactory.getLogger(LoginController.class);
    private static final int MAX_ATTEMPTS = 5;

    @Autowired
    private UserRepository userRepository;

    private BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
    private ConcurrentMap<String, Long> sessionStore = new ConcurrentHashMap<>();
    private ConcurrentMap<String, AtomicInteger> failedAttempts = new ConcurrentHashMap<>();

    @PostMapping("/api/login")
    public LoginResponse login(@RequestBody LoginRequest request) {
        String email = request.getEmail();
        AtomicInteger attempts = failedAttempts.computeIfAbsent(email, e -> new AtomicInteger(0));

        // VULNERABILITY (A07): the original version had no rate limiting,
        // delay, or lockout after repeated failed attempts against the same
        // account.
        //
        // FIX (A07): lock out further attempts once a threshold is reached.
        if (attempts.get() >= MAX_ATTEMPTS) {
            log.warn("Login blocked for {}: too many failed attempts", email);
            return new LoginResponse(null, "Account temporarily locked, try again later");
        }

        User user = userRepository.findByEmail(email);

        if (user != null && passwordEncoder.matches(request.getPassword(), user.getPasswordHash())) {
            attempts.set(0);
            String token = UUID.randomUUID().toString();
            sessionStore.put(token, user.getId());
            return new LoginResponse(token);
        }

        // VULNERABILITY (A09): the original version caught and discarded
        // failed logins here with nothing written to any log, metric, or
        // alert, a brute-force attempt would have been invisible to the team.
        //
        // FIX (A09): every failed attempt is logged with enough context to
        // investigate later, and the count feeds the lockout check above.
        attempts.incrementAndGet();
        log.warn("Failed login attempt for {}: attempt {} of {}", email, attempts.get(), MAX_ATTEMPTS);
        return new LoginResponse(null, "Invalid email or password");
    }
}
