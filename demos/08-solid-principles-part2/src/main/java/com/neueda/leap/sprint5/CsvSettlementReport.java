package com.neueda.leap.sprint5;

import java.util.List;

// Implements exactly what it needs, nothing else. No stubbed, exception-throwing
// methods anywhere - there's nothing to stub, because CsvReportable never asked
// for a toConsole() or toPdf() in the first place.
public class CsvSettlementReport implements CsvReportable {

    @Override
    public String toCsv(List<Order> orders) {
        StringBuilder csv = new StringBuilder("clientId,fee\n");
        for (Order order : orders) {
            csv.append(order.getClientId()).append(",").append(order.calculateFee()).append("\n");
        }
        return csv.toString();
    }
}
