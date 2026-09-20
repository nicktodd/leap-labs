package com.neueda.leap.mission.service;

import java.time.Instant;
import java.util.List;

// One shape, every error, everywhere in this service. A client never has
// to guess whether an error comes back as a plain string, a nested object,
// or Spring's own default body - it's always this.
public record ErrorResponse(
        Instant timestamp,
        int status,
        String error,
        String message,
        String path,
        List<FieldError> fieldErrors
) {
    public record FieldError(String field, String message) {}

    public static ErrorResponse of(int status, String error, String message, String path) {
        return new ErrorResponse(Instant.now(), status, error, message, path, List.of());
    }

    public static ErrorResponse withFieldErrors(int status, String error, String message, String path,
                                                 List<FieldError> fieldErrors) {
        return new ErrorResponse(Instant.now(), status, error, message, path, fieldErrors);
    }
}
