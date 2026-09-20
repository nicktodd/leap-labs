package com.neueda.leap.mission.engine;

import java.util.List;

public class SettlementSummary {

    // Named, so the threshold's meaning is visible at every use, and there's
    // exactly one place to change it. Compare to MessySettlementSummary's bare
    // "10000".
    private static final double LARGE_ORDER_THRESHOLD = 10000;

    public String summarize(List<Order> orders) {
        double totalFees = totalFees(orders);
        int largeOrderCount = countByCategory(orders, true);
        int smallOrderCount = countByCategory(orders, false);

        return format(totalFees, largeOrderCount, smallOrderCount);
    }

    // One job: add up fees. Nothing about categorisation lives here.
    private double totalFees(List<Order> orders) {
        double total = 0;
        for (Order order : orders) {
            total += order.calculateFee();
        }
        return total;
    }

    // One job: count orders in one category. Called twice with opposite flags,
    // rather than one method silently tracking two unrelated counters at once.
    private int countByCategory(List<Order> orders, boolean large) {
        int count = 0;
        for (Order order : orders) {
            if (isLargeOrder(order) == large) {
                count++;
            }
        }
        return count;
    }

    private boolean isLargeOrder(Order order) {
        return order.getTradeValue() > LARGE_ORDER_THRESHOLD;
    }

    // One job: turn the numbers into the report string. No calculation happens
    // here - by the time this method runs, every number it needs already exists.
    private String format(double totalFees, int largeOrderCount, int smallOrderCount) {
        return "Total fees: $" + totalFees + "\n"
                + "Large orders: " + largeOrderCount + "\n"
                + "Small orders: " + smallOrderCount;
    }
}
