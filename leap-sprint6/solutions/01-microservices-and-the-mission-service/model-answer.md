# Model Answer — Service Boundary Sketch

A defensible sketch, not the only correct one — compare your own reasoning, not just the final
answer.

## What comes in over the wire?

A JSON request body, roughly matching Sprint 5's `IncomingOrder` fields, plus the client
identifying itself via the JWT (not in the body — in an `Authorization: Bearer <token>` header,
Module 9's territory):

```json
{
  "ticker": "AAPL",
  "instrumentType": "EQUITY",
  "quantity": 100,
  "price": 150.00,
  "side": "BUY"
}
```

Note `clientId` is deliberately **not** in the body — it comes from the validated JWT, so a
client can't submit an order pretending to be someone else. That's a genuine security
requirement Sprint 5 never had to consider, because everything ran as one trusted process.

## What goes out?

**Accepted:**
```json
{
  "status": "ACCEPTED",
  "fee": 15.0
}
```

**Rejected:**
```json
{
  "status": "REJECTED",
  "reason": "would exceed the client's risk limit"
}
```

This maps directly onto Sprint 5's `ValidationResult` and `SettlementReport` — the shape of the
data barely changes, only how it's delivered (HTTP response instead of a report line).

## What does the service need to talk to, that Sprint 5 didn't?

- **A database** (Postgres, the Sprint 3 schema) — client, portfolio, and holding data can't live
  in an in-memory `Map` that resets every time the process restarts
- **An auth service** (the Node.js stub, Module 9) — to validate the JWT and know which client is
  making the request

## What stays entirely internal?

`OrderValidator`, `HoldingUpdater`, `Portfolio`, `Holding`, and the `Instrument`/`Feeable`
hierarchy should never be visible outside this service — nothing about them belongs in a REST
contract. Only the request/response shapes above are the service's public surface. This is
directly the DTO pattern Module 6 introduces: the API contract and the internal domain model are
different things, deliberately.

## Rough sketch

```
POST /orders (JWT in header)
        |
        v
  [Controller] -- validate JWT --> [Node Auth Service]
        |
        v
  [DTO -> internal request]
        |
        v
  [OrderValidator] -- reads client/holding --> [Postgres, via MyBatis]
        |
    valid? --no--> 400-ish response, reason
        |
       yes
        |
        v
  [OrderProcessingEngine / HoldingUpdater] -- writes updated holding --> [Postgres]
        |
        v
  [Response DTO] --> client
```
