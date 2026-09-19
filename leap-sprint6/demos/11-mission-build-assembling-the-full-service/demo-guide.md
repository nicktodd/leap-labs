# Module 11 Demo Guide — Mission Build: Assembling the Full Service

Nothing new gets built today. Every piece already exists, already works, and already has its own
module behind it. Today is entirely about the seam between them.

## Start Everything

```bash
# Local mission Postgres database from Module 7 just needs to be running
cd shared/auth-stub && npm start   # Module 9, http://localhost:4000
cd demos/11-mission-build-assembling-the-full-service && mvn spring-boot:run
```

## Walk the Whole Request, Live

```bash
TOKEN=$(curl -s -X POST http://localhost:4000/login -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"mission123"}' | ...extract .token...)

curl -s -H "Authorization: Bearer $TOKEN" -X POST http://localhost:8080/accounts/1/orders \
  -H "Content-Type: application/json" \
  -d '{"ticker":"ULVR.L","instrumentType":"EQUITY","quantity":100,"price":40.0,"side":"BUY"}'
```

Then, in a second terminal, prove it actually landed in the database:

```bash
psql -U postgres -h localhost -d mission -c \
  "SELECT h.account_id, i.ticker, h.quantity FROM holdings h JOIN instruments i ON h.instrument_id=i.instrument_id WHERE h.account_id=1 AND i.ticker='ULVR.L';"
```

**This is the moment to slow down.** One HTTP request just: passed through JWT validation
(Module 9) against a real Node.js service; had its body validated by Bean Validation (Module 6);
was looked up and updated against real Postgres rows (Module 7); was checked against Sprint 5's
`OrderValidator` — the exact same class, unmodified, that Sprint 5 tested against a CSV file six
weeks ago; and would have produced a clean, structured error at ANY of those steps if something
had gone wrong (Module 10).

## Open `OrderController` and Count What's NOT New

Walk through `submitOrder` line by line and name, out loud, which module each call belongs to:

- `accountMapper.findInstrument(...)` / `findHolding(...)` — Module 7
- `@Valid @RequestBody OrderRequestDto` — Module 6
- `@AuthenticationPrincipal Jwt jwt` — Module 9 (never read directly here, but its presence is
  what SecurityConfig gates on)
- `orderValidator.validate(...)`, `holdingUpdater.applyOrder(...)`, `instrumentFactory.create(...)`
  — Sprint 5, Module 13, genuinely unchanged
- Every `throw` — Module 10 catches every one of them

**The only genuinely new code in this whole module is the orchestration itself** — deciding what
order to call things in, and how to translate between the domain layer's vocabulary and the HTTP
layer's.

## The One Deliberate Simplification, Named Honestly

Point at `currentPortfolioValue = currentQuantity * dto.price()`. `OrderValidator`'s real
signature wants a client's whole portfolio value, priced at live market rates — building that
properly needs a market-data feed this sprint never scoped. Say explicitly: this is a named
trade-off, not a bug, and a real team would document it exactly this way rather than leave it
looking like an oversight.

## Break Something, on Purpose

Pick one and show it live:
- Remove the `Authorization` header → `401`, before `submitOrder` ever runs
- Send a `SELL` for more than the account holds → `422`, from `OrderValidator`'s own logic
- Use a ticker that doesn't exist → `404`
- Send `quantity: -5` → `400` with a field-level message

None of these are new demos — they're Modules 6, 9, and 10's behaviour, now all reachable through
one real endpoint at once.

## Transition to the Lab

Learners implement `submitOrder` from seven `TODO`s, with every dependency (mappers, security,
error handling, and all of Sprint 5's domain logic) given and already working — verified against
a pre-written integration test hitting the real Postgres container and the real running auth stub.
