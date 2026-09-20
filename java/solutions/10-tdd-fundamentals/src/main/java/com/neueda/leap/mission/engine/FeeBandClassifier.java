package com.neueda.leap.mission.engine;

public class FeeBandClassifier {

    private static final double PREMIUM_THRESHOLD = 5000;
    private static final double INSTITUTIONAL_THRESHOLD = 50000;

    public String classify(double tradeValue) {
        if (tradeValue >= INSTITUTIONAL_THRESHOLD) {
            return "INSTITUTIONAL";
        }
        if (tradeValue >= PREMIUM_THRESHOLD) {
            return "PREMIUM";
        }
        return "STANDARD";
    }
}
