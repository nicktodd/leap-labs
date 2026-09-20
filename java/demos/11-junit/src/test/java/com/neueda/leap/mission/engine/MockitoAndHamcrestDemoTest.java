package com.neueda.leap.mission.engine;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.anyDouble;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;

// WHY ISOLATION MATTERS, AND WHY THAT MEANS MOCKS
//
// OrderExecutor's actual job is small: ask its Instrument for a fee, ask its
// ReportWriter to write a line, return the fee. None of that job involves
// KNOWING HOW a fee is calculated, or HOW a line gets written - it just
// coordinates two collaborators.
//
// Every test of OrderExecutor so far (Module 8's demo) used a REAL
// BondInstrument and a REAL InMemoryReportWriter. That means those tests were
// never truly testing OrderExecutor alone - they were testing OrderExecutor
// AND BondInstrument's fee formula AND InMemoryReportWriter's storage, all at
// once. If BondInstrument's fee calculation had a bug, EVERY test that used a
// real BondInstrument would fail too - including tests whose actual job is to
// check OrderExecutor's coordination logic, which might be completely correct.
// You'd see a red test and have no idea, without investigating, which of the
// two classes actually broke.
//
// A MOCK replaces a real collaborator with a fake stand-in whose behaviour YOU
// control completely, and that records every call made to it so you can check
// afterward. Testing OrderExecutor against a MOCK Instrument and a MOCK
// ReportWriter means: if this test goes red, it is unambiguously OrderExecutor's
// fault. Nothing else is even real enough to have a bug.
@ExtendWith(MockitoExtension.class)
@DisplayName("OrderExecutor, tested in true isolation with Mockito")
class MockitoAndHamcrestDemoTest {

    @Mock
    private Instrument mockInstrument;

    @Mock
    private ReportWriter mockWriter;

    @Nested
    @DisplayName("stubbing: controlling what a mock returns")
    class Stubbing {

        @Test
        @DisplayName("when(...).thenReturn(...) makes the mock respond however the test needs")
        void executorUsesWhateverFeeTheInstrumentReturns() {
            // Stub: "WHEN calculateFee is called with 1000.0, THEN return 42.0" -
            // regardless of what a real Instrument subclass would actually compute.
            // This is the entire point: the test controls the collaborator's
            // behaviour directly, instead of depending on real business logic
            // living somewhere else.
            when(mockInstrument.calculateFee(1000.0)).thenReturn(42.0);

            Order order = new Order("C001", mockInstrument, 1000.0);
            OrderExecutor executor = new OrderExecutor(mockWriter);

            double fee = executor.execute(order);

            assertEquals(42.0, fee);
        }

        @Test
        @DisplayName("anyDouble() stubs a return value for ANY argument, when the exact value doesn't matter")
        void stubbingWithAnArgumentMatcher() {
            when(mockInstrument.calculateFee(anyDouble())).thenReturn(10.0);

            Order order = new Order("C002", mockInstrument, 12345.0);
            double fee = new OrderExecutor(mockWriter).execute(order);

            assertEquals(10.0, fee);
        }
    }

    @Nested
    @DisplayName("verify(): checking a mock was actually used correctly")
    class Verifying {

        @Test
        @DisplayName("verify() confirms a specific call happened, with specific arguments")
        void verifiesTheWriterReceivedTheExpectedLine() {
            when(mockInstrument.calculateFee(1000.0)).thenReturn(42.0);
            Order order = new Order("C001", mockInstrument, 1000.0);

            new OrderExecutor(mockWriter).execute(order);

            // Not just "did execute() return the right number" - this proves
            // OrderExecutor actually TALKED to its ReportWriter collaborator,
            // with exactly the line it should have produced.
            verify(mockWriter).write("C001: $42.0");
        }

        @Test
        @DisplayName("times() confirms HOW MANY times a call happened")
        void verifiesTheInstrumentWasAskedExactlyOnce() {
            when(mockInstrument.calculateFee(anyDouble())).thenReturn(10.0);
            Order order = new Order("C002", mockInstrument, 500.0);

            new OrderExecutor(mockWriter).execute(order);

            verify(mockInstrument, times(1)).calculateFee(500.0);
            verify(mockWriter, times(1)).write(anyString());
        }

        @Test
        @DisplayName("verifyNoInteractions() confirms a mock was never touched at all")
        void aMockNeverCalledHasNoInteractions() {
            // Nothing in this test ever calls mockWriter - proving that, e.g., a
            // validation failure path genuinely never reaches the report writer,
            // rather than trusting that by reading the code.
            verifyNoInteractions(mockWriter);
        }
    }

    @Nested
    @DisplayName("ArgumentCaptor: inspecting exactly what was passed to a mock")
    class Capturing {

        @Test
        @DisplayName("captures the real argument for a closer assertion than an exact-match verify()")
        void capturesTheLineWrittenForDetailedInspection() {
            when(mockInstrument.calculateFee(anyDouble())).thenReturn(7.5);
            Order order = new Order("C004", mockInstrument, 300.0);

            new OrderExecutor(mockWriter).execute(order);

            ArgumentCaptor<String> captor = ArgumentCaptor.forClass(String.class);
            verify(mockWriter).write(captor.capture());

            assertThat(captor.getValue(), allOf(containsString("C004"), containsString("7.5")));
        }
    }

    @Nested
    @DisplayName("mocks vs. Module 8's hand-rolled InMemoryReportWriter")
    class MocksVersusHandRolledFakes {

        @Test
        @DisplayName("a hand-rolled fake still uses REAL collaborator logic elsewhere")
        void theHandRolledFakeOnlyReplacesTheWriterNotTheInstrument() {
            // InMemoryReportWriter (Module 8) is a genuine, useful test double -
            // but notice this test still exercises a REAL BondInstrument. A bug
            // in BondInstrument.calculateFee() would make THIS test fail too,
            // even though it's meant to test OrderExecutor.
            InMemoryReportWriter fakeWriter = new InMemoryReportWriter();
            Instrument realBond = new BondInstrument("VOD.L");
            Order order = new Order("C003", realBond, 8000);

            new OrderExecutor(fakeWriter).execute(order);

            assertEquals(List.of("C003: $5.0"), fakeWriter.getLines());
        }

        @Test
        @DisplayName("a mock isolates OrderExecutor from BOTH collaborators, not just one")
        void theMockIsolatesFromBothCollaborators() {
            when(mockInstrument.calculateFee(anyDouble())).thenReturn(999.0);
            Order order = new Order("C003", mockInstrument, 8000);

            double fee = new OrderExecutor(mockWriter).execute(order);

            // 999.0 is not a real fee any BondInstrument would ever produce -
            // and that's exactly the point. This test could not possibly be
            // affected by a bug in BondInstrument, because BondInstrument was
            // never involved at all.
            assertEquals(999.0, fee);
        }
    }

    @Nested
    @DisplayName("Hamcrest matchers: readable, composable assertions")
    class HamcrestMatchers {

        @Test
        @DisplayName("assertThat(value, matcher) reads closer to a sentence than assertEquals")
        void basicHamcrestMatchers() {
            when(mockInstrument.calculateFee(anyDouble())).thenReturn(42.0);
            double fee = new OrderExecutor(mockWriter).execute(new Order("C005", mockInstrument, 100));

            // assertEquals(42.0, fee) and assertThat(fee, is(42.0)) check the
            // same thing - Hamcrest's phrasing reads more like the requirement
            // it's checking, and its matchers COMPOSE (see below).
            assertThat(fee, is(42.0));
            assertThat(fee, greaterThan(0.0));
        }

        @Test
        @DisplayName("string and collection matchers express intent precisely")
        void stringAndCollectionMatchers() {
            assertThat("Settlement Report\nC001: $42.0", containsString("C001"));
            assertThat("Settlement Report\nC001: $42.0", startsWith("Settlement"));

            List<String> lines = List.of("first", "second", "third");
            assertThat(lines, hasSize(3));
            assertThat(lines, hasItem("second"));
        }

        @Test
        @DisplayName("allOf/anyOf compose several matchers into one readable assertion")
        void composedMatchers() {
            double fee = 42.0;

            // A plain JUnit equivalent would need two separate assertTrue calls,
            // or a manual (fee > 0 && fee < 100) boolean expression with no
            // useful failure message. This single line checks both AND reports
            // exactly which part failed if it doesn't hold.
            assertThat(fee, allOf(greaterThan(0.0), lessThan(100.0)));
        }
    }
}
