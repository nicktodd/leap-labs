package com.fidelity.leap.sprint7.legacy;

public class OtherFeeRule implements FeeRule {

    static final double RATE = 0.0005; // covers BOND and any other trade type

    @Override
    public double feeFor(double tradeValue) {
        return tradeValue * RATE;
    }
}
