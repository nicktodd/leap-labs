package com.fidelity.leap.sprint6;

// A well-formed order that still breaks a BUSINESS rule - distinct from
// Bean Validation failures (malformed requests, Module 6's 400 case). This
// is Module 6's 422 case, finally with somewhere for it to live.
public class OrderRejectedException extends RuntimeException {

    public OrderRejectedException(String message) {
        super(message);
    }
}
