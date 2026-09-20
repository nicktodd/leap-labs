package com.neueda.leap.paysprint;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.Base64;

public class UserRegistrationService {

    private UserRepository userRepository;

    public UserRegistrationService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public User registerUser(String email, String rawPassword) {
        String hashed = md5(rawPassword);
        return userRepository.save(new User(null, email, hashed));
    }

    private String md5(String input) {
        try {
            MessageDigest digest = MessageDigest.getInstance("MD5");
            byte[] hash = digest.digest(input.getBytes(StandardCharsets.UTF_8));
            return Base64.getEncoder().encodeToString(hash);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
