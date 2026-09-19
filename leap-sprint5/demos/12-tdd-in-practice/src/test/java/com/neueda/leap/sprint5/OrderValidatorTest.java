package com.neueda.leap.sprint5;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

// The final test suite from the live TDD session - each test was added ONE AT A
// TIME, in this order. See demo-guide.md for the cycle-by-cycle build.
@DisplayName("OrderValidator")
class OrderValidatorTest {

    private final OrderValidator validator = new OrderValidator();

    @Test
    @DisplayName("accepts a straightforward, well-within-limits buy order")
    void acceptsAValidBuyOrder() {
        OrderRequest request = new OrderRequest(10, 100, true);

        ValidationResult result = validator.validate(request, 0, 0, 5000);

        assertTrue(result.isValid());
    }

    @Nested
    @DisplayName("when the basic order shape is invalid")
    class WhenOrderShapeIsInvalid {

        @Test
        @DisplayName("rejects a zero or negative quantity")
        void rejectsNonPositiveQuantity() {
            OrderRequest request = new OrderRequest(-5, 100, true);

            ValidationResult result = validator.validate(request, 0, 0, 5000);

            assertFalse(result.isValid());
            assertEquals("quantity must be positive", result.getReason());
        }

        @Test
        @DisplayName("rejects a zero or negative price")
        void rejectsNonPositivePrice() {
            OrderRequest request = new OrderRequest(10, -1, true);

            ValidationResult result = validator.validate(request, 0, 0, 5000);

            assertFalse(result.isValid());
            assertEquals("price must be positive", result.getReason());
        }
    }

    @Nested
    @DisplayName("when selling")
    class WhenSelling {

        @Test
        @DisplayName("rejects selling more than the current holding")
        void rejectsSellingMoreThanHeld() {
            OrderRequest request = new OrderRequest(100, 50, false);

            ValidationResult result = validator.validate(request, 40, 0, 5000);

            assertFalse(result.isValid());
            assertEquals("cannot sell more than the current holding", result.getReason());
        }

        @Test
        @DisplayName("accepts selling up to exactly the current holding")
        void acceptsSellingExactlyWhatIsHeld() {
            OrderRequest request = new OrderRequest(40, 50, false);

            ValidationResult result = validator.validate(request, 40, 0, 5000);

            assertTrue(result.isValid());
        }
    }

    @Nested
    @DisplayName("when buying")
    class WhenBuying {

        @Test
        @DisplayName("rejects a buy that would exceed the risk limit")
        void rejectsBuyOverRiskLimit() {
            OrderRequest request = new OrderRequest(100, 60, true);

            ValidationResult result = validator.validate(request, 0, 4000, 5000);

            assertFalse(result.isValid());
            assertEquals("would exceed the client's risk limit", result.getReason());
        }

        @Test
        @DisplayName("accepts a buy that lands exactly on the risk limit")
        void acceptsBuyExactlyAtRiskLimit() {
            OrderRequest request = new OrderRequest(20, 50, true);

            ValidationResult result = validator.validate(request, 4000, 4000, 5000);

            assertTrue(result.isValid());
        }
    }
}
