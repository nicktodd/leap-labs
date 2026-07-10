package com.fidelity.leap.sprint6;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class InstrumentController {

    private final InstrumentRepository repository;

    public InstrumentController(InstrumentRepository repository) {
        this.repository = repository;
    }

    @GetMapping("/instruments/{ticker}")
    public ResponseEntity<Instrument> getInstrument(@PathVariable String ticker) {
        return repository.findByTicker(ticker)
                .map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }
}
