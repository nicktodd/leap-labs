package com.neueda.leap.paysprint;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

public class UserRegistrationService {

    private UserRepository userRepository;
    private BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    public UserRegistrationService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    // VULNERABILITY (A04): the original version hashed passwords with MD5, a
    // fast, unsalted, general-purpose hash, not a password hash. Trivially
    // brute-forced if the database leaks.
    //
    // FIX (A04): bcrypt is slow and salted by design, appropriate for password
    // storage. Note: SHA-256 alone would NOT be an adequate fix here, it is
    // still a fast, general-purpose hash with the same underlying weakness as
    // MD5, just a longer digest. A Copilot suggestion of SHA-256 should be
    // rejected for this reason.
    public User registerUser(String email, String rawPassword) {
        String hashed = passwordEncoder.encode(rawPassword);
        return userRepository.save(new User(null, email, hashed));
    }
}
