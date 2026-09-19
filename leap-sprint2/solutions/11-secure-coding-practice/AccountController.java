package com.neueda.leap.paysprint;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
public class AccountController {

    @Autowired
    private AccountRepository accountRepository;

    @Autowired
    private CurrentUserProvider currentUserProvider;

    // VULNERABILITY (A01): the original version fetched whatever account ID
    // was in the URL, with no check that it belonged to the currently
    // authenticated user, an IDOR letting any user view any account.
    //
    // FIX (A01): verify the account belongs to the authenticated caller
    // before returning it.
    @GetMapping("/api/accounts/{accountId}")
    public Account getAccount(@PathVariable Long accountId) {
        Account account = accountRepository.findById(accountId)
                .orElseThrow(() -> new NotFoundException("Account not found"));

        if (!account.getOwnerId().equals(currentUserProvider.currentUserId())) {
            throw new NotFoundException("Account not found");
        }

        return account;
    }
}
