// PaySprint Mobile - LoginController.java, exception handling (excerpt)

@ExceptionHandler(AuthenticationException.class)
public ResponseEntity<String> handleAuthFailure(AuthenticationException ex) {
    // Failed logins, including repeated attempts against the same account,
    // are caught here and simply turned into a generic response.
    // Nothing is written to any log, metric, or alert.
    return ResponseEntity.status(401).body("Invalid email or password");
}

@ExceptionHandler(AccessDeniedException.class)
public ResponseEntity<String> handleAccessDenied(AccessDeniedException ex) {
    // Same here: an authenticated user trying to access another
    // customer's account (see example 01) hits this handler silently.
    return ResponseEntity.status(403).body("Forbidden");
}
