package com.neueda.leap.mission.service;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

// Kata: the controller layer. Constructor-inject an OrderService, and add a
// @GetMapping("/orders/{ticker}/fee") method that takes the ticker as a
// @PathVariable and the trade value as a @RequestParam double tradeValue,
// then returns service.calculateFee(ticker, tradeValue).
//
// Try: curl "http://localhost:8080/orders/AAPL/fee?tradeValue=10000"
@RestController
public class OrderController {

    // TODO: add a private final OrderService field, and a constructor that
    // accepts one and assigns it.

    // TODO: add the @GetMapping method described above.
}
