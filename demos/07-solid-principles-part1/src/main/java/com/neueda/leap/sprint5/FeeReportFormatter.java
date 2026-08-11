package com.neueda.leap.sprint5;

import java.util.List;

// SRP FIX, part 2 of 2. One job: turn orders (plus a pre-calculated total) into a
// report string. It doesn't calculate anything itself, and it doesn't know or
// care how the report gets delivered - that's a third class's job, not shown here,
// deliberately, to keep the point sharp: each of these classes has exactly one
// reason to change.
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
