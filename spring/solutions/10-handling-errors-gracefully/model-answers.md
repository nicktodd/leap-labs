# Module 10 - Model Answers & Notes

## `GlobalExceptionHandler`

```java
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

@ExceptionHandler(NoSuchElementException.class)
public ResponseEntity<ErrorResponse> handleNotFound(NoSuchElementException ex, HttpServletRequest request) {
    ErrorResponse body = ErrorResponse.of(404, "Not Found", ex.getMessage(), request.getRequestURI());
    return ResponseEntity.status(HttpStatus.NOT_FOUND).body(body);
}

@ExceptionHandler(OrderRejectedException.class)
public ResponseEntity<ErrorResponse> handleRejected(OrderRejectedException ex, HttpServletRequest request) {
    ErrorResponse body = ErrorResponse.of(422, "Unprocessable Entity", ex.getMessage(), request.getRequestURI());
    return ResponseEntity.status(HttpStatus.UNPROCESSABLE_ENTITY).body(body);
}

@ExceptionHandler(Exception.class)
public ResponseEntity<ErrorResponse> handleUnexpected(Exception ex, HttpServletRequest request) {
    ErrorResponse body = ErrorResponse.of(
            500, "Internal Server Error", "an unexpected error occurred", request.getRequestURI());
    return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(body);
}
```

## Why `NoSuchElementException` Covers Two Unrelated Call Sites

`InMemoryOrderRepository.findFeeRate` throws it for an unknown ticker; `OrderController.getOrder`
throws it for an unknown order id. Neither knows the other exists. That's the actual point of
`@RestControllerAdvice`: the handler is keyed on **exception type**, not on which layer or
endpoint threw it. Any future code anywhere in this service that throws
`NoSuchElementException` automatically gets a consistent `404` - nobody has to remember to wire
it up per-endpoint.

## Why the Catch-All Never Echoes `ex.getMessage()`

An anticipated exception (`OrderRejectedException`, `NoSuchElementException`) has a message you
wrote yourself, specifically to be client-safe. An *unanticipated* one - a `NullPointerException`
from a bug, a driver-level exception from a database timeout - was never written with a client in
mind. It might contain an internal class name, a table name, a fragment of a stack. Returning a
fixed, generic message for the catch-all is a deliberate boundary: full detail still reaches the
server log (add a `logger.error("Unhandled exception", ex)` call in a real service - omitted here
to keep the kata focused), but the client only ever sees "an unexpected error occurred."

## The 400 vs 422 Distinction, Now Concrete

This is the same distinction Module 6's `model-answers.md` described but had nowhere to
implement:

- **400** - the *request* is malformed. A negative quantity, a missing ticker. Bean Validation
  catches this before the controller method body ever runs (Module 6).
- **422** - the request is perfectly well-formed, but a *business rule* still rejects it. A trade
  value over the single-order limit is a completely valid `OrderRequestDto` - every field passes
  validation - the rule lives in `OrderService`, one layer deeper, where the domain logic is.

## What This Doesn't Cover (and Why That's Fine)

`OrderRejectedException` and `NoSuchElementException` are unchecked (`RuntimeException`) -
deliberately, so `OrderService` and `InMemoryOrderRepository` don't need `throws` clauses
polluting every method signature up the call stack. This is the same trade-off the Java week made
with its own domain exceptions: checked exceptions model "the caller must decide what to do right
here"; unchecked ones model "something further up the stack - in this case,
`GlobalExceptionHandler` - knows how to handle this generically, so don't force every
intermediate layer to know or care."
