package com.neueda.leap.sprint5;

// Kata C: the fix - composition, not inheritance. This class must NOT extend
// ArrayList (or any other collection type). It should HAVE a list internally,
// fully private, exposed only through the small, deliberate interface below.
// TODO:
// - addClient(String clientId): add the client ID; throw IllegalArgumentException
//   if that ID is already present (no duplicates allowed - the rule
//   BadClientRegistry couldn't enforce).
// - contains(String clientId): return true if the ID is present.
// - size(): return the number of registered clients.
public class GoodClientRegistry {

    // TODO: declare a private field here to hold the client IDs

    public void addClient(String clientId) {
        throw new UnsupportedOperationException("TODO: implement addClient");
    }

    public boolean contains(String clientId) {
        throw new UnsupportedOperationException("TODO: implement contains");
    }

    public int size() {
        throw new UnsupportedOperationException("TODO: implement size");
    }
}
