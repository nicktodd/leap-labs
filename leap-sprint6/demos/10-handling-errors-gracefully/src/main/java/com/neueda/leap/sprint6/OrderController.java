package com.neueda.leap.sprint6;

import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderService service;
    private final Map<String, OrderResponseDto> orders = new ConcurrentHashMap<>();
    private final AtomicInteger idSequence = new AtomicInteger(1);

    public OrderController(OrderService service) {
        this.service = service;
    }

    @PostMapping
    public ResponseEntity<OrderResponseDto> submitOrder(@Valid @RequestBody OrderRequestDto request) {
        double tradeValue = request.quantity() * request.price();
        double fee = service.calculateFee(request.ticker(), tradeValue);

        String id = String.valueOf(idSequence.getAndIncrement());
        OrderResponseDto response = new OrderResponseDto(id, "ACCEPTED", fee, null);
        orders.put(id, response);

        URI location = URI.create("/orders/" + id);
        return ResponseEntity.created(location).body(response);
    }

    // No manual null-check + notFound().build() here any more - throwing
    // lets GlobalExceptionHandler produce the SAME error shape this
    // endpoint would get from an unknown ticker three layers down in
    // OrderService. One handler, every "doesn't exist" case in the service.
    @GetMapping("/{id}")
    public ResponseEntity<OrderResponseDto> getOrder(@PathVariable String id) {
        OrderResponseDto order = orders.get(id);
        if (order == null) {
            throw new NoSuchElementException("no order with id " + id);
        }
        return ResponseEntity.ok(order);
    }
}
