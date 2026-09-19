package com.neueda.leap.sprint5;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CsvSettlementReportTest {

    @Test
    void producesAHeaderLine() {
        String csv = new CsvSettlementReport().toCsv(List.of());

        assertTrue(csv.startsWith("clientId,fee"));
    }

    @Test
    void producesOneLinePerOrder() {
        List<Order> orders = List.of(
                new Order("C001", new EquityInstrument("AAPL"), 10000),
                new Order("C002", new BondInstrument("VOD.L"), 8000)
        );

        String csv = new CsvSettlementReport().toCsv(orders);

        assertTrue(csv.contains("C001,10.0"));
        assertTrue(csv.contains("C002,5.0"));
    }

    @Test
    void doesNotImplementConsoleReportable() {
        assertFalse(ConsoleReportable.class.isAssignableFrom(CsvSettlementReport.class),
                "CsvSettlementReport should only implement CsvReportable - it doesn't need console output");
    }
}
