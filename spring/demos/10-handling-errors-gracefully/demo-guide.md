# Module 10 Demo Guide - Handling Errors Gracefully

Two honest gaps this week has left open on purpose get closed today. Open Module 3's demo
(`GET /portfolios/UNKNOWN` → raw `500`) and Module 6's demo (`400` with no detail about what was
wrong) side by side with this one, if they're still around.

```bash
mvn spring-boot:run
```

```bash
# 201 - unchanged from Module 6
curl -si -X POST http://localhost:8080/orders -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL","instrumentType":"EQUITY","quantity":100,"price":150.00,"side":"BUY"}'

# 400 - now WITH field-level detail
curl -s -X POST http://localhost:8080/orders -H "Content-Type: application/json" \
  -d '{"instrumentType":"EQUITY","quantity":-5,"price":150.00,"side":"BUY"}'

# 404 - unknown order id, no longer a raw 500
curl -s http://localhost:8080/orders/999

# 404 - unknown ticker, THREE LAYERS DOWN in OrderService/InMemoryOrderRepository
curl -s -X POST http://localhost:8080/orders -H "Content-Type: application/json" \
  -d '{"ticker":"NOTREAL","instrumentType":"EQUITY","quantity":100,"price":150.00,"side":"BUY"}'

# 422 - a well-formed order, rejected by a business rule
curl -s -X POST http://localhost:8080/orders -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL","instrumentType":"EQUITY","quantity":100000,"price":150.00,"side":"BUY"}'
```

**Read the two 404 responses side by side.** One came from `OrderController` (unknown order id),
the other from `InMemoryOrderRepository` (unknown ticker) - three layers deeper in the call stack,
inside `OrderService.calculateFee`. Neither piece of code knows the other exists. **Same response
shape anyway.** That's the entire point of `@RestControllerAdvice`.

## One Handler Class, Applied Everywhere

Open `GlobalExceptionHandler.java`. Point at `@RestControllerAdvice` on the class itself - this
is what makes every `@ExceptionHandler` inside apply to *every* `@RestController` in the service,
not just one. Contrast with `try/catch` scattered through individual controller methods: that
approach means remembering to add handling at every call site, and getting the response shape
subtly different each time. This approach means writing the handling once, per exception *type*.

## Walk Through Each Handler

- **`handleValidation`** - pulls every violated field off
  `ex.getBindingResult().getFieldErrors()`. This is Module 6's honest gap, closed: point at the
  generic `{"status":400,...}` body Module 6 shipped with, then this module's
  `{"fieldErrors":[{"field":"ticker","message":"ticker is required"}, ...]}`.
- **`handleNotFound`** - one handler, `NoSuchElementException`, used by two unrelated call sites.
  Emphasise: nobody had to modify `OrderController` and `InMemoryOrderRepository` to "know about"
  each other. They both just throw the same *kind* of exception when something doesn't exist.
- **`handleRejected`** - `OrderRejectedException` → `422`. Open `OrderService.calculateFee` and
  point at where it's thrown: a trade value over the limit is a perfectly well-formed request
  (every Bean Validation annotation on `OrderRequestDto` passes) that a *business rule*, one layer
  deeper, still won't allow.
- **`handleUnexpected`** - the catch-all. **Say explicitly**: it never returns `ex.getMessage()`.
  An exception nobody anticipated might carry something that shouldn't reach a client - a class
  name, a fragment of internal state. Full detail belongs in the server log, not the response
  body.

## `NoSuchElementException` Reused From `java.util`, Not a Custom Type

Point out `NoSuchElementException` is a standard JDK exception, not something written for this
service. `OrderRejectedException` (a genuinely new business concept) got a custom type;
"this thing you looked up doesn't exist" didn't need one. Worth a beat of discussion: when is a
custom exception worth creating, versus reusing something the JDK already has a name for?

## Transition to the Lab

Learners implement all four handlers from TODOs, verified against a pre-written integration test
(`OrderErrorHandlingTest`) that exercises the real running service end-to-end - all four handlers
plus the untouched happy path.
