# Module 11 - Model Answers & Notes

## `OrderController.submitOrder`

```java
@PostMapping
public ResponseEntity<OrderResponseDto> submitOrder(@PathVariable int accountId,
                                                      @Valid @RequestBody OrderRequestDto dto,
                                                      @AuthenticationPrincipal Jwt jwt) {
    InstrumentRow instrument = accountMapper.findInstrument(dto.ticker());
    if (instrument == null) {
        throw new NoSuchElementException("no such instrument: " + dto.ticker());
    }

    HoldingRow existingHolding = accountMapper.findHolding(accountId, dto.ticker());
    double currentQuantity = existingHolding == null ? 0.0 : existingHolding.getQuantity();
    double currentPortfolioValue = currentQuantity * dto.price();

    OrderRequest domainRequest = new OrderRequest(dto.quantity(), dto.price(), dto.isBuy());
    ValidationResult result = orderValidator.validate(
            domainRequest, currentQuantity, currentPortfolioValue, RISK_LIMIT);

    if (!result.isValid()) {
        throw new OrderRejectedException(result.getReason());
    }

    Holding holding = new Holding(currentQuantity);
    holdingUpdater.applyOrder(holding, dto.isBuy(), dto.quantity());

    if (existingHolding == null) {
        accountMapper.insertHolding(accountId, instrument.getInstrumentId(), holding.getQuantity());
    } else {
        accountMapper.updateHoldingQuantity(existingHolding.getHoldingId(), holding.getQuantity());
    }

    Instrument instrumentObj = instrumentFactory.create(
            instrument.getAssetClass().toUpperCase(), instrument.getTicker());
    double fee = instrumentObj.calculateFee(domainRequest.tradeValue());

    return ResponseEntity.ok(new OrderResponseDto("ACCEPTED", fee, holding.getQuantity()));
}
```

## Why `currentPortfolioValue` Is Just `currentQuantity * dto.price()`

`OrderValidator.validate` (from the Java week, unchanged) takes a `currentPortfolioValue` parameter meant to
represent the client's whole portfolio, valued at current market prices. Building that properly
would mean summing every holding across every account for the client, each priced from a live
market feed - a genuine feature this week never scoped. Using the single holding being traded,
priced at the incoming order's own price, keeps `OrderValidator`'s real signature and real
risk-limit logic genuinely exercised against real data, without inventing a market-data service
that doesn't exist. Worth saying explicitly to learners: this is a named, deliberate
simplification, not a bug - the kind of trade-off real projects document and revisit later, not
quietly leave unexplained.

## Why the Instrument Lookup Happens Before the Holding Lookup

If `dto.ticker()` doesn't exist in `instruments` at all, there's no point querying `holdings` for
it - a `404` is the right answer immediately. Ordering the checks this way means the error a
client gets back always reflects the *first* thing actually wrong with their request, not
whichever check happened to run last.

## `instrument.getAssetClass().toUpperCase()`

The Data week's schema's `asset_class` column stores `'Equity'`, `'Bond'`, `'Fund'`, `'Cash'`
(capitalised, from `enterprise-schema.sql`'s own `CHECK` constraint). `InstrumentFactory` (from
the Java week, unchanged) matches on `"EQUITY"`, `"BOND"`, `"FUND"` - uppercase, because that's
what the Java week's order files used. Neither side was "wrong" when it was written; they simply
came from different weeks with different conventions. `.toUpperCase()` here is the one-line
adapter that lets two
pieces of genuinely unrelated code work together without either one changing. (An account holding
a `'Cash'` instrument would throw `IllegalArgumentException` here, caught by the catch-all as a
`500` - a real edge case this demo doesn't handle further, worth a mention if a learner asks.)

## What Assembly Actually Means

Every module this week built a piece in isolation: Module 4 designed the shape of the URL,
Module 6 built the DTO, Module 7 built the mapper, Module 9 built the security, Module 10 built
the error handling. None of those modules' code changed today - `submitOrder` is the *only* new
logic, and it's entirely orchestration: call this, then that, in the right order, translating
between the domain layer's vocabulary (`Holding`, `OrderRequest`, `ValidationResult`) and the HTTP
layer's vocabulary (DTOs, status codes, exceptions). That's what "assembling a service" means in
practice - not a big rewrite, a thin controller method that knows how to introduce pieces that
already work to each other.
