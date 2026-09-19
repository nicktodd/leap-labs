package com.neueda.leap.sprint5;

// The corrected version of BondInstrumentBuggy (see ConcreteInheritanceProblem.java) -
// now extending the ABSTRACT Instrument, which forces this override to exist.
// Leave this method out entirely and the project simply won't compile.
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
