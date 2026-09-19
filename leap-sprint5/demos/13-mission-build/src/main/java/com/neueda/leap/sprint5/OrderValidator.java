package com.neueda.leap.sprint5;

// This is the END STATE of a live TDD session built from Module 3's mission-brief
// requirement 3 - see demo-guide.md for the five red-green-refactor cycles that
// actually built it.
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
