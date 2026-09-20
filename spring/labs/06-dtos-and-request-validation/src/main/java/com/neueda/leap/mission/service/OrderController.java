package com.neueda.leap.mission.service;

import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

// Kata B: implement submitOrder and getOrder below. An in-memory `orders` map
// is given so getOrder has something to look up - Module 7 replaces this with
// real persistence.
@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderService service;
    private final Map<String, OrderResponseDto> orders = new ConcurrentHashMap<>();
    private final AtomicInteger idSequence = new AtomicInteger(1);

    public OrderController(OrderService service) {
        this.service = service;
    }

    // TODO: POST /orders (this method's mapping annotation is missing).
    // Take a @Valid @RequestBody OrderRequestDto. Calculate the fee via
    // service.calculateFee(ticker, quantity * price). Generate a new id from
    // idSequence, build an OrderResponseDto with status "ACCEPTED", put it in
    // the `orders` map keyed by id, and return 201 Created with a Location
    // header of "/orders/{id}".
    public ResponseEntity<OrderResponseDto> submitOrder(@Valid @RequestBody OrderRequestDto request) {
        throw new UnsupportedOperationException("TODO: implement submitOrder");
    }

    // TODO: GET /orders/{id} (this method's mapping annotation is missing).
    // Look up the id in the `orders` map. Return 200 with the found
    // OrderResponseDto, or 404 if there's no order with that id.
    public ResponseEntity<OrderResponseDto> getOrder(@PathVariable String id) {
        throw new UnsupportedOperationException("TODO: implement getOrder");
    }
}
