package com.neueda.leap.sprint6;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

public record OrderRequestDto(

        @NotBlank(message = "ticker is required")
        String ticker,

        @NotNull(message = "instrumentType is required")
        InstrumentType instrumentType,

        @Positive(message = "quantity must be positive")
        double quantity,

        @Positive(message = "price must be positive")
        double price,

        @NotNull(message = "side is required")
        Side side
) {
}
