package com.neueda.leap.mission.engine;

public class Client {

    private final String clientId;
    private final double riskLimit;
    private final Portfolio portfolio = new Portfolio();

    public Client(String clientId, double riskLimit) {
        this.clientId = clientId;
        this.riskLimit = riskLimit;
    }

    public String getClientId() {
        return clientId;
    }

    public double getRiskLimit() {
        return riskLimit;
    }

    public Portfolio getPortfolio() {
        return portfolio;
    }
}
