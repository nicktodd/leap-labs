package com.neueda.leap.sprint5;

import java.util.List;

public class FeeReportFormatter {

    public String format(List<Order> orders, double total) {
        StringBuilder report = new StringBuilder("Settlement Report\n");
        for (Order order : orders) {
            report.append(order.getClientId())
                    .append(": $")
                    .append(order.calculateFee())
                    .append("\n");
        }
        report.append("Total fees: $").append(total);
        return report.toString();
    }
}
