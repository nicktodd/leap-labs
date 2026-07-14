package com.fidelity.leap.sprint7.legacy;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

// A CHARACTERISATION test: it records what doIt() actually DOES today, bugs
// and all - not what it SHOULD do. Its job is to be the safety net for the
// refactor that follows, not to judge the behaviour. In particular, this
// test deliberately locks in the "2 bad rows are silently skipped" bug,
// because fixing THAT is Module 8's job (on a different codebase) - not
// something this refactor is allowed to change.
class TradeReportGeneratorCharacterisationTest {

    private static final Path REPORT_FILE = Path.of("report.csv");

    @AfterEach
    void cleanUpGeneratedReport() throws Exception {
        Files.deleteIfExists(REPORT_FILE);
    }

    @Test
    void capturesTheExactCurrentBehaviourOfDoIt() throws Exception {
        // doIt() accumulates into static state that other test classes
        // (e.g. RecordTradeTest) also touch - reset it explicitly rather
        // than relying on this test running first in a fresh JVM.
        TradeReportGenerator.tot.clear();
        TradeReportGenerator.f.clear();
        TradeReportGenerator.c = 0;

        ByteArrayOutputStream capturedOut = new ByteArrayOutputStream();
        PrintStream originalOut = System.out;
        System.setOut(new PrintStream(capturedOut));

        try {
            TradeReportGenerator.doIt("src/main/resources/trades.csv");
        } finally {
            System.setOut(originalOut);
        }

        String output = capturedOut.toString();

        // 12 rows in the CSV, 2 are malformed (a blank quantity, a
        // non-numeric price) - doIt() silently skips both. This is the
        // exact bug Module 1 asked you to notice. The test locks it in
        // AS-IS; it is not this refactor's job to fix it.
        assertTrue(output.contains("Processed 10 trades"),
                "expected exactly 10 of the 12 rows to be processed");

        assertTrue(output.contains("AAPL total=33810.0 fee=33.81"));
        assertTrue(output.contains("VOD.L total=44700.0 fee=44.7"));
        assertTrue(output.contains("GILT10 total=203000.0 fee=101.5"));
        assertTrue(output.contains("CORPB1 total=148250.0 fee=74.125"));
        assertTrue(output.contains("GLBEQ1 total=18975.0 fee=9.4875"));
        assertTrue(output.contains("ULVR.L total=15280.000000000002 fee=15.280000000000003"));

        assertTrue(Files.exists(REPORT_FILE), "report.csv should have been written");
        String reportContent = Files.readString(REPORT_FILE);
        assertEquals("""
                TICKER,QTY,VALUE,FEE
                AAPL,100.0,15025.0,15.025
                VOD.L,500.0,44700.0,44.7
                GILT10,2000.0,203000.0,101.5
                AAPL,50.0,7550.0,7.55
                CORPB1,1000.0,98750.0,49.375
                GLBEQ1,300.0,12630.0,6.315
                AAPL,75.0,11235.0,11.235
                GLBEQ1,150.0,6345.0,3.1725
                ULVR.L,400.0,15280.000000000002,15.280000000000003
                CORPB1,500.0,49500.0,24.75
                """, reportContent);
    }
}
