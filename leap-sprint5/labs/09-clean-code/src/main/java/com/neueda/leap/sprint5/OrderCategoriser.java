package com.neueda.leap.sprint5;

import java.util.List;

// Your task: refactor this class WITHOUT changing its behaviour. The tests in
// OrderCategoriserTest already pass against this messy version - they must still
// pass, unchanged, once you're done. See labs/09-clean-code/README.md for the
// full task and clean-code-checklist.md for what to look for.
public class OrderCategoriser {

    public String categorise(List<Order> o) {
        int a = 0;
        int b = 0;
        int c = 0;
        double t = 0;
        for (int i = 0; i < o.size(); i++) {
            Order x = o.get(i);
            t = t + x.calculateFee();
            if (x.getInstrument() instanceof EquityInstrument) {
                a = a + 1;
            } else if (x.getInstrument() instanceof BondInstrument) {
                b = b + 1;
            } else if (x.getInstrument() instanceof FundInstrument) {
                c = c + 1;
            }
        }
        String d;
        if (a > b && a > c) {
            d = "Equity-heavy";
        } else if (b > a && b > c) {
            d = "Bond-heavy";
        } else if (c > a && c > b) {
            d = "Fund-heavy";
        } else {
            d = "Mixed";
        }
        double avg;
        if (o.size() == 0) {
            avg = 0;
        } else {
            avg = t / o.size();
        }
        return d + " portfolio: " + a + " equity, " + b + " bond, " + c + " fund orders. "
                + "Average fee: $" + avg;
    }
}
