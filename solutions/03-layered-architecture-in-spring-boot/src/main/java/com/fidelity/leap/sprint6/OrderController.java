package com.fidelity.leap.sprint6;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class OrderController {

    private final OrderService service;

    public OrderController(OrderService service) {
        this.service = service;
    }

    @GetMapping("/orders/{ticker}/fee")
    public double fee(@PathVariable String ticker, @RequestParam double tradeValue) {
        return service.calculateFee(ticker, tradeValue);
    }
}
