package com.neueda.leap.mission.service;

import java.math.BigDecimal;

// Result-mapping class for the XML-based mapper - a client's holding,
// joined across holdings -> accounts -> instruments.
public class Holding {
    private int clientId;
    private String clientName;
    private String ticker;
    private BigDecimal quantity;

    public int getClientId() {
        return clientId;
    }

    public void setClientId(int clientId) {
        this.clientId = clientId;
    }

    public String getClientName() {
        return clientName;
    }

    public void setClientName(String clientName) {
        this.clientName = clientName;
    }

    public String getTicker() {
        return ticker;
    }

    public void setTicker(String ticker) {
        this.ticker = ticker;
    }

    public BigDecimal getQuantity() {
        return quantity;
    }

    public void setQuantity(BigDecimal quantity) {
        this.quantity = quantity;
    }
}
