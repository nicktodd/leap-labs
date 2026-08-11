package com.neueda.leap.sprint5;

public class DerivativeInstrument extends Instrument {

    public DerivativeInstrument(String ticker) {
        super(ticker);
    }

    @Override
    public double calculateFee(double tradeValue) {
        return tradeValue * 0.02;
    }
}
