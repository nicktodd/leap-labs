package com.fidelity.leap.sprint6;

// Also a DTO, matching Module 5's OpenAPI OrderResponse schema exactly. Note
// what's NOT here: no reference to Instrument, no internal fee-calculation
// detail beyond the final number. A client only ever sees this shape -
// changing an internal domain class never has to mean changing this contract,
// and vice versa.
public record OrderResponseDto(String id, String status, Double fee, String reason) {
}
