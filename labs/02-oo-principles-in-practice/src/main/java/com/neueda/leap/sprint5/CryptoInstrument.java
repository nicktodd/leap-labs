package com.neueda.leap.sprint5;

// Kata B.2: implement Crypto's fee structure - 0.5% of trade value, with a $1.00
// minimum fee (crypto exchanges typically charge a higher rate than equities, with
// a floor so tiny trades aren't effectively fee-free).
public class CryptoInstrument extends Instrument {

    private static final double FEE_RATE = 0.005;
    private static final double MINIMUM_FEE = 1.00;

    public CryptoInstrument(String ticker) {
        super(ticker);
    }

    @Override
    public double calculateFee(double tradeValue) {
        throw new UnsupportedOperationException("TODO: implement calculateFee");
    }
}
