package com.neueda.leap.mission.service;

// Result-mapping class for AccountMapper.findInstrument - Module 7's pattern,
// applied here rather than repeated.
public class InstrumentRow {
    private int instrumentId;
    private String ticker;
    private String assetClass;

    public int getInstrumentId() {
        return instrumentId;
    }

    public void setInstrumentId(int instrumentId) {
        this.instrumentId = instrumentId;
    }

    public String getTicker() {
        return ticker;
    }

    public void setTicker(String ticker) {
        this.ticker = ticker;
    }

    public String getAssetClass() {
        return assetClass;
    }

    public void setAssetClass(String assetClass) {
        this.assetClass = assetClass;
    }
}
