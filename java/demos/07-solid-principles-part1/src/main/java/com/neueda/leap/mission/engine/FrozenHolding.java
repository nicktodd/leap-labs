package com.neueda.leap.mission.engine;

// LSP FIX. FrozenHolding does NOT extend Holding - it HOLDS one (composition,
// exactly like Module 4's Portfolio/Holding relationship). It exposes only
// getQuantity(), and deliberately has no adjust() method at all: there is no
// promise to break, because it never claimed to be a Holding in the first place.
// Any code that specifically wants to work with frozen holdings has to say so
// explicitly (by using the FrozenHolding type), rather than discovering the
// restriction at runtime via a thrown exception.
public class FrozenHolding {

    private final Holding holding;

    public FrozenHolding(Holding holding) {
        this.holding = holding;
    }

    public double getQuantity() {
        return holding.getQuantity();
    }
}
