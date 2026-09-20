package com.neueda.leap.mission.service;

import org.springframework.stereotype.Repository;

import java.util.Map;
import java.util.NoSuchElementException;

// Given, don't modify. A hardcoded Map stands in for Postgres, exactly like
// Module 3's demo - the whole point of OrderRepository is that OrderService
// never needs to know that.
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
