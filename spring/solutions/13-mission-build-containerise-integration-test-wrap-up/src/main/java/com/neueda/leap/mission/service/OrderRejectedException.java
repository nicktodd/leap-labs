package com.neueda.leap.mission.service;

// Module 10's pattern, reused. Thrown when OrderController translates a
// domain.ValidationResult.invalid(...) into an HTTP-facing failure.
public class OrderRejectedException extends RuntimeException {

    public OrderRejectedException(String message) {
        super(message);
    }
}
