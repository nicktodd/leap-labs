package com.neueda.leap.sprint6;

import jakarta.validation.ConstraintViolation;
import jakarta.validation.Validation;
import jakarta.validation.Validator;
import jakarta.validation.ValidatorFactory;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

// No Spring context - jakarta.validation's own Validator runs the annotations
// directly. This is exactly the same idea as Sprint 5's isolated unit tests:
// checking OrderRequestDto's validation rules doesn't require starting a web
// server.
class OrderRequestDtoTest {

    private static ValidatorFactory factory;
    private static Validator validator;

    @BeforeAll
    static void setUpValidator() {
        factory = Validation.buildDefaultValidatorFactory();
        validator = factory.getValidator();
    }

    @AfterAll
    static void closeFactory() {
        factory.close();
    }

    @Test
    void aFullyValidRequestHasNoViolations() {
        OrderRequestDto request = new OrderRequestDto("AAPL", InstrumentType.EQUITY, 100, 150.00, Side.BUY);

        Set<ConstraintViolation<OrderRequestDto>> violations = validator.validate(request);

        assertTrue(violations.isEmpty());
    }

    @Test
    void aBlankTickerIsRejected() {
        OrderRequestDto request = new OrderRequestDto("", InstrumentType.EQUITY, 100, 150.00, Side.BUY);

        Set<ConstraintViolation<OrderRequestDto>> violations = validator.validate(request);

        assertEquals(1, violations.size());
        assertEquals("ticker", violations.iterator().next().getPropertyPath().toString());
    }

    @Test
    void aNullInstrumentTypeIsRejected() {
        OrderRequestDto request = new OrderRequestDto("AAPL", null, 100, 150.00, Side.BUY);

        Set<ConstraintViolation<OrderRequestDto>> violations = validator.validate(request);

        assertEquals(1, violations.size());
        assertEquals("instrumentType", violations.iterator().next().getPropertyPath().toString());
    }

    @Test
    void aNonPositiveQuantityIsRejected() {
        OrderRequestDto request = new OrderRequestDto("AAPL", InstrumentType.EQUITY, -5, 150.00, Side.BUY);

        Set<ConstraintViolation<OrderRequestDto>> violations = validator.validate(request);

        assertEquals(1, violations.size());
        assertEquals("quantity", violations.iterator().next().getPropertyPath().toString());
    }

    @Test
    void aNonPositivePriceIsRejected() {
        OrderRequestDto request = new OrderRequestDto("AAPL", InstrumentType.EQUITY, 100, 0, Side.BUY);

        Set<ConstraintViolation<OrderRequestDto>> violations = validator.validate(request);

        assertEquals(1, violations.size());
        assertEquals("price", violations.iterator().next().getPropertyPath().toString());
    }

    @Test
    void aNullSideIsRejected() {
        OrderRequestDto request = new OrderRequestDto("AAPL", InstrumentType.EQUITY, 100, 150.00, null);

        Set<ConstraintViolation<OrderRequestDto>> violations = validator.validate(request);

        assertEquals(1, violations.size());
        assertEquals("side", violations.iterator().next().getPropertyPath().toString());
    }

    @Test
    void multipleViolationsAreAllReported() {
        OrderRequestDto request = new OrderRequestDto("", null, -5, -1, null);

        Set<ConstraintViolation<OrderRequestDto>> violations = validator.validate(request);

        assertEquals(5, violations.size());
    }
}
