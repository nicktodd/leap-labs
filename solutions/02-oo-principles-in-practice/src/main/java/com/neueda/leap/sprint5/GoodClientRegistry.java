package com.neueda.leap.sprint5;

import java.util.ArrayList;
import java.util.List;

// Composition, not inheritance: this class HAS a List internally, fully private,
// exposed only through the small interface below - not every ArrayList method.
public class GoodClientRegistry {

    private final List<String> clientIds = new ArrayList<>();

    public void addClient(String clientId) {
        if (clientIds.contains(clientId)) {
            throw new IllegalArgumentException("client already registered: " + clientId);
        }
        clientIds.add(clientId);
    }

    public boolean contains(String clientId) {
        return clientIds.contains(clientId);
    }

    public int size() {
        return clientIds.size();
    }
}
