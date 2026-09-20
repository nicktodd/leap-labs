package com.neueda.leap.merchantportal;

import org.springframework.web.bind.annotation.*;

@RestController
public class WebhookController {

    @PostMapping("/api/webhooks/payment-status")
    public void handlePaymentStatusWebhook(@RequestBody PaymentStatusEvent event) {
        payoutStatusUpdater.markSettled(event.getPayoutId(), event.getStatus());
    }

    private PayoutStatusUpdater payoutStatusUpdater;
}
