package com.neueda.leap.mission.engine;

import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.*;

// Every test you've written this sprint used @Test and assertEquals/assertTrue.
// That's a small fraction of what JUnit offers. This demo walks through the rest,
// applied to classes you already know: Holding, Instrument, and its subclasses.
@DisplayName("JUnit 5 features, applied to familiar classes")
class JUnitFeaturesDemoTest {

    // --- @BeforeEach: shared setup, re-run fresh before EVERY test ---
    // A new Holding is created before each test method runs, so no test can
    // accidentally see state left over from another one.
    private Holding holding;

    @BeforeEach
    void setUp() {
        holding = new Holding(100);
    }

    @Test
    @DisplayName("a fresh holding starts with the quantity it was constructed with")
    void freshHoldingHasInitialQuantity() {
        assertEquals(100.0, holding.getQuantity(), 0.0001);
    }

    @Test
    @DisplayName("adjusting is reflected immediately")
    void adjustChangesQuantity() {
        holding.adjust(50);
        assertEquals(150.0, holding.getQuantity(), 0.0001);
    }

    // --- assertThrows: the FORMAL way to test for an expected exception ---
    // Compare to a manual try/catch (which some earlier labs used) - assertThrows
    // is shorter, and fails with a clear message if NO exception is thrown at all,
    // which a try/catch can silently miss if written carelessly.
    @Test
    @DisplayName("adjusting below zero throws, and does not change state")
    void adjustBelowZeroThrows() {
        IllegalArgumentException exception = assertThrows(
                IllegalArgumentException.class,
                () -> holding.adjust(-1000)
        );
        assertTrue(exception.getMessage().contains("negative"));
        // and the state is provably unchanged - this is a SECOND assertion,
        // grouped with assertAll below in a moment.
    }

    // --- assertAll: group related assertions so ALL of them run and report,
    // even if an earlier one fails. A chain of separate assertEquals calls
    // stops at the first failure - assertAll doesn't. ---
    @Test
    @DisplayName("a bond's ticker and fee are both correct, reported together")
    void bondReportsTickerAndFeeTogether() {
        BondInstrument bond = new BondInstrument("VOD.L");

        assertAll("bond properties",
                () -> assertEquals("VOD.L", bond.getTicker()),
                () -> assertEquals(5.0, bond.calculateFee(1000), 0.0001),
                () -> assertEquals(5.0, bond.calculateFee(1_000_000), 0.0001)
        );
        // If the ticker assertion failed AND the fee assertion failed, assertAll
        // reports BOTH failures in one run - a chain of assertEquals would only
        // ever show you the first one, hiding the second until you fix the first.
    }

    // --- @ParameterizedTest + @ValueSource: run the SAME test body against
    // several different inputs, instead of copy-pasting near-identical tests. ---
    @ParameterizedTest
    @ValueSource(doubles = {1000, 5000, 1_000_000, 0.01})
    @DisplayName("a bond's fee is always exactly $5, regardless of trade value")
    void bondFeeIsAlwaysFive(double tradeValue) {
        assertEquals(5.0, new BondInstrument("VOD.L").calculateFee(tradeValue), 0.0001);
    }

    // --- @ParameterizedTest + @CsvSource: when the test needs an input AND its
    // expected output, paired together. ---
    @ParameterizedTest
    @CsvSource({
            "1000, 1.0",
            "10000, 10.0",
            "100000, 100.0"
    })
    @DisplayName("an equity's fee is 0.1% of trade value")
    void equityFeeIsOnePercentOfTradeValue(double tradeValue, double expectedFee) {
        assertEquals(expectedFee, new EquityInstrument("AAPL").calculateFee(tradeValue), 0.0001);
    }

    // --- @Nested: group related tests into their own inner class, so the test
    // report itself documents the structure of the behaviour being tested. ---
    @Nested
    @DisplayName("when the holding is at exactly zero")
    class WhenHoldingIsAtZero {

        private Holding zeroHolding;

        @BeforeEach
        void setUp() {
            // Each @Nested class gets its OWN @BeforeEach - this runs in
            // addition to the outer class's setUp() above, not instead of it.
            zeroHolding = new Holding(0);
        }

        @Test
        @DisplayName("a positive adjustment succeeds")
        void positiveAdjustmentSucceeds() {
            zeroHolding.adjust(10);
            assertEquals(10.0, zeroHolding.getQuantity(), 0.0001);
        }

        @Test
        @DisplayName("any negative adjustment throws")
        void anyNegativeAdjustmentThrows() {
            assertThrows(IllegalArgumentException.class, () -> zeroHolding.adjust(-0.01));
        }
    }

    // --- @Disabled: skip a test deliberately, with a reason on record - very
    // different from just deleting or commenting it out, which loses the intent. ---
    @Test
    @Disabled("Derivative instruments aren't introduced until Module 7's OCP kata")
    void placeholderForFutureInstrumentType() {
        fail("not yet implemented");
    }
}
