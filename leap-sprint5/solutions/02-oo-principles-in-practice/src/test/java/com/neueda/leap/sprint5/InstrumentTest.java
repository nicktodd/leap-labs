package com.neueda.leap.sprint5;

import org.junit.jupiter.api.Test;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

class InstrumentTest {

    @Test
    void bondChargesAFlatFiveDollarFeeRegardlessOfTradeSize() {
        Instrument bond = new BondInstrument("GILT10");
        assertEquals(5.00, bond.calculateFee(100.0), 0.001);
        assertEquals(5.00, bond.calculateFee(1_000_000.0), 0.001);
    }

    @Test
    void cryptoChargesHalfAPercent() {
        Instrument crypto = new CryptoInstrument("BTC");
        assertEquals(50.00, crypto.calculateFee(10_000.0), 0.001);
    }

    @Test
    void cryptoAppliesAOneDollarMinimumFeeOnSmallTrades() {
        Instrument crypto = new CryptoInstrument("BTC");
        // 0.5% of 50.00 = 0.25, below the $1.00 minimum
        assertEquals(1.00, crypto.calculateFee(50.0), 0.001);
    }

    @Test
    void polymorphicListCallsTheCorrectSubclassImplementation() {
        List<Instrument> instruments = List.of(
                new BondInstrument("GILT10"),
                new CryptoInstrument("BTC")
        );
        double total = 0.0;
        for (Instrument instrument : instruments) {
            total += instrument.calculateFee(10_000.0);
        }
        assertEquals(5.00 + 50.00, total, 0.001);
    }
}
