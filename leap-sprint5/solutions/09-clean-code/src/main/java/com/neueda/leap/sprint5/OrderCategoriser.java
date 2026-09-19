package com.neueda.leap.sprint5;

import java.util.List;

public class OrderCategoriser {

    public String categorise(List<Order> orders) {
        CategoryCounts counts = countByInstrumentType(orders);
        double averageFee = averageFee(orders);

        return dominantCategory(counts) + " portfolio: "
                + counts.equity + " equity, " + counts.bond + " bond, " + counts.fund + " fund orders. "
                + "Average fee: $" + averageFee;
    }

    private CategoryCounts countByInstrumentType(List<Order> orders) {
        CategoryCounts counts = new CategoryCounts();
        for (Order order : orders) {
            if (order.getInstrument() instanceof EquityInstrument) {
                counts.equity++;
            } else if (order.getInstrument() instanceof BondInstrument) {
                counts.bond++;
            } else if (order.getInstrument() instanceof FundInstrument) {
                counts.fund++;
            }
        }
        return counts;
    }

    private double averageFee(List<Order> orders) {
        if (orders.isEmpty()) {
            return 0;
        }
        double totalFees = 0;
        for (Order order : orders) {
            totalFees += order.calculateFee();
        }
        return totalFees / orders.size();
    }

    private String dominantCategory(CategoryCounts counts) {
        if (counts.equity > counts.bond && counts.equity > counts.fund) {
            return "Equity-heavy";
        }
        if (counts.bond > counts.equity && counts.bond > counts.fund) {
            return "Bond-heavy";
        }
        if (counts.fund > counts.equity && counts.fund > counts.bond) {
            return "Fund-heavy";
        }
        return "Mixed";
    }

    // A small, private, named holder rather than three parallel counters passed
    // around separately - it exists purely to make countByInstrumentType's
    // return type self-explanatory.
    private static class CategoryCounts {
        int equity;
        int bond;
        int fund;
    }
}
