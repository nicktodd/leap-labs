package com.neueda.leap.mission.service;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.List;
import java.util.NoSuchElementException;

// @RestControllerAdvice applies these handlers to every @RestController in
// the service - one place, every endpoint. Spring picks the most specific
// matching @ExceptionHandler for whatever gets thrown; anything not caught
// here falls through to the catch-all at the bottom.
@RestControllerAdvice
public class GlobalExceptionHandler {

    // Module 6's honest gap, closed: instead of Spring's default
    // {"status":400,"error":"Bad Request",...} with no mention of WHAT was
    // wrong, every violated field and its message is listed explicitly.
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException ex,
                                                            HttpServletRequest request) {
        List<ErrorResponse.FieldError> fieldErrors = ex.getBindingResult().getFieldErrors().stream()
                .map(fe -> new ErrorResponse.FieldError(fe.getField(), fe.getDefaultMessage()))
                .toList();
        ErrorResponse body = ErrorResponse.withFieldErrors(
                400, "Bad Request", "request failed validation", request.getRequestURI(), fieldErrors);
        return ResponseEntity.badRequest().body(body);
    }

    // Module 3's honest gap, closed: an unknown ticker (or, here, an unknown
    // order id) used to bubble up as a raw, unhandled 500. Same exception
    // type from two different layers - the repository and the controller -
    // now produces the exact same clean response shape.
    @ExceptionHandler(NoSuchElementException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(NoSuchElementException ex, HttpServletRequest request) {
        ErrorResponse body = ErrorResponse.of(404, "Not Found", ex.getMessage(), request.getRequestURI());
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(body);
    }

    // A well-formed order, rejected by a BUSINESS rule - Module 6's 422
    // case, distinct from the 400 case above.
    @ExceptionHandler(OrderRejectedException.class)
    public ResponseEntity<ErrorResponse> handleRejected(OrderRejectedException ex, HttpServletRequest request) {
        ErrorResponse body = ErrorResponse.of(422, "Unprocessable Entity", ex.getMessage(), request.getRequestURI());
        return ResponseEntity.status(HttpStatus.UNPROCESSABLE_ENTITY).body(body);
    }

    // The catch-all. Deliberately generic - never echo ex.getMessage() or a
    // stack trace here. An unanticipated exception might carry internal
    // detail (a SQL fragment, an internal class name) that has no business
    // reaching a client. Full detail still goes to the server log.
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleUnexpected(Exception ex, HttpServletRequest request) {
        ErrorResponse body = ErrorResponse.of(
                500, "Internal Server Error", "an unexpected error occurred", request.getRequestURI());
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(body);
    }
}
