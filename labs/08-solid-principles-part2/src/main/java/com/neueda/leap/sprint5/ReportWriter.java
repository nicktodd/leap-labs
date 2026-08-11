package com.neueda.leap.sprint5;

// The abstraction DIP is built around. High-level code (OrderExecutor) will
// depend on THIS, not on any specific way of actually writing a line out.
public interface ReportWriter {
    void write(String line);
}
