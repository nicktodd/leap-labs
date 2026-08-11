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

    @Nested
    @DisplayName("when the order is valid")
    class WhenOrderIsValid {

        @Test
        @DisplayName("accepts an order that stays within the risk limit")
        void acceptsAnOrderWithinTheLimit() {
            assertTrue(checker.canAcceptOrder(1000, 500, 2000));
        }

        @Test
        @DisplayName("accepts an order that lands exactly on the risk limit boundary")
        void acceptsAnOrderAtExactBoundary() {
            assertTrue(checker.canAcceptOrder(1000, 1000, 2000));
        }

        @ParameterizedTest
        @DisplayName("rejects orders that would push portfolio over the limit")
        @ValueSource(doubles = {1001, 5000, 99999})
        void rejectsOrdersOverLimit(double orderValue) {
            assertFalse(checker.canAcceptOrder(1000, orderValue, 2000));
        }

        @ParameterizedTest
        @DisplayName("handles various portfolio/order/limit combinations correctly")
        @CsvSource({
            "0, 100, 200, true",
            "100, 100, 200, true",
            "100, 101, 200, false",
            "0, 200, 200, true",
            "1, 200, 200, false"
        })
        void handlesVariousCombinations(double portfolioValue, double orderValue, double riskLimit, boolean expected) {
            assertEquals(expected, checker.canAcceptOrder(portfolioValue, orderValue, riskLimit));
        }
    }

    @Nested
    @DisplayName("when the input is invalid")
    class WhenInputIsInvalid {

        @Test
        @DisplayName("throws IllegalArgumentException when orderValue is zero")
        void throwsWhenOrderValueIsZero() {
            assertThrows(IllegalArgumentException.class, () -> checker.canAcceptOrder(0, 0, 1000));
        }

        @Test
        @DisplayName("throws IllegalArgumentException when orderValue is negative")
        void throwsWhenOrderValueIsNegative() {
            assertThrows(IllegalArgumentException.class, () -> checker.canAcceptOrder(0, -1, 1000));
        }

        @Test
        @DisplayName("throws IllegalArgumentException when riskLimit is negative, with correct message")
        void throwsWhenRiskLimitIsNegative() {
            assertAll(
                () -> assertThrows(IllegalArgumentException.class,
                    () -> checker.canAcceptOrder(0, 100, -1)),
                () -> {
                    Exception ex = assertThrows(IllegalArgumentException.class,
                        () -> checker.canAcceptOrder(0, 100, -1));
                    assertTrue(ex.getMessage().contains("riskLimit"));
                }
            );
        }
    }
}
