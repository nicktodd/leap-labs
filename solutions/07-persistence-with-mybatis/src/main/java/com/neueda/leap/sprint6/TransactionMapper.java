package com.neueda.leap.sprint6;

import java.util.List;

// Given - the interface for Kata B (XML-based). You'll write the SQL in
// TransactionMapper.xml, not here.
public interface TransactionMapper {

    List<Transaction> findByAccountId(int accountId);
}
