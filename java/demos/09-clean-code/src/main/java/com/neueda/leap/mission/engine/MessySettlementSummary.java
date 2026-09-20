package com.neueda.leap.mission.engine;

import java.util.List;

// CLEAN CODE VIOLATIONS, deliberately, for the demo:
// - single-letter/meaningless variable names (o, x, s, n1, n2)
// - a magic number (10000) with no explanation of what it means
// - one long method doing several unrelated jobs at once
// - deep nesting instead of early returns
// - a comment explaining WHAT the code does (the code already says that) instead
//   of WHY, which is the only kind of comment worth writing
public class MessySettlementSummary {

    public String s(List<Order> o) {
        int n1 = 0;
        int n2 = 0;
        double x = 0;
        // loop through the orders and add up fees and counts
        for (int i = 0; i < o.size(); i++) {
            Order od = o.get(i);
            double f = od.calculateFee();
            x = x + f;
            if (od.getTradeValue() > 10000) {
                n1 = n1 + 1;
            } else {
                if (od.getTradeValue() <= 10000) {
                    n2 = n2 + 1;
                }
            }
        }
        String r = "";
        r = r + "Total fees: $" + x + "\n";
        r = r + "Large orders: " + n1 + "\n";
        r = r + "Small orders: " + n2;
        return r;
    }
}
