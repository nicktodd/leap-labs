package com.neueda.leap.mission.service;

import org.springframework.stereotype.Repository;

import java.util.Map;
import java.util.NoSuchElementException;

// @Repository marks this as a Spring-managed bean, in the persistence layer -
// functionally identical to @Component, but the name documents intent AND
// tells Spring to translate database-specific exceptions consistently once a
// real database is involved (Module 7).
//
// A hardcoded Map stands in for Postgres for now - the whole point of the
// PortfolioRepository interface is that nothing outside this class needs to
// know that.
@Repository
public class InMemoryPortfolioRepository implements PortfolioRepository {

    private static final Map<String, Double> VALUES = Map.of(
            "C001", 42000.0,
            "C002", 15500.0
    );

    @Override
    public double findTotalValue(String clientId) {
        Double value = VALUES.get(clientId);
        if (value == null) {
            throw new NoSuchElementException("no such client: " + clientId);
        }
        return value;
    }
}
