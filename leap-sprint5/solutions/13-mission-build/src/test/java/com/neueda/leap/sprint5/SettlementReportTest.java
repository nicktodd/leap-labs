package com.neueda.leap.sprint5;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class SettlementReportTest {

    @Test
    void rendersAnAcceptedOrder() {
        SettlementReport report = new SettlementReport();

        report.recordAccepted("C001", "AAPL", 15.0);

        assertEquals("Settlement Report\n"
                + "C001 AAPL: ACCEPTED, fee $15.0\n"
                + "Total fees: $15.0", report.render());
    }

    @Test
    void rendersARejectedOrder() {
        SettlementReport report = new SettlementReport();

        report.recordRejected("C002", "VWRL", "would exceed the client's risk limit");

        assertEquals("Settlement Report\n"
                + "C002 VWRL: REJECTED - would exceed the client's risk limit\n"
                + "Total fees: $0.0", report.render());
    }

    @Test
    void sumsFeesAcrossMultipleAcceptedOrdersAndSkipsRejectedOnes() {
        SettlementReport report = new SettlementReport();

        report.recordAccepted("C001", "AAPL", 15.0);
        report.recordRejected("C002", "VWRL", "would exceed the client's risk limit");
        report.recordAccepted("C001", "VOD.L", 5.0);

        String rendered = report.render();

        assertEquals("Settlement Report\n"
                + "C001 AAPL: ACCEPTED, fee $15.0\n"
                + "C002 VWRL: REJECTED - would exceed the client's risk limit\n"
                + "C001 VOD.L: ACCEPTED, fee $5.0\n"
                + "Total fees: $20.0", rendered);
    }
}
