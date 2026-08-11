package com.neueda.leap.sprint5;

import java.util.ArrayList;
import java.util.List;

public class GoodClientRegistry {

    private final List<String> clients = new ArrayList<>();

    public void addClient(String clientId) {
        if (clients.contains(clientId)) {
            throw new IllegalArgumentException("Client already registered: " + clientId);
        }
        clients.add(clientId);
    }

    public boolean contains(String clientId) {
        return clients.contains(clientId);
    }

    public int size() {
        return clients.size();
    }
}
