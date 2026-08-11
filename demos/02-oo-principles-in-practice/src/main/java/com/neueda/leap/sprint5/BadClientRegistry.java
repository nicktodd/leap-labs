package com.neueda.leap.sprint5;

import java.util.ArrayList;

// BAD inheritance, on purpose - a real, common mistake. It's tempting: extending
// ArrayList<Client> gives you add(), get(), size(), iteration, all "for free."
// But a ClientRegistry is not an ArrayList - there's no genuine "is-a" relationship,
// only a desire to reuse ArrayList's storage code. This is inheritance used purely
// for code reuse, not because the "is-a" test actually holds.
//
// What goes wrong in practice: ArrayList<Client> also exposes remove(int index),
// set(int index, Client c), sort(Comparator), addAll(Collection), and every other
// ArrayList method - none of which a "client registry" necessarily wants to expose
// or guarantee the behaviour of. Callers can now bypass any registry-specific rule
// (e.g. "no duplicate client IDs") by calling an inherited ArrayList method
// directly. The registry has no control over its own interface any more.
public class BadClientRegistry extends ArrayList<String> {
    // Deliberately empty: everything is "inherited" from ArrayList, which is
    // exactly the problem - this class has no way to add its own rules.
}

// The fix (see GoodClientRegistry.java in the solution): use COMPOSITION instead -
// a ClientRegistry that HAS an internal List, wrapped behind a small, deliberate
// interface it fully controls, rather than IS-A ArrayList with every ArrayList
// method along for the ride.
