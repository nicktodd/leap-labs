package com.neueda.leap.sprint6;

import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.util.Map;
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

    @GetMapping("/{id}")
    public ResponseEntity<OrderResponseDto> getOrder(@PathVariable String id) {
        OrderResponseDto order = orders.get(id);
        if (order == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(order);
    }
}
