package com.fidelity.leap.sprint6;

import org.springframework.stereotype.Service;

import java.time.Clock;
import java.time.Instant;

// The service layer's job: business logic, coordinating whatever it needs
// from the repository layer. This class doesn't know or care that
// PortfolioRepository is currently backed by a hardcoded Map - Module 7 swaps
// that for real Postgres access, and this class does not change.
//
// Constructor injection, no @Autowired needed: a class with exactly one
// constructor gets its parameters supplied by Spring automatically.
@Service
public class PortfolioService {

    private final PortfolioRepository repository;
    private final Clock clock;

    public PortfolioService(PortfolioRepository repository, Clock clock) {
        this.repository = repository;
        this.clock = clock;
    }

    public String describeValue(String clientId) {
        double total = repository.findTotalValue(clientId);
        Instant asOf = clock.instant();
        return "Client " + clientId + ": $" + total + " as of " + asOf;
    }
}
