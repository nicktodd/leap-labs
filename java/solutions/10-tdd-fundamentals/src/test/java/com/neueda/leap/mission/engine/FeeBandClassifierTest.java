package com.neueda.leap.mission.engine;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class FeeBandClassifierTest {

    @Test
    void classifiesASmallTradeAsStandard() {
        assertEquals("STANDARD", new FeeBandClassifier().classify(1000));
    }

    @Test
    void classifiesALargeTradeAsInstitutional() {
        assertEquals("INSTITUTIONAL", new FeeBandClassifier().classify(60000));
    }

    @Test
    void classifiesAMidSizedTradeAsPremium() {
        assertEquals("PREMIUM", new FeeBandClassifier().classify(10000));
    }

    @Test
    void treatsThePremiumLowerBoundaryAsInclusive() {
        assertEquals("PREMIUM", new FeeBandClassifier().classify(5000));
    }

    @Test
    void treatsTheInstitutionalLowerBoundaryAsInclusive() {
        assertEquals("INSTITUTIONAL", new FeeBandClassifier().classify(50000));
    }
}
