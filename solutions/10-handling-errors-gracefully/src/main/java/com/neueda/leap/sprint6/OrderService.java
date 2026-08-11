package com.neueda.leap.sprint6;

import org.springframework.stereotype.Service;

@Service
public class OrderService {

    // A single order above this value needs manual sign-off - not a
    // malformed request (Bean Validation's job), a well-formed order this
    // service still won't process on its own. This is the business rule
    // Module 6's model-answers.md pointed at without anywhere to put it.
    private static final double MAX_TRADE_VALUE = 1_000_000.0;

    private final OrderRepository repository;

    public OrderService(OrderRepository repository) {
        this.repository = repository;
    }

    public double calculateFee(String ticker, double tradeValue) {
        if (tradeValue > MAX_TRADE_VALUE) {
            throw new OrderRejectedException(
                    "trade value " + tradeValue + " exceeds the single-order limit of " + MAX_TRADE_VALUE);
        }
        double rate = repository.findFeeRate(ticker);
        return tradeValue * rate;
    }
}
