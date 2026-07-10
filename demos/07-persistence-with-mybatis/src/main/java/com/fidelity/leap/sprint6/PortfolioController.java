package com.fidelity.leap.sprint6;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class PortfolioController {

    private final InstrumentMapper instrumentMapper;
    private final HoldingMapper holdingMapper;

    public PortfolioController(InstrumentMapper instrumentMapper, HoldingMapper holdingMapper) {
        this.instrumentMapper = instrumentMapper;
        this.holdingMapper = holdingMapper;
    }

    @GetMapping("/instruments/{ticker}")
    public ResponseEntity<Instrument> getInstrument(@PathVariable String ticker) {
        Instrument instrument = instrumentMapper.findByTicker(ticker);
        if (instrument == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(instrument);
    }

    @GetMapping("/clients/{clientId}/holdings")
    public List<Holding> getHoldings(@PathVariable int clientId) {
        return holdingMapper.findByClientId(clientId);
    }
}
