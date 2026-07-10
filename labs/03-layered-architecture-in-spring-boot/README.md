# Module 3 Lab — Layered Architecture in Spring Boot

## Objectives

By the end of this lab you will have:

- Built a controller → service → repository layered structure, with constructor-based DI
- Seen why layering and DI make a class testable without a running Spring context

## Setup

- Java 21 and Maven installed
- Given, don't modify: `MissionServiceApplication.java`, `OrderRepository.java`,
  `InMemoryOrderRepository.java`, `application.properties`
- `mvn test` runs `OrderServiceTest.java` — pre-written, defines what `OrderService` must do

## The Business Rule

`OrderService.calculateFee(ticker, tradeValue)` returns `tradeValue * rate`, where `rate` comes
from `OrderRepository.findFeeRate(ticker)`.

## Task

### Kata A — `OrderService`

- Add a `private final OrderRepository` field
- Add a constructor that accepts an `OrderRepository` and assigns it to the field (this is what
  lets Spring inject it automatically — and what lets the test inject a mock instead)
- Implement `calculateFee(ticker, tradeValue)` as described above

### Kata B — `OrderController`

- Add a `private final OrderService` field, and a constructor that accepts one
- Add a method annotated `@GetMapping("/orders/{ticker}/fee")` that takes `ticker` as a
  `@PathVariable` and `tradeValue` as a `@RequestParam double`, and returns
  `service.calculateFee(ticker, tradeValue)`

### Verify

```bash
mvn test
curl "http://localhost:8080/orders/AAPL/fee?tradeValue=10000"
```

(You'll need `mvn spring-boot:run` running in a separate terminal for the `curl` to work.)

## A question worth sitting with

`OrderServiceTest` never starts a Spring context, never touches `InMemoryOrderRepository`, and
runs in milliseconds. What would you have had to do differently to test `OrderService` if it
built its own `OrderRepository` internally (`new InMemoryOrderRepository()`) instead of taking
one through its constructor? (Compare to Sprint 5, Module 8's `BadOrderExecutor`.)

## Deliverable

`OrderService.java` and `OrderController.java`, both fully implemented.

## Acceptance criteria

- `mvn test` passes with 0 failures and 0 errors (2 tests)
- `OrderService` takes its `OrderRepository` through its constructor — no `new
  InMemoryOrderRepository()` anywhere inside it
- `curl "http://localhost:8080/orders/AAPL/fee?tradeValue=10000"` returns `10.0`
