# Service Boundary Sketch — Order Processing & Settlement Engine

Pair names: Zack Todd

## What comes in over the wire?

An incoming HTTP POST request needs:
- `clientId` (String) — who is submitting the order
- `ticker` (String) — the instrument being bought/sold
- `instrumentType` (String) — "EQUITY", "BOND", "FUND", "CRYPTO" — needed to construct the right Instrument subclass
- `quantity` (double) — number of units
- `price` (double) — price per unit
- `side` (String) — "BUY" or "SELL"

Compare to Sprint 5's `IncomingOrder`: same fields, but in Sprint 5 these came from a CSV line. Here they come as JSON in an HTTP request body. The JWT in the `Authorization` header implicitly carries the authenticated user's identity — the `clientId` in the body should be validated against it.

## What goes out?

**Accepted order response (HTTP 200):**
```json
{
  "status": "ACCEPTED",
  "clientId": "C001",
  "ticker": "AAPL",
  "fee": 12.50
}
```

**Rejected order response (HTTP 422 Unprocessable Entity):**
```json
{
  "status": "REJECTED",
  "clientId": "C001",
  "ticker": "AAPL",
  "reason": "cannot sell more than the current holding"
}
```

## What does the service need to talk to, that Sprint 5 didn't?

1. **PostgreSQL** — client and portfolio data is now persisted in the Sprint 3 schema, not held in an in-memory `Map<String, Client>`. The service needs a database connection (MyBatis) to load holdings and client risk limits per request.
2. **JWT auth service** — every request must carry a valid JWT issued by the Node.js auth service. The service needs to validate the token on every incoming request before processing the order.
3. **Docker / container runtime** — the service runs containerised, so it needs to be aware of environment-variable-based config (datasource URL, auth service URL, JWT secret) rather than hardcoded values.

## What stays entirely internal?

Sprint 5 classes that should never be visible outside the service boundary:
- `OrderProcessingEngine` — the orchestrator is an internal implementation detail
- `OrderValidator` — validation rules are internal business logic
- `HoldingUpdater` — how holdings are mutated is nobody else's concern
- `SettlementReport` — internal report format; external callers get individual order responses, not a batch report
- `ValidationResult` — internal value type used between validator and engine
- `Portfolio`, `Holding` — internal domain model; callers get back a result, not the updated portfolio state

## Rough sketch

```
Client (HTTP) 
    --> [POST /orders]  + JWT in Authorization header
    --> OrderController (Spring MVC)
    --> JwtFilter (validates token against auth service)
    --> OrderService (wraps Sprint 5's OrderProcessingEngine)
    --> MyBatis DAOs (load Client + Holding from Postgres)
    --> OrderProcessingEngine (Sprint 5, unchanged)
    --> response: AcceptedOrderResponse or RejectedOrderResponse (JSON)
```
