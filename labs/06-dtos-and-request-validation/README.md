# Module 6 Lab — DTOs & Request Validation

## Objectives

By the end of this lab you will have:

- Applied Bean Validation annotations to a DTO, matching Module 5's OpenAPI schema exactly
- Implemented both operations from Module 5's spec against the Module 3 layered service
- Seen validation tested in true isolation, with no Spring context required

## Setup

- Java 21 and Maven installed
- Given, don't modify: `MissionServiceApplication.java`, `OrderRepository.java`,
  `InMemoryOrderRepository.java`, `OrderService.java`, `InstrumentType.java`, `Side.java`,
  `OrderResponseDto.java`
- `mvn test` runs `OrderRequestDtoTest.java` — pre-written, defines the exact validation rules
  `OrderRequestDto` must enforce

## Task

### Kata A — `OrderRequestDto`

Add Bean Validation annotations to every field, matching Module 5's OpenAPI `OrderRequest`
schema:

- `ticker` — required, non-blank (`@NotBlank`)
- `instrumentType` — required (`@NotNull`)
- `quantity` — required, must be positive (`@Positive`)
- `price` — required, must be positive (`@Positive`)
- `side` — required (`@NotNull`)

Run `mvn test` — all 7 tests in `OrderRequestDtoTest` should pass. Notice this test never starts
a Spring context; it uses `jakarta.validation`'s own `Validator` directly.

### Kata B — `OrderController`

Two operations, both currently stubbed with `UnsupportedOperationException` and missing their
mapping annotations:

- **`submitOrder`**: add `@PostMapping`. Take `@Valid @RequestBody OrderRequestDto`. Calculate
  the fee via `service.calculateFee(ticker, quantity * price)`. Generate an id from
  `idSequence`, build an `OrderResponseDto` with status `"ACCEPTED"`, store it in the `orders`
  map, and return `201 Created` with a `Location` header of `/orders/{id}`.
- **`getOrder`**: add `@GetMapping("/{id}")`. Look up `id` in the `orders` map. Return `200` with
  the found order, or `404` if there's no order with that id.

### Verify

```bash
mvn spring-boot:run
```

```bash
curl -si -X POST http://localhost:8080/orders -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL","instrumentType":"EQUITY","quantity":100,"price":150.00,"side":"BUY"}'

curl http://localhost:8080/orders/1
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/orders/999
```

## Deliverable

`OrderRequestDto.java` and `OrderController.java`, both fully implemented.

## Acceptance criteria

- `mvn test` passes with 0 failures and 0 errors (7 tests)
- `POST /orders` returns `201` with a `Location` header for a valid request, and `400` for an
  invalid one (missing/negative fields)
- `GET /orders/{id}` returns `200` for an order that was just created, and `404` for one that
  doesn't exist
