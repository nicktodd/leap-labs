package com.neueda.leap.sprint5;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

@DisplayName("HoldingUpdater")
class HoldingUpdaterTest {

    private final HoldingUpdater updater = new HoldingUpdater();

    @Nested
    @DisplayName("when buying")
    class WhenBuying {

        @Test
        @DisplayName("increases the holding's quantity")
        void increasesQuantity() {
            Holding holding = new Holding(100);

            updater.applyOrder(holding, true, 10);

            assertEquals(110.0, holding.getQuantity(), 0.0001);
        }

        @Test
        @DisplayName("rejects a non-positive quantity")
        void rejectsNonPositiveQuantity() {
            Holding holding = new Holding(100);

            assertThrows(IllegalArgumentException.class, () -> updater.applyOrder(holding, true, -5));
        }
    }

    @Nested
    @DisplayName("when selling")
    class WhenSelling {

        @Test
        @DisplayName("decreases the holding's quantity")
        void decreasesQuantity() {
            Holding holding = new Holding(100);

            updater.applyOrder(holding, false, 10);

            assertEquals(90.0, holding.getQuantity(), 0.0001);
        }

        @Test
        @DisplayName("rejects selling more than the current holding")
        void rejectsSellingMoreThanHeld() {
            Holding holding = new Holding(100);

            assertThrows(IllegalArgumentException.class, () -> updater.applyOrder(holding, false, 200));
        }
    }
}
