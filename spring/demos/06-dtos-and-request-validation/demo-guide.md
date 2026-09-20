# Module 6 Demo Guide - DTOs & Request Validation

The spec becomes real code today. Run it, then walk through the failure case deliberately.

```bash
mvn spring-boot:run

# Valid request
curl -si -X POST http://localhost:8080/orders -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL","instrumentType":"EQUITY","quantity":100,"price":150.00,"side":"BUY"}'

# Invalid request - missing ticker, negative quantity
curl -si -X POST http://localhost:8080/orders -H "Content-Type: application/json" \
  -d '{"instrumentType":"EQUITY","quantity":-5,"price":150.00,"side":"BUY"}'
```

Expect: `201` with a `Location` header for the first; `400` for the second, with **no
mention of what specifically was wrong** in the response body yet.

## This IS Module 5's Spec - Point at It Directly

Open `order-service.yaml` from Module 5 next to `OrderRequestDto.java`. Walk through them side by
side: `ticker: string` → `String ticker`; `quantity: number, minimum: 0, exclusiveMinimum: true`
→ `@Positive double quantity`; `side: enum [BUY, SELL]` → `Side side` (a real Java enum). **This
is the entire point of contract-first**: the spec wasn't a suggestion, it was the actual
requirement this code had to satisfy.

## The DTO Pattern: Why Not Just Use the Domain Object Directly?

Ask the group: why not have the controller accept an `Order` domain object directly, if one
existed? Reasons, in order of how often they come up in a real system:

1. **The API contract and the internal model change for different reasons.** A database column
   rename shouldn't break every client of the API. A DTO absorbs that - the internal model can
   change freely as long as the DTO's mapping logic updates to match.
2. **You don't want to accidentally expose internal fields.** A domain object might carry
   internal-only data (audit fields, internal ids, calculated caches) that should never leave the
   service boundary.
3. **Validation belongs on the boundary, not scattered through the domain.** `OrderRequestDto`'s
   annotations describe exactly what's required to *enter* the system - that's a different
   concern from the domain's own invariants (the Java week's Module 2 `Holding` - validated in
   its own right, for its own reasons).

**Say explicitly**: there is no `Order` class anywhere in this module's demo. `OrderRequestDto`
and `OrderResponseDto` are the entire API surface - `OrderService` and `OrderRepository` behind
them have never heard of either DTO.

## `@Valid`: Validation That Runs Before Your Code Does

Point at `@Valid @RequestBody OrderRequestDto request` in the controller signature. Run the
invalid request again and be explicit: **the controller method body never executed.** Spring
intercepted the request, ran every annotation on `OrderRequestDto` (`@NotBlank`, `@NotNull`,
`@Positive`), found failures, and returned `400` automatically - before `submitOrder(...)`'s
first line ever ran.

## The Honest Gap: the 400 Doesn't Say What Was Wrong

Point at the actual response body: `{"timestamp": ..., "status": 400, "error": "Bad Request",
"path": "/orders"}` - no mention of "ticker is required" or "quantity must be positive," even
though those messages exist right there in the `@NotBlank`/`@Positive` annotations. **This is
deliberate, not a bug to apologise for.** Turning validation failures into a genuinely useful
response body is exactly Module 10's job (centralised exception handling) - today's job was
getting validation to trigger at all.

## Transition to the Lab

Learners implement Module 5's `GET /orders/{id}` spec the same way - a DTO, validation where it
applies, against the layered service they already built in Module 3.
