package com.neueda.leap.paysprint;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
public class AccountController {

    @Autowired
    private AccountRepository accountRepository;

    @Autowired
    private CurrentUserProvider currentUserProvider;

    @GetMapping("/api/accounts/{accountId}")
    public Account getAccount(@PathVariable Long accountId) {
        return accountRepository.findById(accountId)
                .orElseThrow(() -> new NotFoundException("Account not found"));
    }
}
