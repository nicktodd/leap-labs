package com.fidelity.leap.sprint6;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

// Given - wires both mappers into endpoints so you can verify your work
// with curl.
@RestController
public class PortfolioController {

    private final AdvisorMapper advisorMapper;
    private final TransactionMapper transactionMapper;

    public PortfolioController(AdvisorMapper advisorMapper, TransactionMapper transactionMapper) {
        this.advisorMapper = advisorMapper;
        this.transactionMapper = transactionMapper;
    }

    @GetMapping("/advisors/{advisorId}")
    public ResponseEntity<Advisor> getAdvisor(@PathVariable int advisorId) {
        Advisor advisor = advisorMapper.findById(advisorId);
        if (advisor == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(advisor);
    }

    @GetMapping("/accounts/{accountId}/transactions")
    public List<Transaction> getTransactions(@PathVariable int accountId) {
        return transactionMapper.findByAccountId(accountId);
    }
}
