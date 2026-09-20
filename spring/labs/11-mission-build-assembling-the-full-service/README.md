# Module 11 Lab - Mission Build: Assembling the Full Service

## Objectives

By the end of this lab you will have:

- Assembled six modules' worth of work - REST design, DTOs and validation, MyBatis persistence,
  JWT security, and centralised error handling - into one working endpoint
- Reused the Java week's `OrderValidator`, `HoldingUpdater`, and fee-calculation hierarchy completely
  unchanged, wired against real HTTP, real Postgres, and real security instead of a CSV file and
  an in-memory map

## Setup

- Java 21, Maven, and Node.js installed
- Your local `mission` Postgres database from Module 7, seeded with the Data week's enterprise
  schema (nothing to start - a local Postgres server just needs to be running)
- The shared auth stub running (leave it running for the whole lab):

  ```bash
  cd shared/auth-stub && npm start    # http://localhost:4000
  ```
- Given, don't modify: everything in `domain/` (the Java week's business logic, unchanged),
  `AccountMapper.java`/`.xml`, `SecurityConfig.java`, `GlobalExceptionHandler.java`,
  `ErrorResponse.java`, `OrderRejectedException.java`, `OrderRequestDto.java`,
  `OrderResponseDto.java`, `InstrumentRow.java`, `HoldingRow.java`, `application.properties`
- `mvn test` runs `OrderIntegrationTest.java` - pre-written, hits the real running service,
  real Postgres, and a real token from the real running auth stub

## Task

Implement `OrderController.submitOrder`, following the seven `TODO`s in the file:

1. Look up the instrument by ticker via `accountMapper.findInstrument(...)` - `null` means the
   ticker doesn't exist.
2. Look up the account's existing holding via `accountMapper.findHolding(...)` - `null` means no
   current position (treat as quantity `0.0`).
3. Compute `currentPortfolioValue` as `currentQuantity * dto.price()` - a deliberate
   simplification; see the demo guide for why.
4. Build a `domain.OrderRequest` from the DTO and call `orderValidator.validate(...)` - the Java
   week's `OrderValidator`, completely unchanged. If the result isn't valid, throw
   `OrderRejectedException`.
5. Build a `domain.Holding`, call `holdingUpdater.applyOrder(...)`, then persist the new quantity
   - insert if there was no existing holding, update if there was.
6. Use `instrumentFactory.create(...)` to get the right `Instrument` subtype, and call
   `calculateFee(...)` on it.
7. Return `200 OK` with an `OrderResponseDto`.

### Verify

```bash
mvn test
```

```bash
mvn spring-boot:run
```

```bash
TOKEN=$(curl -s -X POST http://localhost:4000/login -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"mission123"}' | ...extract .token...)

# 200 - a real BUY, persisted to Postgres
curl -s -H "Authorization: Bearer $TOKEN" -X POST http://localhost:8080/accounts/1/orders \
  -H "Content-Type: application/json" \
  -d '{"ticker":"ULVR.L","instrumentType":"EQUITY","quantity":10,"price":40.0,"side":"BUY"}'

# 401 - no token at all
curl -si -X POST http://localhost:8080/accounts/1/orders \
  -H "Content-Type: application/json" \
  -d '{"ticker":"ULVR.L","instrumentType":"EQUITY","quantity":10,"price":40.0,"side":"BUY"}'
```

## Deliverable

`OrderController.java`, fully implemented.

## Acceptance criteria

- `mvn test` passes with 0 failures and 0 errors (5 tests)
- A request with no token is rejected before your code runs at all
- A valid order is accepted, its fee correctly calculated, and the new holding quantity actually
  persisted in Postgres
- Selling more than the account holds, or trading an unknown ticker, produce the correct status
  code and error shape - not a raw 500
