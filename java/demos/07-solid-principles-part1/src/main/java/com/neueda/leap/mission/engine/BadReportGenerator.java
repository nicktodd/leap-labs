package com.neueda.leap.mission.engine;

import java.util.List;

// SRP VIOLATION - this is Module 6's flawed-design.mmd, in code. One class does
// THREE unrelated things: sums the fees (a calculation), formats them as a report
// (a presentation concern), and "sends" the report (an I/O concern). Three
// different reasons for this class to change: the fee calculation rule changes,
// the report format changes, or the delivery mechanism changes - and any one of
// those changes risks breaking the other two, because they all live in one place.
public class BadReportGenerator {

    public void generateAndSend(List<Order> orders) {
        // Responsibility 1: calculation
        double total = 0;
        for (Order order : orders) {
            total += order.calculateFee();
        }

        // Responsibility 2: formatting/presentation
        StringBuilder report = new StringBuilder("Settlement Report\n");
        for (Order order : orders) {
            report.append(order.getClientId())
                    .append(": $")
                    .append(order.calculateFee())
                    .append("\n");
        }
        report.append("Total fees: $").append(total);

        // Responsibility 3: delivery/I-O
        System.out.println("--- Emailing report ---");
        System.out.println(report);
    }
}
