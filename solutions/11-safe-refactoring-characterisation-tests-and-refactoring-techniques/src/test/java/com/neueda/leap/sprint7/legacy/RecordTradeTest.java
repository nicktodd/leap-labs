package com.neueda.leap.sprint7.legacy;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

// Unlike FeeCalculatorTest, this test CANNOT treat recordTrade() as a pure
// function - it reads and writes TradeReportGenerator's static tot/f/c
// fields directly. This test has to manually reset that shared state before
// each run, which is exactly the friction a pure function like
// FeeCalculator never has. Extract Method moved the code; it did not
// remove the static-state problem underneath it.
class RecordTradeTest {

    @BeforeEach
    void resetSharedState() {
        TradeReportGenerator.tot.clear();
        TradeReportGenerator.f.clear();
        TradeReportGenerator.c = 0;
    }

    @Test
    void secondTradeForTheSameTickerAccumulatesOntoTheFirst() {
        TradeReportGenerator.recordTrade("AAPL", 1000.0, 1.0);
        TradeReportGenerator.recordTrade("AAPL", 500.0, 0.5);

        assertEquals(1500.0, TradeReportGenerator.tot.get("AAPL"), 0.0001);
        assertEquals(1.5, TradeReportGenerator.f.get("AAPL"), 0.0001);
        assertEquals(2, TradeReportGenerator.c);
    }

    @Test
    void differentTickersAreTrackedSeparately() {
        TradeReportGenerator.recordTrade("AAPL", 1000.0, 1.0);
        TradeReportGenerator.recordTrade("VOD.L", 200.0, 0.1);

        assertEquals(1000.0, TradeReportGenerator.tot.get("AAPL"), 0.0001);
        assertEquals(200.0, TradeReportGenerator.tot.get("VOD.L"), 0.0001);
        assertEquals(2, TradeReportGenerator.c);
    }
}
