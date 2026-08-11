package com.neueda.leap.sprint5;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class DerivativeInstrumentTest {

    @Test
    void chargesFlatTwoPercent() {
        DerivativeInstrument derivative = new DerivativeInstrument("FTSE-FUT");

        assertEquals(400.0, derivative.calculateFee(20000), 0.0001);
    }

    @Test
    void feeScalesWithTradeValue() {
        DerivativeInstrument derivative = new DerivativeInstrument("FTSE-FUT");

        assertEquals(20.0, derivative.calculateFee(1000), 0.0001);
    }

    @Test
    void isAnInstrument() {
        DerivativeInstrument derivative = new DerivativeInstrument("FTSE-FUT");

        assertEquals("FTSE-FUT", derivative.getTicker());
    }
}
