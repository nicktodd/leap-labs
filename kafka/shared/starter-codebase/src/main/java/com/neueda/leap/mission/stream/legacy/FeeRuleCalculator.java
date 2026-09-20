package com.neueda.leap.mission.stream.legacy;

import java.util.Map;

// A BONUS, OPTIONAL further refactor - not required by Module 11's lab, and
// NOT wired into doIt() (FeeCalculator remains what TradeReportGenerator
// actually calls). This class exists purely to demonstrate two more named
// refactoring techniques on the exact same fee logic, so they can be
// compared side by side with what Module 11's main exercise already did:
//
//   EXTRACT INTERFACE - FeeRule names the capability ("give me a fee for
//   this value") that EQUITY and "everything else" each implement their
//   own way, instead of one method choosing between them.
//
//   REPLACE CONDITIONAL WITH POLYMORPHISM - FeeCalculator.calculateFee()
//   used an if/else (then a ternary) to choose behaviour based on a type
//   String. Here, the Map<String, FeeRule> lookup replaces that decision
//   entirely - there is no if/else asking "which type is this?" anywhere
//   in this class. Adding a new trade type with its own fee rule means
//   adding a new FeeRule implementation and one new map entry - NOT
//   editing an existing method's conditional logic.
//
// Whether this is a WORTHWHILE refactor for THIS codebase is a genuine
// question, deliberately left open for discussion - see the demo guide.
public class FeeRuleCalculator {

    private static final Map<String, FeeRule> RULES = Map.of(
            "EQUITY", new EquityFeeRule()
    );
    private static final FeeRule DEFAULT_RULE = new OtherFeeRule();

    public static double calculateFee(String tradeType, double tradeValue) {
        FeeRule rule = RULES.getOrDefault(tradeType, DEFAULT_RULE);
        return rule.feeFor(tradeValue);
    }
}
