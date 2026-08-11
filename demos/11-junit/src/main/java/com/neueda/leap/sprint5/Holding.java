package com.neueda.leap.sprint5;

// Encapsulation as a DESIGN DECISION, not just "make fields private out of habit."
// The field is private specifically because this class has an invariant to protect:
// quantity can never go negative. If quantity were a public field, EVERY piece of
// code anywhere in the codebase that touches a Holding would be individually
// responsible for remembering that rule - and it only takes one careless line,
// anywhere, to break it. Making the field private and only exposing a validated
// method to change it means the rule is enforced in exactly one place, permanently.
public class Holding {

    private double quantity;

    public Holding(double initialQuantity) {
        if (initialQuantity < 0) {
            throw new IllegalArgumentException("initial quantity cannot be negative");
        }
        this.quantity = initialQuantity;
    }

    public double getQuantity() {
        return quantity;
    }

    // The ONLY way to change quantity - and it enforces the invariant every time,
    // not just when the caller remembers to check.
    public void adjust(double delta) {
        double newQuantity = quantity + delta;
        if (newQuantity < 0) {
            throw new IllegalArgumentException(
                    "adjustment would make quantity negative: " + quantity + " + " + delta);
        }
        quantity = newQuantity;
    }
}

// Compare to what this would look like WITHOUT encapsulation (do not do this):
//
// public class BadHolding {
//     public double quantity;   // any code, anywhere, can set this to anything
// }
//
// BadHolding h = new BadHolding();
// h.quantity = -500;             // compiles fine, and now the whole system has
//                                 // to somehow cope with a holding that makes no
//                                 // real-world sense.
