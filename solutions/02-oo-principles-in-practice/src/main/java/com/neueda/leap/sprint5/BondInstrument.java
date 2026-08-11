package com.neueda.leap.sprint5;

// Kata B.1: a flat $5.00 fee, regardless of trade size (bonds are typically
// fee-flat, unlike equities).
public class BondInstrument extends Instrument {

    private static final double FLAT_FEE = 5.00;

    public BondInstrument(String ticker) {
        super(ticker);
    }

    @Override
    public double calculateFee(double tradeValue) {
        return FLAT_FEE;
    }
}
