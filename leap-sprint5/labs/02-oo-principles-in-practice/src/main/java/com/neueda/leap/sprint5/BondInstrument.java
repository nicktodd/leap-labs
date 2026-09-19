package com.neueda.leap.sprint5;

// Kata B.1: implement a Bond's fee structure - a flat $5.00 fee, regardless of
// trade size (bonds are typically fee-flat, unlike equities).
public class BondInstrument extends Instrument {

    public BondInstrument(String ticker) {
        super(ticker);
    }

    @Override
    public double calculateFee(double tradeValue) {
        throw new UnsupportedOperationException("TODO: implement calculateFee");
    }
}
