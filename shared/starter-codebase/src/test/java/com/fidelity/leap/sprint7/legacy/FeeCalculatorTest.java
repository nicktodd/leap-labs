package com.fidelity.leap.sprint7.legacy;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

// This is the test Module 10 asked you to describe but couldn't write:
// fee logic, tested in isolation, with no file I/O, no static state, no
// CSV parsing in the way. Extract Method didn't just tidy the code up -
// it made a previously untestable rule directly testable.
class FeeCalculatorTest {

    @Test
    void equityTradesAreChargedTheEquityRate() {
        double fee = FeeCalculator.calculateFee("EQUITY", 10_000);

        assertEquals(10.0, fee, 0.0001);
    }

    @Test
    void bondTradesAreChargedTheOtherRate() {
        double fee = FeeCalculator.calculateFee("BOND", 10_000);

        assertEquals(5.0, fee, 0.0001);
    }

    @Test
    void unrecognisedTradeTypesFallBackToTheOtherRate() {
        // Locks in the legacy fallback behaviour explicitly, now that it's
        // a deliberate, named choice (OTHER_FEE_RATE) rather than a
        // coincidence between two separate if-branches.
        double fee = FeeCalculator.calculateFee("FUND", 10_000);

        assertEquals(5.0, fee, 0.0001);
    }
}
