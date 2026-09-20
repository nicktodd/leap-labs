package com.neueda.leap.mission.engine;

import java.util.List;

public class CleanCodeDemo {

    public static void main(String[] args) {
        List<Order> orders = List.of(
                new Order("C001", new EquityInstrument("AAPL"), 15000),
                new Order("C002", new BondInstrument("VOD.L"), 8000),
                new Order("C003", new FundInstrument("VWRL"), 5000),
                new Order("C004", new EquityInstrument("MSFT"), 20000)
        );

        System.out.println("=== Messy version ===");
        System.out.println(new MessySettlementSummary().s(orders));

        System.out.println();
        System.out.println("=== Clean version - identical output ===");
        System.out.println(new SettlementSummary().summarize(orders));
    }
}
