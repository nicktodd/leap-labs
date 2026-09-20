package com.neueda.leap.mission.engine;

import java.util.List;

public class OODemo {

    public static void main(String[] args) {

        // --- Part 0: class vs. object ---
        // Trade (from Module 1) is a CLASS: a blueprint. It has no data of its own
        // until something builds an OBJECT from it with "new". Every "new Trade(...)"
        // call creates a separate, independent object - changing one never affects
        // another, even though both were built from the exact same class.
        Trade tradeOne = new Trade("T0001", "Alice Chen", "AAPL", 120, 185.32, "BUY");
        Trade tradeTwo = new Trade("T0002", "Ben Whitfield", "MSFT", 60, 402.11, "BUY");
        System.out.println("Two objects, one class: " + tradeOne + " | " + tradeTwo);
        System.out.println("Same class? " + (tradeOne.getClass() == tradeTwo.getClass()));
        System.out.println("Same object? " + (tradeOne == tradeTwo));

        // --- Part 1: encapsulation as a design decision ---
        // The simplest of today's ideas: one object, protecting its own data.
        // No inheritance, no interfaces, nothing else involved yet.
        Holding holding = new Holding(100);
        holding.adjust(-30);
        System.out.println("\nHolding quantity after sell: " + holding.getQuantity());
        try {
            holding.adjust(-1000);
        } catch (IllegalArgumentException e) {
            System.out.println("Rejected: " + e.getMessage());
        }

        // --- Part 2: a straightforward inheritance example ---
        // Before anything goes wrong: PremiumInstrumentV1 extends ConcreteInstrument,
        // deliberately overriding calculateFee() with its own logic, while getTicker()
        // is inherited completely unchanged - it's never redefined, extends already
        // gives PremiumInstrumentV1 that method for free.
        PremiumInstrumentV1 premium = new PremiumInstrumentV1("VOD.L");
        double tradeValue = 10000.0;
        System.out.println("\n" + premium.getTicker() + " (inherited method) premium fee "
                + "(overridden method): " + premium.calculateFee(tradeValue));

        // --- Part 3: the same mechanism, but a subclass that DOESN'T override ---
        ConcreteInstrument equityV1 = new EquityInstrumentV1("AAPL");
        ConcreteInstrument bondBuggy = new BondInstrumentBuggy("GILT10");
        System.out.println("\nEquityInstrumentV1 fee (correct by coincidence): "
                + equityV1.calculateFee(tradeValue));
        System.out.println("BondInstrumentBuggy fee (SHOULD be a flat $5.00): "
                + bondBuggy.calculateFee(tradeValue) + "  <- silently wrong");
        // Nothing here failed to compile. The bug is real, and invisible until
        // someone notices the number is wrong in production.

        // --- Part 4: the fix - an ABSTRACT class ---
        // Instrument.java is now abstract, with calculateFee() having no body at
        // all. Try (mentally, don't uncomment) writing:
        //     class BrokenInstrument extends Instrument { }
        // - it will not compile. "class BrokenInstrument must implement the
        // inherited abstract method Instrument.calculateFee". The Step 3 bug is
        // now a compiler error, not a silent mistake.
        Instrument equity = new EquityInstrument("AAPL");
        Instrument bond = new BondInstrument("GILT10");
        System.out.println("\nEquityInstrument fee: " + equity.calculateFee(tradeValue));
        System.out.println("BondInstrument fee: " + bond.calculateFee(tradeValue));

        // --- Part 5: interfaces - a capability, not a hierarchy ---
        // AccountMaintenanceCharge has nothing to do with Instrument - no ticker,
        // not a tradable thing at all - but it still implements Feeable, because
        // it can still calculate a fee.
        Feeable maintenanceCharge = new AccountMaintenanceCharge("ACC-001");
        System.out.println("\nAccountMaintenanceCharge fee: "
                + maintenanceCharge.calculateFee(0.0));

        // --- Part 6: polymorphism across the interface, not just the class hierarchy ---
        // A List<Feeable> can hold BOTH Instruments (which implement Feeable
        // indirectly, via the abstract class) AND AccountMaintenanceCharge (which
        // implements it directly) - genuinely unrelated classes, united only by
        // the one capability they share.
        List<Feeable> feeableThings = List.of(equity, bond, maintenanceCharge);
        double totalFees = 0.0;
        for (Feeable feeable : feeableThings) {
            totalFees += feeable.calculateFee(tradeValue);
        }
        System.out.println("Total fees across unrelated Feeable things: " + totalFees);

        // --- Part 7: recognising bad inheritance ---
        BadClientRegistry registry = new BadClientRegistry();
        registry.add("C001");
        registry.add("C001"); // ArrayList allows the duplicate - the registry
                                // never got the chance to define its own rule.
        System.out.println("\nRegistry (should never have allowed a duplicate): " + registry);
    }
}
