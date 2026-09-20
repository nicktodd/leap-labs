package com.neueda.leap.mission.engine;

// Kata A: fix HoldingStarter's public-field problem here, properly.
// TODO:
// - quantity must be a PRIVATE field.
// - Constructor: accept an initial quantity; throw IllegalArgumentException if it's negative.
// - getQuantity(): return the current quantity.
// - adjust(double delta): apply delta to quantity; throw IllegalArgumentException
//   (without changing state) if the result would be negative.
public class Holding {

    // TODO: declare the field here (private!)

    public Holding(double initialQuantity) {
        throw new UnsupportedOperationException("TODO: implement constructor");
    }

    public double getQuantity() {
        throw new UnsupportedOperationException("TODO: implement getQuantity");
    }

    public void adjust(double delta) {
        throw new UnsupportedOperationException("TODO: implement adjust");
    }
}
