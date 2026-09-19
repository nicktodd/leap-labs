package com.neueda.leap.sprint5;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class FeeReportFormatterTest {

    @Test
    void formatsOneOrderPerLineWithTotal() {
        List<Order> orders = List.of(
                new Order("C001", new EquityInstrument("AAPL"), 10000),
                new Order("C002", new BondInstrument("VOD.L"), 8000)
        );

        String report = new FeeReportFormatter().format(orders, 15.0);

        String expected = "Settlement Report\n"
                + "C001: $10.0\n"
                + "C002: $5.0\n"
                + "Total fees: $15.0";
        assertEquals(expected, report);
    }

    @Test
    void includesEveryClientId() {
        List<Order> orders = List.of(
                new Order("C001", new EquityInstrument("AAPL"), 10000),
                new Order("C002", new BondInstrument("VOD.L"), 8000),
                new Order("C003", new FundInstrument("VWRL"), 5000)
        );

        String report = new FeeReportFormatter().format(orders, 17.0);

        assertTrue(report.contains("C001"));
        assertTrue(report.contains("C002"));
        assertTrue(report.contains("C003"));
    }
}
