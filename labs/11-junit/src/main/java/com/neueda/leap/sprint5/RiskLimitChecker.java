package com.neueda.leap.sprint5;

// Given, fully implemented - your job this module is to TEST this thoroughly, not
// to change it. See labs/11-junit/README.md.
public class RiskLimitChecker {

    public boolean canAcceptOrder(double currentPortfolioValue, double orderValue, double riskLimit) {
        if (orderValue <= 0) {
            throw new IllegalArgumentException("orderValue must be positive");
        }
        if (riskLimit < 0) {
            throw new IllegalArgumentException("riskLimit cannot be negative");
        }
        return currentPortfolioValue + orderValue <= riskLimit;
    }
}
