package com.neueda.leap.mission.engine;

import java.util.List;

// SRP FIX, part 1 of 2. One job: add up fees. Nothing about formatting, nothing
// about delivery. If the calculation rule changes, this is the only class that
// needs to change.
public class FeeAggregator {

    public double totalFees(List<Order> orders) {
        double total = 0;
        for (Order order : orders) {
            total += order.calculateFee();
        }
        return total;
    }
}
