package com.neueda.leap.sprint6;

// A plain record for the demo - deliberately not the real DTO pattern yet
// (that's Module 6). Today's point is HTTP semantics, not request shaping.
public record OrderRecord(String id, String ticker, double quantity, double price) {
}
