package com.neueda.leap.sprint5;

import java.util.List;

public class SolidDemo {

    public static void main(String[] args) {
        List<Order> orders = List.of(
                new Order("C001", new EquityInstrument("AAPL"), 10000),
                new Order("C002", new BondInstrument("VOD.L"), 8000),
                new Order("C003", new FundInstrument("VWRL"), 5000)
        );

        System.out.println("=== S: Single Responsibility Principle ===");
        System.out.println("-- Before: one class does calculation, formatting, AND delivery --");
        new BadReportGenerator().generateAndSend(orders);

        System.out.println();
        System.out.println("-- After: three separate, single-purpose classes --");
        FeeAggregator aggregator = new FeeAggregator();
        double total = aggregator.totalFees(orders);
        FeeReportFormatter formatter = new FeeReportFormatter();
        String report = formatter.format(orders, total);
        System.out.println(report);

        System.out.println();
        System.out.println("=== O: Open/Closed Principle ===");
        Order derivativeOrder = new Order("C004", new DerivativeInstrument("FTSE-FUT"), 20000);
        System.out.println("New instrument type, zero changes to Instrument, Feeable, Order,");
        System.out.println("FeeAggregator, or FeeReportFormatter:");
        System.out.println("DerivativeInstrument fee on $20000: $" + derivativeOrder.calculateFee());

        System.out.println();
        System.out.println("=== L: Liskov Substitution Principle ===");
        Holding realHolding = new Holding(100);
        System.out.println("-- Before: FrozenHoldingBad extends Holding, but breaks its contract --");
        Holding disguisedFrozenHolding = new FrozenHoldingBad(100);
        try {
            adjustAll(List.of(realHolding, disguisedFrozenHolding), 10);
            System.out.println("adjustAll succeeded for every Holding in the list");
        } catch (UnsupportedOperationException e) {
            System.out.println("adjustAll CRASHED on a value that's still typed as Holding: " + e.getMessage());
        }

        System.out.println();
        System.out.println("-- After: FrozenHolding doesn't extend Holding, so it can't be");
        System.out.println("   smuggled into code that expects a genuine, adjustable Holding --");
        FrozenHolding properlyFrozen = new FrozenHolding(new Holding(100));
        adjustAll(List.of(realHolding), 10);
        System.out.println("adjustAll succeeded — only real Holdings were ever in the list");
        System.out.println("Frozen quantity, read-only: " + properlyFrozen.getQuantity());
    }

    // Generic code written against Holding. This is exactly the kind of code that
    // silently breaks when a subtype doesn't honour its supertype's contract.
    private static void adjustAll(List<Holding> holdings, double delta) {
        for (Holding holding : holdings) {
            holding.adjust(delta);
        }
    }
}
