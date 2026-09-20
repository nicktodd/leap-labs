# Lab 4 Model Answers

## Verified Output

```
dave logged in successfully
erin failed to log in
dave failed to log in
dave failed to log in
frank logged in successfully
erin logged in successfully

Summary: 3 successful, 3 failed
dave had 2+ consecutive failures - would trigger a lockout in a real system
```

Only `dave` is locked out. `erin` fails once (`erin,fail` in the morning) but then succeeds
in the afternoon, so her consecutive-fail count resets to 0 before hitting 2 - same
per-user, sequence-sensitive logic as Module 3, just applied to this lab's dataset.

## Key Points

- **TODO 1** is a one-liner once spread is understood: `[...morningAttempts,
  ...afternoonAttempts]`. The common mistake is reaching for `.concat()` out of habit -
  not wrong, just not what this module is practising.
- **TODO 2** combines two ideas from this module in one line: destructuring `{ username, outcome }`
  directly in the arrow function's parameter list, so the body never touches
  `attempt.username` or `attempt.outcome` directly.
- **TODO 3**: `checkLockouts` is given as the rest-parameter example; `isLockedOut` is a
  plain per-user loop, identical in spirit to Module 3's `while` loop, just scoped to one
  username at a time and reusable.

## The Reflection Question

Checking every username without listing them by hand needs the actual set of usernames
present in `allAttempts`, not a hardcoded list. That's a job for the same tools this module
introduced: map each attempt to its `username` (an idea this module previews further with
array methods), then de-duplicate - e.g. `[...new Set(allAttempts.map((a) => a.username))]`
uses spread again, this time to turn a `Set` back into an array. Nobody is expected to
produce this unprompted; it's a preview of where destructuring/spread naturally leads once
array methods are available.
