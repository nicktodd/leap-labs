package com.neueda.leap.merchantportal;

import org.springframework.web.bind.annotation.*;

@RestController
public class WebhookController {

    private static final String WEBHOOK_SHARED_SECRET = System.getenv("PAYMENT_WEBHOOK_SECRET");

    private PayoutStatusUpdater payoutStatusUpdater;

    // VULNERABILITY (A08): the original endpoint received payment-status
    // updates from an external payment provider and applied them directly,
    // with no verification that the request actually came from that provider
    // (no HMAC signature check, no shared secret, nothing). Anyone who could
    // reach this URL could mark any payout as "settled".
    //
    // FIX (A08): verify an HMAC signature (computed with a shared secret,
    // provided by the payment provider) over the raw request body before
    // trusting anything in the payload. Reject the request entirely if the
    // signature is missing or doesn't match.
    @PostMapping("/api/webhooks/payment-status")
    public void handlePaymentStatusWebhook(
            @RequestBody PaymentStatusEvent event,
            @RequestHeader("X-Payment-Signature") String providedSignature,
            @RequestBody(required = false) String rawBody) {

        String expectedSignature = HmacUtil.sign(rawBody, WEBHOOK_SHARED_SECRET);
        if (!HmacUtil.constantTimeEquals(expectedSignature, providedSignature)) {
            throw new SecurityException("Invalid webhook signature");
        }

        payoutStatusUpdater.markSettled(event.getPayoutId(), event.getStatus());
    }
}
