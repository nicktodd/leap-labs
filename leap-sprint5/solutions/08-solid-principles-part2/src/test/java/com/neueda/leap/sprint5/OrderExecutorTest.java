package com.neueda.leap.sprint5;

import org.junit.jupiter.api.Test;

import java.lang.reflect.Constructor;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class OrderExecutorTest {

    @Test
    void constructorDependsOnTheReportWriterAbstraction() {
        Constructor<?>[] constructors = OrderExecutor.class.getConstructors();

        boolean dependsOnAbstraction = false;
        for (Constructor<?> constructor : constructors) {
            Class<?>[] paramTypes = constructor.getParameterTypes();
            if (paramTypes.length == 1 && paramTypes[0] == ReportWriter.class) {
                dependsOnAbstraction = true;
            }
        }

        assertTrue(dependsOnAbstraction,
                "OrderExecutor's constructor must take a ReportWriter (the interface), "
                        + "not a specific concrete writer class");
    }

    @Test
    void executeReturnsTheCalculatedFee() {
        InMemoryReportWriter writer = new InMemoryReportWriter();
        OrderExecutor executor = new OrderExecutor(writer);
        Order order = new Order("C001", new EquityInstrument("AAPL"), 10000);

        double fee = executor.execute(order);

        assertEquals(10.0, fee, 0.0001);
    }

    @Test
    void executeWritesThroughTheProvidedWriter() {
        InMemoryReportWriter writer = new InMemoryReportWriter();
        OrderExecutor executor = new OrderExecutor(writer);
        Order order = new Order("C002", new BondInstrument("VOD.L"), 8000);

        executor.execute(order);

        assertTrue(writer.getLines().stream().anyMatch(line -> line.contains("C002") && line.contains("5.0")));
    }
}
