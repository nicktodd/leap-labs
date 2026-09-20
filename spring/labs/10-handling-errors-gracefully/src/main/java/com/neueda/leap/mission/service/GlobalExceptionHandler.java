package com.neueda.leap.mission.service;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.NoSuchElementException;

// KATA: one handler per exception type, all applied globally to every
// @RestController via @RestControllerAdvice. Use ErrorResponse.of(...) or
// ErrorResponse.withFieldErrors(...) to build each body - both are given,
// fully implemented, in ErrorResponse.java.
@RestControllerAdvice
public class GlobalExceptionHandler {

    // TODO: handle MethodArgumentNotValidException (thrown when @Valid
    // fails) -> 400, with one FieldError per violated field. Pull them from
    // ex.getBindingResult().getFieldErrors().
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException ex,
                                                            HttpServletRequest request) {
        throw new UnsupportedOperationException("TODO: implement handleValidation");
    }

    // TODO: handle NoSuchElementException -> 404. This is thrown both by
    // InMemoryOrderRepository (unknown ticker) and by OrderController
    // (unknown order id) - one handler covers both.
    @ExceptionHandler(NoSuchElementException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(NoSuchElementException ex, HttpServletRequest request) {
        throw new UnsupportedOperationException("TODO: implement handleNotFound");
    }

    // TODO: handle OrderRejectedException -> 422 (a well-formed order,
    // rejected by a business rule - distinct from the 400 case above).
    @ExceptionHandler(OrderRejectedException.class)
    public ResponseEntity<ErrorResponse> handleRejected(OrderRejectedException ex, HttpServletRequest request) {
        throw new UnsupportedOperationException("TODO: implement handleRejected");
    }

    // TODO: catch-all -> 500. Deliberately generic: never echo
    // ex.getMessage() or expose internal detail to the client here.
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleUnexpected(Exception ex, HttpServletRequest request) {
        throw new UnsupportedOperationException("TODO: implement handleUnexpected");
    }
}
