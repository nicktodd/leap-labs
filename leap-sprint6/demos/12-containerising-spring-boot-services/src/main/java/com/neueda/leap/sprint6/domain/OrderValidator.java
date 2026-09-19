package com.neueda.leap.sprint6.domain;

// Carried over from Sprint 5, Module 13 UNCHANGED - not one line of business logic
// in this package was rewritten for Sprint 6. Only what's around it changed: HTTP
// instead of a CSV file, Postgres instead of an in-memory Map, a JWT instead of no
// auth at all. See shared/mission-brief.md, "What Changes, and What Doesn't".
//
// This is the END STATE of a live TDD session built from Sprint 5 Module 3's
// mission-brief requirement 3 - see Sprint 5's demo-guide.md for the five
// red-green-refactor cycles that actually built it.
public class OrderValidator {

    public ValidationResult validate(OrderRequest request, double currentHoldingQuantity,
                                      double currentPortfolioValue, double riskLimit) {
        if (request.getQuantity() <= 0) {
            return ValidationResult.invalid("quantity must be positive");
        }
        if (request.getPrice() <= 0) {
            return ValidationResult.invalid("price must be positive");
        }
        if (!request.isBuy() && request.getQuantity() > currentHoldingQuantity) {
            return ValidationResult.invalid("cannot sell more than the current holding");
        }
        if (request.isBuy() && currentPortfolioValue + request.tradeValue() > riskLimit) {
            return ValidationResult.invalid("would exceed the client's risk limit");
        }
        return ValidationResult.valid();
    }
}
