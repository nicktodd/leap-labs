package com.neueda.leap.mission.service;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

// No Spring context, no real repository - just a mock. Notice this test can
// run in milliseconds, and would keep passing unchanged even if
// InMemoryOrderRepository were replaced with a real Postgres-backed one in
// Module 7.
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private OrderRepository repository;

    @Test
    void calculatesFeeAsTradeValueTimesTheRate() {
        when(repository.findFeeRate("AAPL")).thenReturn(0.001);

        OrderService service = new OrderService(repository);

        double fee = service.calculateFee("AAPL", 10000);

        assertEquals(10.0, fee, 0.0001);
        verify(repository).findFeeRate("AAPL");
    }

    @Test
    void aZeroRateProducesAZeroFee() {
        when(repository.findFeeRate("VWRL")).thenReturn(0.0);

        OrderService service = new OrderService(repository);

        double fee = service.calculateFee("VWRL", 5000);

        assertEquals(0.0, fee, 0.0001);
    }
}
