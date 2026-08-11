package com.neueda.leap.sprint5;

// LSP VIOLATION. A frozen holding (e.g. under regulatory hold) can't be adjusted -
// that's a genuine business rule. But expressing it by EXTENDING Holding and
// overriding adjust() to always throw breaks the promise Holding makes to every
// piece of code that already depends on it: "you can call adjust() on any
// Holding, and it will either succeed or throw only if the specific delta would
// go negative." A FrozenHoldingBad breaks that promise unconditionally - any
// generic code written against Holding (see SolidDemo's adjustAll helper) that
// works fine for a real Holding will crash the moment it's handed one of these.
// That's Liskov Substitution, violated: a subtype should be usable anywhere its
// supertype is expected, without surprising the caller.
public class FrozenHoldingBad extends Holding {

    public FrozenHoldingBad(double quantity) {
        super(quantity);
    }

    @Override
    public void adjust(double delta) {
        throw new UnsupportedOperationException("holding is frozen");
    }
}
