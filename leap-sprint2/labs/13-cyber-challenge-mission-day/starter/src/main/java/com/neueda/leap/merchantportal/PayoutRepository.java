package com.neueda.leap.merchantportal;

import java.util.Optional;

public interface PayoutRepository {
    Optional<PayoutRequest> findById(Long payoutId);
    PayoutRequest save(PayoutRequest payout);
}
