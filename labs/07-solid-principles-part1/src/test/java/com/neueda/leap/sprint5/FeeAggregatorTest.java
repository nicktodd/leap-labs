package com.neueda.leap.sprint5;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

class FeeAggregatorTest {

    @Test
    void sumsFeesAcrossOrders() {
        List<Order> orders = List.of(
                new Order("C001", new EquityInstrument("AAPL"), 10000),
                new Order("C002", new BondInstrument("VOD.L"), 8000),
                new Order("C003", new FundInstrument("VWRL"), 5000)
        );

        double total = new FeeAggregator().totalFees(orders);

        assertEquals(17.0, total, 0.0001);
    }

    @Test
    void returnsZeroForNoOrders() {
        double total = new FeeAggregator().totalFees(List.of());

        assertEquals(0.0, total, 0.0001);
    }
}
