package com.neueda.leap.mission.service;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

// The JPA equivalent of Module 7's plain Instrument class - same four
// columns, but this one IS the persistence model, not just a query
// result shape. @Entity puts it under Hibernate's management: once
// loaded, this object is tracked, and changes to it get written back
// on flush - MyBatis's Instrument had none of that.
@Entity
@Table(name = "instruments")
public class Instrument {

    @Id
    private Integer instrumentId;

    private String ticker;
    private String name;
    private String assetClass;
    private String currency;

    protected Instrument() {
        // JPA requires a no-args constructor to build entities via reflection
    }

    public Integer getInstrumentId() {
        return instrumentId;
    }

    public String getTicker() {
        return ticker;
    }

    public String getName() {
        return name;
    }

    public String getAssetClass() {
        return assetClass;
    }

    public String getCurrency() {
        return currency;
    }
}
