package com.neueda.leap.sprint6;

import org.springframework.stereotype.Service;

// Kata: the service layer. Constructor-inject an OrderRepository (no
// @Autowired needed - a single constructor is enough), and implement
// calculateFee(ticker, tradeValue) as tradeValue * repository.findFeeRate(ticker).
// See OrderServiceTest.java for the exact behaviour expected.
@Service
public class OrderService {

    // TODO: add a private final OrderRepository field, and a constructor
    // that accepts one and assigns it.

    public double calculateFee(String ticker, double tradeValue) {
        throw new UnsupportedOperationException("TODO: implement calculateFee");
    }
}
