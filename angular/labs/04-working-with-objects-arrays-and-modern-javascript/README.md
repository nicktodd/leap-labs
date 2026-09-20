# Lab 4: Working with Objects, Arrays & Modern JavaScript

## Task

`report.mjs` is Module 3's `login-attempts.js`, half-refactored into this module's style,
importing data from `attempts-data.mjs`. Three TODOs, in order:

1. **`allAttempts`** - combine `morningAttempts` and `afternoonAttempts` using the spread
   operator.
2. **`describeOutcome`** - an arrow function, destructuring `{ username, outcome }` in its
   parameter list, using if/else.
3. **`isLockedOut`** and **`checkLockouts`** - `checkLockouts` is given, using a rest
   parameter (`...usernames`); you write `isLockedOut(attempts, username)`, the same
   consecutive-failure check as Module 3's `while` loop.

Run it now, before changing anything:

```bash
node report.mjs
```

It throws at TODO 1. That's the starting point - work through the TODOs in order, rerunning
after each one.

## Expected Output (once all three TODOs are done)

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

## A Question Worth Sitting With

`checkLockouts(allAttempts, "dave", "erin", "frank")` passes three specific usernames by
hand. What would you change so it checks every username that actually appears in
`allAttempts`, without anyone having to list them? (You don't need to implement it - just
say what you'd reach for. A hint: you already have the tools from Part 3 of the demo guide.)
