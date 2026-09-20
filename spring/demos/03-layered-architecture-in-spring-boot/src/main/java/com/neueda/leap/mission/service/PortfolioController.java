package com.neueda.leap.mission.service;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

// The controller layer's job: translate HTTP into a method call, and a method
// return value back into HTTP. No business logic lives here - it delegates to
// PortfolioService immediately. Controller -> Service -> Repository, each
// layer doing exactly one kind of work, each depending only on the layer
// directly below it.
@RestController
public class PortfolioController {

    private final PortfolioService service;

    public PortfolioController(PortfolioService service) {
        this.service = service;
    }

    @GetMapping("/portfolios/{clientId}")
    public String getPortfolio(@PathVariable String clientId) {
        return service.describeValue(clientId);
    }
}
