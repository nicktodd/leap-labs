package com.neueda.leap.paysprint;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;

@RestController
public class LoginController {

    @Autowired
    private UserRepository userRepository;

    private ConcurrentMap<String, Long> sessionStore = new ConcurrentHashMap<>();

    @PostMapping("/api/login")
    public LoginResponse login(@RequestBody LoginRequest request) {
        User user = userRepository.findByEmail(request.getEmail());

        if (user != null && user.getPasswordHash().equals(md5(request.getPassword()))) {
            String token = UUID.randomUUID().toString();
            sessionStore.put(token, user.getId());
            return new LoginResponse(token);
        }

        return new LoginResponse(null, "Invalid email or password");
    }

    @ExceptionHandler(AuthenticationFailedException.class)
    public LoginResponse handleAuthFailure(AuthenticationFailedException ex) {
        return new LoginResponse(null, "Invalid email or password");
    }

    private String md5(String input) {
        try {
            java.security.MessageDigest digest = java.security.MessageDigest.getInstance("MD5");
            byte[] hash = digest.digest(input.getBytes(java.nio.charset.StandardCharsets.UTF_8));
            return java.util.Base64.getEncoder().encodeToString(hash);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
