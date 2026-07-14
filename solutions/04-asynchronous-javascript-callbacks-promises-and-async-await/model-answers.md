# Lab 4 Model Answers

## Verified Output

```
--- sequential ---
Verified: dave
Verified: erin
Not verified: mallory (Unknown user: mallory)
--- concurrent ---
Verified: dave
Verified: erin
Not verified: mallory (Unknown user: mallory)
```

## Key Points

- **TODO 1**: try/catch has to sit INSIDE the loop body, not around the whole loop —
  around the whole loop, `mallory`'s rejection would throw past `dave` and `erin` if
  they came after her in the list, aborting the rest of the check.
- **TODO 2**: `Promise.allSettled` never rejects — every entry in the returned array
  is `{ status: "fulfilled", value }` or `{ status: "rejected", reason }`, so all
  three outcomes are always available, regardless of how many failed. `Promise.all`
  would have rejected the whole call the instant `mallory`'s promise rejected,
  losing `dave` and `erin`'s results entirely.

## The Reflection Question

Concurrent (`Promise.allSettled`) is strictly better here BECAUSE the three checks
are independent — checking `dave` has no bearing on checking `erin`. Module 2's
consecutive-failure lockout check is the opposite case: it deliberately needs
sequence, because "2+ consecutive failures" is only a meaningful question when the
attempts are examined in the order they actually happened. Running lockout checks
concurrently wouldn't just be pointless, it would be wrong — there'd be no
"consecutive" to detect. The rule isn't "concurrent is always faster so always use
it" - it's "run things concurrently only when they're actually independent of each
other," the same judgement call that applies to parallelising anything, in any
language.
