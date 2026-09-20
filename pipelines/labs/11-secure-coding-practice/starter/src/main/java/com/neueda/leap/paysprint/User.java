package com.neueda.leap.paysprint;

public class User {
    private Long id;
    private String email;
    private String passwordHash;

    public User(Long id, String email, String passwordHash) {
        this.id = id;
        this.email = email;
        this.passwordHash = passwordHash;
    }

    public Long getId() { return id; }
    public String getEmail() { return email; }
    public String getPasswordHash() { return passwordHash; }
}
