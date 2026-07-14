package com.fidelity.leap.sprint7.legacy;

public class EquityFeeRule implements FeeRule {

    static final double RATE = 0.001;

    @Override
    public double feeFor(double tradeValue) {
        return tradeValue * RATE;
    }
}
