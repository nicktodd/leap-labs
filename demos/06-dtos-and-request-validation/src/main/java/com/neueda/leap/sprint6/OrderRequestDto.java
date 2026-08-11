package com.neueda.leap.sprint6;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

// The DTO (Data Transfer Object) - the shape of what crosses the HTTP
// boundary, straight from Module 5's OpenAPI OrderRequest schema. This is
// deliberately NOT the same class as any internal domain object - there is
// no "Order" class here at all, only what a client is required to send.
//
// A record, because a DTO has no behaviour - it's pure data, and Bean
// Validation annotations work the same way on record components as on
// regular fields.
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
