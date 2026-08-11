package com.neueda.leap.sprint5;

public class BondInstrument extends Instrument {

    public BondInstrument(String ticker) {
        super(ticker);
    }

    @Override
    public double calculateFee(double tradeValue) {
        return 5.00;
    }
}
