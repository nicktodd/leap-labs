package com.neueda.leap.sprint5;

import java.util.List;

public class FeeAggregator {

    public double totalFees(List<Order> orders) {
        double total = 0;
        for (Order order : orders) {
            total += order.calculateFee();
        }
        return total;
    }
}
