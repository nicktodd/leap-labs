package com.neueda.leap.sprint6;

// Kata A: add Bean Validation annotations to every field, matching
// Module 5's OpenAPI OrderRequest schema:
//   - ticker: required, non-blank
//   - instrumentType: required
//   - quantity: required, must be positive
//   - price: required, must be positive
//   - side: required
// See OrderRequestDtoTest.java for the exact behaviour expected - it uses
// jakarta.validation directly, no Spring context needed.
public record OrderRequestDto(
        String ticker,
        InstrumentType instrumentType,
        double quantity,
        double price,
        Side side
) {
}
