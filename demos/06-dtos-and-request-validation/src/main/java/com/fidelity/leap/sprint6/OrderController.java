package com.fidelity.leap.sprint6;

import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.util.concurrent.atomic.AtomicInteger;

@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderService service;
    private final AtomicInteger idSequence = new AtomicInteger(1);

    public OrderController(OrderService service) {
        this.service = service;
    }

    // @Valid triggers Bean Validation against every annotated field on
    // OrderRequestDto BEFORE this method body ever runs. A request that
    // fails validation never reaches this code at all - Spring intercepts
    // it and returns a 400 automatically.
    @PostMapping
    public ResponseEntity<OrderResponseDto> submitOrder(@Valid @RequestBody OrderRequestDto request) {
        double tradeValue = request.quantity() * request.price();
        double fee = service.calculateFee(request.ticker(), tradeValue);

        String id = String.valueOf(idSequence.getAndIncrement());
        OrderResponseDto response = new OrderResponseDto(id, "ACCEPTED", fee, null);

        URI location = URI.create("/orders/" + id);
        return ResponseEntity.created(location).body(response);
    }
}
