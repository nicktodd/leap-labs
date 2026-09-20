package com.neueda.leap.mission.engine;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

// The final test suite from the live TDD session - each test here was added ONE
// AT A TIME, in this order, with a run in between each. See demo-guide.md.
class TickerValidatorTest {

    @Test
    void acceptsAStandardTicker() {
        assertTrue(new TickerValidator().isValid("AAPL"));
    }

    @Test
    void rejectsAnEmptyString() {
        assertFalse(new TickerValidator().isValid(""));
    }

    @Test
    void rejectsLowercase() {
        assertFalse(new TickerValidator().isValid("aapl"));
    }

    @Test
    void rejectsMoreThanFiveLetters() {
        assertFalse(new TickerValidator().isValid("TOOLONG"));
    }

    @Test
    void rejectsDigits() {
        assertFalse(new TickerValidator().isValid("AAPL1"));
    }

    @Test
    void acceptsTheLondonSuffix() {
        assertTrue(new TickerValidator().isValid("VOD.L"));
    }

    @Test
    void rejectsNull() {
        assertFalse(new TickerValidator().isValid(null));
    }
}
