package com.neueda.leap.sprint5;

// Kata C (LSP): FrozenHoldingBad.java (given, don't modify) extends Holding and
// breaks its contract by making adjust() always throw. Fix this WITHOUT
// inheriting from Holding at all - use composition instead (hold a Holding as a
// field). Expose only getQuantity(); there should be no adjust() method here,
// because a frozen holding genuinely can't be adjusted, and pretending otherwise
// (by exposing a method that always throws) is exactly the mistake
// FrozenHoldingBad makes.
public class FrozenHolding {

    public FrozenHolding(Holding holding) {
        throw new UnsupportedOperationException("TODO: implement constructor");
    }

    public double getQuantity() {
        throw new UnsupportedOperationException("TODO: implement getQuantity");
    }
}
