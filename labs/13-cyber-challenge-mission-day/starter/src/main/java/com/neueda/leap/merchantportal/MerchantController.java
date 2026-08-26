package com.neueda.leap.merchantportal;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
public class MerchantController {

    @Autowired
    private PayoutRepository payoutRepository;

    @GetMapping("/api/payouts/{payoutId}")
    public PayoutRequest getPayout(@PathVariable Long payoutId) {
        return payoutRepository.findById(payoutId)
                .orElseThrow(() -> new RuntimeException("Payout not found"));
    }
}
