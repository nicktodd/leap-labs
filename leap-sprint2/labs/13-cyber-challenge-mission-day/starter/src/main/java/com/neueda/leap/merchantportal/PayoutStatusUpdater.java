package com.neueda.leap.merchantportal;

public interface PayoutStatusUpdater {
    void markSettled(Long payoutId, String status);
}
