package com.neueda.leap.merchantportal;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
public class MerchantController {

    @Autowired
    private PayoutRepository payoutRepository;

    @Autowired
    private CurrentMerchantProvider currentMerchantProvider;

    // VULNERABILITY (A01): the original version returned any payout request
    // by ID, with no check that the caller is the merchant (or an authorised
    // staff member) it belongs to. Any logged-in merchant could view another
    // merchant's pending/approved payout amounts.
    //
    // FIX (A01): verify the payout belongs to the authenticated merchant
    // before returning it.
    @GetMapping("/api/payouts/{payoutId}")
    public PayoutRequest getPayout(@PathVariable Long payoutId) {
        PayoutRequest payout = payoutRepository.findById(payoutId)
                .orElseThrow(() -> new RuntimeException("Payout not found"));

        if (!payout.getMerchantId().equals(currentMerchantProvider.currentMerchantId())) {
            throw new RuntimeException("Payout not found");
        }

        return payout;
    }
}
