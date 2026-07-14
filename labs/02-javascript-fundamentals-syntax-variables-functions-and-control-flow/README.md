# Module 2 Lab — JavaScript Fundamentals: Syntax, Variables, Functions & Control Flow

## Objectives

By the end of this lab you will have:

- Written your first real JavaScript functions — a declaration and an expression
- Used `if`/`else` and a `for` loop to process a list and build up a summary
- Run a script with `node` and read a real stack trace when something isn't implemented yet

## Setup

```bash
cd labs/02-javascript-fundamentals-syntax-variables-functions-and-control-flow
node login-attempts.js
```

You should see `Summary: 0 successful, 0 failed`, then a crash — `Error: TODO 1: implement
parseAttempt`. That's the starting point: two functions and one loop aren't implemented yet.

## Task

### TODO 1 — `parseAttempt`

Given a string like `"dave,success"`, split it on the comma and return an object with a
`username` and an `outcome` property. `"dave,success"` should behave like
`{ username: "dave", outcome: "success" }`.

### TODO 2 — `describeOutcome`

Given an outcome string, return `"logged in successfully"` if it's `"success"`, otherwise return
`"failed to log in"`. Use `if`/`else` explicitly — don't reach for a shortcut you haven't been
shown yet.

### TODO 3 — the `for` loop

Loop over `rawAttempts` by index. For each entry: call `parseAttempt`, then `describeOutcome`,
print a line in the format `<username> <description>`, and increment `successCount` or
`failCount` depending on the outcome.

### Run It

```bash
node login-attempts.js
```

## Deliverable

A working `login-attempts.js` that prints one line per attempt, then
`Summary: 3 successful, 3 failed`, then a lockout line naming a specific user.

## A Question Worth Sitting With

Once your script runs, look closely at who gets named in the lockout line, and why. The
consecutive-failure check counts fails *across the whole list*, not per user — so it's possible
for one user's failure to be "blamed" on a lockout that was really triggered by two DIFFERENT
users failing back to back. Is that a bug, or a deliberately simple (if slightly wrong) first
version of a real security check? Be ready to explain your answer — there's a defensible case
either way, and Module 3's refactor doesn't fix this, on purpose.

## Acceptance criteria

- `node login-attempts.js` runs to completion with no errors
- Output shows `3 successful, 3 failed`
- The lockout line names a specific user, not `null`/`undefined`
- You can explain, in one sentence, why the lockout logic might name a user who didn't actually
  fail twice in a row themselves
