package com.neueda.leap.sprint5;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class HoldingUpdaterTest {

    private HoldingUpdater updater;

    @BeforeEach
    void setUp() {
        updater = new HoldingUpdater();
    }

    @Nested
    @DisplayName("when buying")
    class WhenBuying {

        @Test
        @DisplayName("increases the holding quantity by the order quantity")
        void increaseHoldingOnBuy() {
            Holding holding = new Holding(100);
            updater.applyOrder(holding, true, 10);
            assertEquals(110, holding.getQuantity());
        }

        @Test
        @DisplayName("throws IllegalArgumentException when quantity is negative")
        void throwsOnNegativeQuantity() {
            Holding holding = new Holding(100);
            assertThrows(IllegalArgumentException.class, () -> updater.applyOrder(holding, true, -5));
        }
    }

    @Nested
    @DisplayName("when selling")
    class WhenSelling {

        @Test
        @DisplayName("decreases the holding quantity by the order quantity")
        void decreaseHoldingOnSell() {
            Holding holding = new Holding(100);
            updater.applyOrder(holding, false, 10);
            assertEquals(90, holding.getQuantity());
        }

        @Test
        @DisplayName("throws when selling more than the current holding")
        void throwsWhenSellingMoreThanHeld() {
            Holding holding = new Holding(100);
            assertThrows(IllegalArgumentException.class, () -> updater.applyOrder(holding, false, 200));
        }
    }
}
