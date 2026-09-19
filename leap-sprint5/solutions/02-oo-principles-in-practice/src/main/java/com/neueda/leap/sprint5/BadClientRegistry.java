package com.neueda.leap.sprint5;

import java.util.ArrayList;

// Kata C: this is the BAD version, given as-is (do not modify it). It extends
// ArrayList<String> purely to reuse storage code - there's no genuine "is-a"
// relationship, and it can't enforce its own rules (e.g. no duplicate client IDs).
// Your task is to write GoodClientRegistry.java (a separate class) that fixes this
// properly using composition. See README.md for what GoodClientRegistry must do.
public class BadClientRegistry extends ArrayList<String> {
}
