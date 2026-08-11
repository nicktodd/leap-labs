package com.neueda.leap.sprint7.legacy;

// Extracted from TradeReportGenerator.doIt() (Module 11's first refactoring
// step). Behaviour is UNCHANGED - this is Extract Method plus Introduce
// Named Constant, nothing more. The old code used 0.0005 for both BOND and
// "anything else" as a coincidence (Module 10 flagged this as a duplicated
// literal); this version makes that a DELIBERATE, named, shared decision -
// OTHER_FEE_RATE - so a future reader knows it was chosen, not copy-pasted.
public class FeeCalculator {

    static final double EQUITY_FEE_RATE = 0.001;
    static final double OTHER_FEE_RATE = 0.0005; // covers BOND and any other trade type

    public static double calculateFee(String tradeType, double tradeValue) {
        double rate = tradeType.equals("EQUITY") ? EQUITY_FEE_RATE : OTHER_FEE_RATE;
        return tradeValue * rate;
    }
}
