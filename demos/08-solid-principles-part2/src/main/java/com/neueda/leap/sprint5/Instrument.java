package com.neueda.leap.sprint5;

// Step 2 of the story: the fix for ConcreteInheritanceProblem.java. Instrument is
// now ABSTRACT, and implements the Feeable interface (see Feeable.java).
//
// "abstract" means: this class can never be instantiated directly (new
// Instrument("AAPL") is a compile error) - it exists only to be extended. And
// because calculateFee() has NO body here, every subclass is REQUIRED to supply
// its own, or that subclass must also be declared abstract. A class that forgets
// to override it, like BondInstrumentBuggy did, simply won't compile any more -
// the exact bug from Step 1 is now impossible, enforced by the compiler, not by
// someone remembering.
public abstract class Instrument implements Feeable {

    private final String ticker;

    protected Instrument(String ticker) {
        this.ticker = ticker;
    }

    public String getTicker() {
        return ticker;
    }

    // No body - subclasses MUST provide one. Compare to ConcreteInstrument's
    // version, which had a real (and dangerously reusable) default.
    @Override
    public abstract double calculateFee(double tradeValue);
}
