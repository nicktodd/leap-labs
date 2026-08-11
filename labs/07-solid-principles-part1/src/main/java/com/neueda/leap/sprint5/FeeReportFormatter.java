package com.neueda.leap.sprint5;

import java.util.List;

public class FeeReportFormatter {

    public String format(List<Order> orders, double total) {
        StringBuilder sb = new StringBuilder();
        sb.append("Settlement Report\n");
        for (Order order : orders) {
            sb.append(order.getClientId()).append(": $").append(order.calculateFee()).append("\n");
        }
        sb.append("Total fees: $").append(total);
        return sb.toString();
    }
}
