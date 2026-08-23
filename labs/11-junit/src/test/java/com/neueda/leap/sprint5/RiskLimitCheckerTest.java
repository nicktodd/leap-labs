package com.neueda.leap.sprint5;

import org.junit.jupiter.api.*;

// Build this out following labs/11-junit/README.md. One example test is given to
// show the convention (naming, @DisplayName) - add the rest yourself.
@DisplayName("RiskLimitChecker")
class RiskLimitCheckerTest {

    @Test
    @DisplayName("accepts an order that stays within the risk limit")
    void acceptsAnOrderWithinTheLimit() {
        RiskLimitChecker checker = new RiskLimitChecker();

        boolean accepted = checker.canAcceptOrder(1000, 500, 2000);

        Assertions.assertTrue(accepted);
    }

    // TODO: the rest of the suite - see the checklist in README.md.
}
