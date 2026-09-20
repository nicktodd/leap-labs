# Module 10 Lab - Handling Errors Gracefully

## Objectives

By the end of this lab you will have:

- Implemented a `@RestControllerAdvice` that turns every kind of failure in the service into the
  same consistent error response shape
- Closed two gaps this week has deliberately left open since Module 3 (a raw, unhandled 500)
  and Module 6 (a validation 400 with no detail about what was wrong)
- Distinguished a malformed request (400) from a well-formed request a business rule still
  rejects (422)

## Setup

- Java 21 and Maven installed
- Given, don't modify: `MissionServiceApplication.java`, `OrderRepository.java`,
  `InMemoryOrderRepository.java`, `OrderRequestDto.java`, `OrderResponseDto.java`,
  `OrderService.java` (already throws `OrderRejectedException` for trade values over the limit),
  `OrderController.java`, `ErrorResponse.java`, `OrderRejectedException.java`
- `mvn test` runs `OrderErrorHandlingTest.java` - pre-written, exercises every handler against the
  real running service

## Task

Implement all four `@ExceptionHandler` methods in `GlobalExceptionHandler`, currently stubbed
with `throw new UnsupportedOperationException(...)`:

- **`handleValidation`** - `MethodArgumentNotValidException` (thrown when `@Valid` fails) → `400`.
  Build one `ErrorResponse.FieldError` per violated field from
  `ex.getBindingResult().getFieldErrors()`, and return them via `ErrorResponse.withFieldErrors(...)`.
- **`handleNotFound`** - `NoSuchElementException` → `404`. This single handler covers two
  unrelated call sites: `InMemoryOrderRepository` throwing it for an unknown ticker, and
  `OrderController.getOrder` throwing it for an unknown order id.
- **`handleRejected`** - `OrderRejectedException` → `422`. A well-formed order a business rule
  still rejects - not the same thing as a malformed request.
- **`handleUnexpected`** - catch-all `Exception` → `500`. Return a generic message
  (`"an unexpected error occurred"`) - never `ex.getMessage()` here. An exception you didn't
  anticipate might carry detail (a class name, a fragment of internal state) that has no business
  reaching a client.

Use `ErrorResponse.of(status, error, message, request.getRequestURI())` for the three
non-validation handlers.

### Verify

```bash
mvn test
```

```bash
mvn spring-boot:run
```

```bash
# 201
curl -si -X POST http://localhost:8080/orders -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL","instrumentType":"EQUITY","quantity":100,"price":150.00,"side":"BUY"}'

# 400, with fieldErrors
curl -s -X POST http://localhost:8080/orders -H "Content-Type: application/json" \
  -d '{"instrumentType":"EQUITY","quantity":-5,"price":150.00,"side":"BUY"}'

# 404 - unknown order id
curl -s http://localhost:8080/orders/999

# 404 - unknown ticker, three layers down
curl -s -X POST http://localhost:8080/orders -H "Content-Type: application/json" \
  -d '{"ticker":"NOTREAL","instrumentType":"EQUITY","quantity":100,"price":150.00,"side":"BUY"}'

# 422 - business rule
curl -s -X POST http://localhost:8080/orders -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL","instrumentType":"EQUITY","quantity":100000,"price":150.00,"side":"BUY"}'
```

## Deliverable

`GlobalExceptionHandler.java`, fully implemented.

## Acceptance criteria

- `mvn test` passes with 0 failures and 0 errors (5 tests)
- Every error response has the same JSON shape: `timestamp`, `status`, `error`, `message`, `path`,
  `fieldErrors`
- The catch-all handler never leaks an exception's own message to the client
