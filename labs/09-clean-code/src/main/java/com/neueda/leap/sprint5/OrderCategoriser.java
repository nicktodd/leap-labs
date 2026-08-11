package com.neueda.leap.sprint5;

import java.util.List;

public class OrderCategoriser {

    private static final double LARGE_ORDER_THRESHOLD = 10000;

    public String categorise(List<Order> orders) {
        int equityCount = 0;
        int bondCount = 0;
        int fundCount = 0;
        double totalFees = 0;

        for (Order order : orders) {
            totalFees += order.calculateFee();
            if (order.getInstrument() instanceof EquityInstrument) {
                equityCount++;
            } else if (order.getInstrument() instanceof BondInstrument) {
                bondCount++;
            } else if (order.getInstrument() instanceof FundInstrument) {
                fundCount++;
            }
        }

        String dominantCategory = dominantCategory(equityCount, bondCount, fundCount);
        double averageFee = orders.isEmpty() ? 0 : totalFees / orders.size();

        return dominantCategory + " portfolio: " + equityCount + " equity, " + bondCount
                + " bond, " + fundCount + " fund orders. Average fee: $" + averageFee;
    }

    private String dominantCategory(int equityCount, int bondCount, int fundCount) {
        if (equityCount > bondCount && equityCount > fundCount) {
            return "Equity-heavy";
        } else if (bondCount > equityCount && bondCount > fundCount) {
            return "Bond-heavy";
        } else if (fundCount > equityCount && fundCount > bondCount) {
            return "Fund-heavy";
        } else {
            return "Mixed";
        }
    }
}
