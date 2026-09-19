package com.neueda.leap.sprint5;

// Step 1 of the story: inheriting from a CONCRETE class (not abstract yet).
// These three classes are deliberately non-public and live in one file together -
// they only exist to set up the problem Instrument.java (the abstract version)
// then fixes. Nothing here is part of the lab.

// A concrete class - it CAN be instantiated directly (new ConcreteInstrument(...)
// is legal), and calculateFee() has a real, default implementation.
class ConcreteInstrument {

    private final String ticker;

    ConcreteInstrument(String ticker) {
        this.ticker = ticker;
    }

    String getTicker() {
        return ticker;
    }

    // A "default" fee: 0.1% of trade value. Reasonable for an equity, but this is
    // only a guess at what most subclasses will want - nothing forces a subclass
    // to actually override it.
    double calculateFee(double tradeValue) {
        return tradeValue * 0.001;
    }
}

// A STRAIGHTFORWARD example of inheritance working exactly as intended - shown
// first, before anything goes wrong. PremiumInstrumentV1 deliberately overrides
// calculateFee() with its own logic (a higher, 1% "premium" rate), while
// inheriting getTicker() completely unchanged - it never redefines getTicker(),
// it doesn't need to, extends ConcreteInstrument means it already has it.
class PremiumInstrumentV1 extends ConcreteInstrument {

    PremiumInstrumentV1(String ticker) {
        super(ticker); // calls ConcreteInstrument's constructor to set up the
                         // inherited ticker field
    }

    @Override
    double calculateFee(double tradeValue) {
        return tradeValue * 0.01; // 1% - genuinely different from the 0.1% default
    }
}

// This override happens to be correct for an equity's fee.
class EquityInstrumentV1 extends ConcreteInstrument {
    EquityInstrumentV1(String ticker) {
        super(ticker);
    }
    // (No override needed - the inherited default already matches what an
    // equity's fee should be. This alone should feel a little too convenient.)
}

// THE BUG: bonds should charge a flat $5.00 fee, not a percentage. Whoever wrote
// this class forgot to override calculateFee() - and the compiler said nothing,
// because ConcreteInstrument's calculateFee() is a real, callable method, not a
// requirement. This class silently, incorrectly inherits the equity-style
// percentage fee instead.
class BondInstrumentBuggy extends ConcreteInstrument {
    BondInstrumentBuggy(String ticker) {
        super(ticker);
    }
}
