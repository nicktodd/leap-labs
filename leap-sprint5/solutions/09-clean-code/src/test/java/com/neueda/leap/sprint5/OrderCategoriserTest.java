package com.neueda.leap.sprint5;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

// These tests already pass against the given, messy OrderCategoriser - they exist
// to prove your refactor doesn't change behaviour, not to define new behaviour.
class OrderCategoriserTest {

    @Test
    void identifiesAnEquityHeavyPortfolio() {
        List<Order> orders = List.of(
                new Order("C001", new EquityInstrument("AAPL"), 10000),
                new Order("C002", new EquityInstrument("MSFT"), 10000),
                new Order("C003", new EquityInstrument("GOOG"), 10000),
                new Order("C004", new BondInstrument("VOD.L"), 8000)
        );

        String result = new OrderCategoriser().categorise(orders);

        assertEquals("Equity-heavy portfolio: 3 equity, 1 bond, 0 fund orders. Average fee: $8.75", result);
    }

    @Test
    void reportsMixedWhenNoCategoryDominates() {
        List<Order> orders = List.of(
                new Order("C001", new EquityInstrument("AAPL"), 10000),
                new Order("C002", new BondInstrument("VOD.L"), 8000),
                new Order("C003", new FundInstrument("VWRL"), 5000)
        );

        String result = new OrderCategoriser().categorise(orders);

        assertEquals("Mixed portfolio: 1 equity, 1 bond, 1 fund orders. Average fee: $5.666666666666667", result);
    }

    @Test
    void handlesAnEmptyPortfolioWithoutDividingByZero() {
        String result = new OrderCategoriser().categorise(List.of());

        assertEquals("Mixed portfolio: 0 equity, 0 bond, 0 fund orders. Average fee: $0.0", result);
    }
}
