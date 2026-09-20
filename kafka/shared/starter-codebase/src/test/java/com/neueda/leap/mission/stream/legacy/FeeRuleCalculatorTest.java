package com.neueda.leap.mission.stream.legacy;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

// Proves FeeRuleCalculator (Extract Interface + Replace Conditional with
// Polymorphism) produces EXACTLY the same results as FeeCalculator (Extract
// Method + Introduce Named Constant) for every trade type the real CSV
// contains. Same inputs, same outputs, two different internal designs -
// this is what "behaviour-preserving" looks like when comparing two
// refactors of the same logic, not just one refactor against the original.
class FeeRuleCalculatorTest {

    @Test
    void matchesFeeCalculatorForEquityTrades() {
        assertEquals(FeeCalculator.calculateFee("EQUITY", 10_000),
                FeeRuleCalculator.calculateFee("EQUITY", 10_000), 0.0001);
    }

    @Test
    void matchesFeeCalculatorForBondTrades() {
        assertEquals(FeeCalculator.calculateFee("BOND", 10_000),
                FeeRuleCalculator.calculateFee("BOND", 10_000), 0.0001);
    }

    @Test
    void matchesFeeCalculatorForUnrecognisedTradeTypes() {
        assertEquals(FeeCalculator.calculateFee("FUND", 10_000),
                FeeRuleCalculator.calculateFee("FUND", 10_000), 0.0001);
    }
}
