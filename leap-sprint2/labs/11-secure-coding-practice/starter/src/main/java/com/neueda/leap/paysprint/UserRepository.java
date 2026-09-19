package com.neueda.leap.paysprint;

public interface UserRepository {
    User findByEmail(String email);
    User save(User user);
}
