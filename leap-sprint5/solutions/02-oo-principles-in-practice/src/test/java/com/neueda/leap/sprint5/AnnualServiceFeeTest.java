package com.neueda.leap.sprint5;

import org.junit.jupiter.api.Test;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class AnnualServiceFeeTest {

    @Test
    void doesNotExtendInstrument() {
        // This must be a capability shared via interface, not a forced hierarchy.
        assertFalse(Instrument.class.isAssignableFrom(AnnualServiceFee.class),
                "AnnualServiceFee must not extend or relate to Instrument at all");
    }

    @Test
    void implementsFeeableDirectly() {
        assertTrue(Feeable.class.isAssignableFrom(AnnualServiceFee.class));
    }

    @Test
    void alwaysChargesAFlatThirtyDollarFeeRegardlessOfTradeValue() {
        Feeable fee = new AnnualServiceFee();
        assertEquals(30.00, fee.calculateFee(0.0), 0.001);
        assertEquals(30.00, fee.calculateFee(1_000_000.0), 0.001);
    }

    @Test
    void polymorphicListMixesInstrumentsAndNonInstrumentFeeables() {
        List<Feeable> feeableThings = List.of(
                new BondInstrument("GILT10"),   // an Instrument
                new AnnualServiceFee()            // NOT an Instrument
        );
        double total = 0.0;
        for (Feeable feeable : feeableThings) {
            total += feeable.calculateFee(10_000.0);
        }
        assertEquals(5.00 + 30.00, total, 0.001);
    }
}
