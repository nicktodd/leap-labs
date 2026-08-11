package com.neueda.leap.sprint6;

import org.springframework.stereotype.Repository;

import java.util.Map;
import java.util.NoSuchElementException;

@Repository
public class InMemoryOrderRepository implements OrderRepository {

    private static final Map<String, Double> RATES = Map.of(
            "AAPL", 0.001,
            "VOD.L", 0.0005,
            "VWRL", 0.0
    );

    @Override
    public double findFeeRate(String ticker) {
        Double rate = RATES.get(ticker);
        if (rate == null) {
            throw new NoSuchElementException("no such ticker: " + ticker);
        }
        return rate;
    }
}
