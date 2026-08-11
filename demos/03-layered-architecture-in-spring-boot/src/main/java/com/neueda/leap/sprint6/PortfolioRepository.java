package com.neueda.leap.sprint6;

// The repository layer's job: know how to fetch data, and nothing else. No
// business logic lives here - just "given a clientId, what's the total value?"
// This is an interface deliberately, exactly like Sprint 5's ReportWriter -
// Module 7 swaps InMemoryPortfolioRepository for a real MyBatis-backed one,
// and nothing above this interface needs to change.
public interface PortfolioRepository {
    double findTotalValue(String clientId);
}
