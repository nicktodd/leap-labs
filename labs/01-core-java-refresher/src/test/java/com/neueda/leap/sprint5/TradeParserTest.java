package com.neueda.leap.sprint5;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class TradeParserTest {

    private final TradeParser parser = new TradeParser();

    @Test
    void parsesAWellFormedLine() throws MalformedTradeException {
        Trade trade = parser.parse("T0001,Alice Chen,AAPL,120,185.32,BUY");
        assertEquals("T0001", trade.getTradeId());
        assertEquals("Alice Chen", trade.getClientName());
        assertEquals("AAPL", trade.getInstrument());
        assertEquals(120.0, trade.getQuantity());
        assertEquals(185.32, trade.getPrice());
        assertEquals("BUY", trade.getSide());
    }

    @Test
    void throwsMalformedTradeExceptionForNonPositiveQuantity() {
        assertThrows(MalformedTradeException.class,
                () -> parser.parse("T0002,Ben Whitfield,MSFT,-5,402.11,BUY"));
    }

    @Test
    void throwsMalformedTradeExceptionForNonPositivePrice() {
        assertThrows(MalformedTradeException.class,
                () -> parser.parse("T0003,Alice Chen,AAPL,40,0,SELL"));
    }

    @Test
    void letsNumberFormatExceptionPropagateForNonNumericQuantity() {
        // Unchecked - NumberFormatException is a RuntimeException, so no "throws"
        // is needed on this test method, and parse() shouldn't catch it either.
        assertThrows(NumberFormatException.class,
                () -> parser.parse("T0004,Alice Chen,AAPL,not-a-number,186.10,BUY"));
    }
}
