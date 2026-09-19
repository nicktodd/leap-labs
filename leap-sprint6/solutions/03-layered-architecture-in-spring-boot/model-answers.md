# Model Answers — Layered Architecture in Spring Boot

## Why the constructor is the actual point of this kata

It's tempting to think Kata A is "implement one line of arithmetic." The line
`return tradeValue * repository.findFeeRate(ticker);` is trivial. The constructor is not — it's
the mechanism that makes `OrderServiceTest` possible at all. Without a constructor that accepts
an `OrderRepository`, there is no way to hand `OrderService` a mock instead of a real repository,
and the test would either need a running Spring context (slow, heavyweight) or would have to
accept whatever `InMemoryOrderRepository` actually does (no longer testing `OrderService` in
isolation).

## What breaks if `OrderService` builds its own repository

```java
public class OrderService {
    private final OrderRepository repository = new InMemoryOrderRepository();
    ...
}
```

This compiles and runs identically from `OrderController`'s point of view — Spring doesn't even
need to know about it. But `OrderServiceTest` becomes impossible to write as a true unit test:
every test would exercise `InMemoryOrderRepository`'s real lookup logic too, and there would be
no way to test what happens when `findFeeRate` throws, without adding a ticker that's guaranteed
to be missing from the real map. This is exactly Sprint 5 Module 8's `BadOrderExecutor` problem,
recurring in a Spring context.

## Why `@GetMapping` uses `@RequestParam double`, not a request body

`GET` requests conventionally don't have a body — query parameters (`?tradeValue=10000`) are the
normal way to pass simple values to a `GET` endpoint. Module 6 (DTOs & Request Validation)
introduces request bodies, for `POST`/`PUT` endpoints that create or modify something — order
submission itself will use a DTO, not query parameters, because it's meaningfully more than one
or two primitive values.

## What this sets up for Module 7

`OrderRepository` is the exact interface Module 7's MyBatis mapper will implement for real,
against the Sprint 3 Postgres schema. `OrderService` and `OrderController` won't need a single
line changed when that happens — this is the whole point of building the interface first,
against a fake implementation, before the real one exists.
