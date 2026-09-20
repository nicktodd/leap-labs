package com.neueda.leap.paysprint;

public class AuthenticationFailedException extends RuntimeException {
    public AuthenticationFailedException(String message) {
        super(message);
    }
}
