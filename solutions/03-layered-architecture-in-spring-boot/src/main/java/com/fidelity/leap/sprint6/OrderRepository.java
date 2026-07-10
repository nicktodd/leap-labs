package com.fidelity.leap.sprint6;

// Given, don't modify. The repository layer's contract: given a ticker, what
// fee rate applies? Nothing about HOW that's looked up is exposed here -
// Module 7 swaps InMemoryOrderRepository for a real MyBatis-backed one
// against this exact interface.
public interface OrderRepository {
    double findFeeRate(String ticker);
}
