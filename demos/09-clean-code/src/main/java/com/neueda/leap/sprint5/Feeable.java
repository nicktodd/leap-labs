package com.neueda.leap.sprint5;

// Step 3 of the story: an INTERFACE.
//
// An interface is a pure contract: a method signature with no body and no state
// at all (not even a private field) - just a promise that "any class implementing
// this has a calculateFee method." Unlike Instrument (an abstract class), a
// Feeable doesn't need to BE an Instrument at all - it just needs to be able to
// calculate a fee. That's the problem abstract classes alone can't solve: some
// things that need to calculate a fee (see AccountMaintenanceCharge.java) have
// nothing else in common with an Instrument, and forcing them into the Instrument
// hierarchy just to reuse this one capability would be exactly the kind of bad,
// reuse-only inheritance Part 6 of this demo warns about.
//
// A class can extend only ONE other class, but can implement as many interfaces
// as it needs - Instrument extends nothing, but implements Feeable.
public interface Feeable {
    double calculateFee(double tradeValue);
}
