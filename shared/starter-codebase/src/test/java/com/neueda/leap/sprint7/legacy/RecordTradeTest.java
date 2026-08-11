package com.neueda.leap.sprint7.legacy;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Lab 11, Part C: tests for the extracted recordTrade() method.
 *
 * Part C written answer: unlike FeeCalculator, recordTrade() still cannot be
 * tested in full isolation because it reads and writes the static fields
 * tot, f, and c on TradeReportGenerator directly — those fields are shared
 * mutable state, not parameters or return values. Extract Method moved the
 * code into a named method, but it did NOT remove the dependency on global
 * state. Any test that calls recordTrade() must manually reset tot, f, and c
 * beforehand (as done in @BeforeEach below), and two tests running concurrently
 * would interfere with each other through those shared fields. The problem is
 * the static state itself, not where the logic lives.
 */
class RecordTradeTest {

    @BeforeEach
    void resetStaticState() {
        TradeReportGenerator.tot.clear();
        TradeReportGenerator.f.clear();
        TradeReportGenerator.c = 0;
    }

    @Test
    void firstTradeForTickerInitialisesTotals() {
        TradeReportGenerator.recordTrade("AAPL", 1000.0, 1.0);

        assertEquals(1000.0, TradeReportGenerator.tot.get("AAPL"));
        assertEquals(1.0, TradeReportGenerator.f.get("AAPL"));
        assertEquals(1, TradeReportGenerator.c);
    }

    @Test
    void secondTradeForSameTickerAccumulatesOntoExistingTotals() {
        TradeReportGenerator.recordTrade("AAPL", 1000.0, 1.0);
        TradeReportGenerator.recordTrade("AAPL", 500.0, 0.5);

        assertEquals(1500.0, TradeReportGenerator.tot.get("AAPL"), 1e-9);
        assertEquals(1.5, TradeReportGenerator.f.get("AAPL"), 1e-9);
        assertEquals(2, TradeReportGenerator.c);
    }

    @Test
    void tradesForDifferentTickersAreTrackedSeparately() {
        TradeReportGenerator.recordTrade("AAPL", 1000.0, 1.0);
        TradeReportGenerator.recordTrade("VOD.L", 2000.0, 2.0);

        assertEquals(1000.0, TradeReportGenerator.tot.get("AAPL"), 1e-9);
        assertEquals(2000.0, TradeReportGenerator.tot.get("VOD.L"), 1e-9);
        assertEquals(2, TradeReportGenerator.c);
    }
}
