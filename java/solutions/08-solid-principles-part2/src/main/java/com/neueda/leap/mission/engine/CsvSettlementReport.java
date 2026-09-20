package com.neueda.leap.mission.engine;

import java.util.List;

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
