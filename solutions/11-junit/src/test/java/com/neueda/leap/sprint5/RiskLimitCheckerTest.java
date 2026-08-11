package com.neueda.leap.sprint5;

import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("RiskLimitChecker")
class RiskLimitCheckerTest {

    private RiskLimitChecker checker;

    @BeforeEach
    void setUp() {
        checker = new RiskLimitChecker();
    }

    @Test
    @DisplayName("accepts an order that stays within the risk limit")
    void acceptsAnOrderWithinTheLimit() {
        assertTrue(checker.canAcceptOrder(1000, 500, 2000));
    }

    @ParameterizedTest
    @ValueSource(doubles = {1500, 2000, 10000})
    @DisplayName("rejects an order that would push the portfolio over the limit")
    void rejectsAnOrderOverTheLimit(double orderValue) {
        assertFalse(checker.canAcceptOrder(1000, orderValue, 2000));
    }

    @ParameterizedTest
    @CsvSource({
            "1000, 500, 2000, true",
            "1000, 1000, 2000, true",   // exact boundary: 1000 + 1000 == 2000
            "1000, 1000.01, 2000, false",
            "0, 5000, 5000, true",
            "4999, 2, 5000, false"
    })
    @DisplayName("accepts or rejects correctly across a range of portfolio/order/limit combinations")
    void acceptsOrRejectsAcrossCombinations(double currentPortfolioValue, double orderValue,
                                             double riskLimit, boolean expected) {
        assertEquals(expected, checker.canAcceptOrder(currentPortfolioValue, orderValue, riskLimit));
    }

    @Nested
    @DisplayName("when the input is invalid")
    class WhenInputIsInvalid {

        @Test
        @DisplayName("a zero or negative order value throws")
        void zeroOrNegativeOrderValueThrows() {
            IllegalArgumentException exception = assertThrows(
                    IllegalArgumentException.class,
                    () -> checker.canAcceptOrder(1000, 0, 2000)
            );

            assertAll("exception details",
                    () -> assertNotNull(exception.getMessage()),
                    () -> assertTrue(exception.getMessage().contains("orderValue"))
            );
        }

        @Test
        @DisplayName("a negative risk limit throws")
        void negativeRiskLimitThrows() {
            IllegalArgumentException exception = assertThrows(
                    IllegalArgumentException.class,
                    () -> checker.canAcceptOrder(1000, 500, -1)
            );

            assertTrue(exception.getMessage().contains("riskLimit"));
        }
    }

    @Nested
    @DisplayName("when the order is exactly at the boundary")
    class WhenOrderIsAtTheBoundary {

        @Test
        @DisplayName("a portfolio starting at zero, with an order equal to the limit, is accepted")
        void zeroStartExactlyAtLimitIsAccepted() {
            assertTrue(checker.canAcceptOrder(0, 5000, 5000));
        }

        @Test
        @DisplayName("one cent over the limit is rejected")
        void oneCentOverTheLimitIsRejected() {
            assertFalse(checker.canAcceptOrder(0, 5000.01, 5000));
        }
    }
}
