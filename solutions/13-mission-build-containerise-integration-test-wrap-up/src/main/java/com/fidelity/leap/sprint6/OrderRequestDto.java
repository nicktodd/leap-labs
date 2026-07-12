package com.fidelity.leap.sprint6;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

// Module 6's DTO pattern - the API contract, decoupled from
// domain.OrderRequest. Nothing in domain/ knows this class exists.
public record OrderRequestDto(
        @NotBlank(message = "ticker is required")
        String ticker,

        @NotNull(message = "instrumentType is required")
        String instrumentType,

        @Positive(message = "quantity must be positive")
        double quantity,

        @Positive(message = "price must be positive")
        double price,

        @NotNull(message = "side is required")
        String side
) {
    public boolean isBuy() {
        return "BUY".equalsIgnoreCase(side);
    }
}
