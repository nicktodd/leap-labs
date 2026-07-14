package com.fidelity.leap.sprint7.legacy;

// EXTRACT INTERFACE (a further step beyond FeeCalculator - see
// FeeRuleCalculator.java for the full explanation). This interface names a
// single capability - "given a trade's value, what's the fee?" - so that
// EQUITY and everything-else can each provide their own answer, instead of
// one method deciding between them with an if/else.
public interface FeeRule {
    double feeFor(double tradeValue);
}
