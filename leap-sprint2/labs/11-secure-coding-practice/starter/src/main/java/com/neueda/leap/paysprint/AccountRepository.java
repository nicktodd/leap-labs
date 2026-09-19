package com.neueda.leap.paysprint;

import java.util.Optional;

public interface AccountRepository {
    Optional<Account> findById(Long accountId);
}
