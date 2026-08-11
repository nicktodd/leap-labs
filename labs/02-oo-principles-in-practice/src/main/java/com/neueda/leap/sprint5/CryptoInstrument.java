package com.neueda.leap.sprint5;

public class CryptoInstrument extends Instrument {

    private static final double FEE_RATE = 0.005;
    private static final double MINIMUM_FEE = 1.00;

    public CryptoInstrument(String ticker) {
        super(ticker);
    }

    @Override
    public double calculateFee(double tradeValue) {
        return Math.max(tradeValue * FEE_RATE, MINIMUM_FEE);
    }
}
