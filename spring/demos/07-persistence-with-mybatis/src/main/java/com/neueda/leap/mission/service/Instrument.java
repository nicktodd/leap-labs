package com.neueda.leap.mission.service;

// A plain result-mapping class - MyBatis populates this by matching column
// names (or an explicit mapping) to these fields. No JPA annotations, no
// entity lifecycle, no persistence context - just a query result, mapped.
public class Instrument {
    private String ticker;
    private String name;
    private String assetClass;
    private String currency;

    public String getTicker() {
        return ticker;
    }

    public void setTicker(String ticker) {
        this.ticker = ticker;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getAssetClass() {
        return assetClass;
    }

    public void setAssetClass(String assetClass) {
        this.assetClass = assetClass;
    }

    public String getCurrency() {
        return currency;
    }

    public void setCurrency(String currency) {
        this.currency = currency;
    }
}
