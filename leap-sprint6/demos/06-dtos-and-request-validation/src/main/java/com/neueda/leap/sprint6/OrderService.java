package com.neueda.leap.sprint6;

import org.springframework.stereotype.Service;

@Service
public class OrderService {

    private final OrderRepository repository;

    public OrderService(OrderRepository repository) {
        this.repository = repository;
    }

    public double calculateFee(String ticker, double tradeValue) {
        double rate = repository.findFeeRate(ticker);
        return tradeValue * rate;
    }
}
