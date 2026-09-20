package com.neueda.leap.mission.engine;

// The abstraction DIP is built around. High-level code (OrderExecutor) will
// depend on THIS, not on any specific way of actually writing a line out.
public interface ReportWriter {
    void write(String line);
}
