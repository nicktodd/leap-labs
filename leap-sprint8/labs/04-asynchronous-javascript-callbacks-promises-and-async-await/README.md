# Lab 4: Asynchronous JavaScript — Callbacks, Promises & Async/Await

## Task

`report.mjs` checks a list of usernames (`dave`, `erin`, `mallory` - `mallory` is NOT
a known user) against the fake network call in `verify-credentials.mjs`. Two TODOs:

1. **`checkSequentially(usernames)`** — an `async` function that `await`s each
   username's check IN ORDER, using try/catch PER ITERATION so `mallory`'s failure
   doesn't stop `dave` and `erin` from being checked too.
2. **`checkConcurrently(usernames)`** — an `async` function that starts all three
   checks at once with `Promise.allSettled` (not `Promise.all` — that would reject
   the whole thing the moment `mallory` fails, and the task needs every result).

Run it now, before changing anything:

```bash
node report.mjs
```

It throws at TODO 1. That's the starting point.

## Expected Output (once both TODOs are done)

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

Same result both ways — the point of this lab isn't a different answer, it's a
different (and, for three independent checks, faster) way of getting to it.

## A Question Worth Sitting With

`checkSequentially` takes roughly three times as long to run as `checkConcurrently`
in this lab (three 20ms delays back to back, versus three 20ms delays running at the
same time) — with only three usernames, that difference is invisible to a human. At
what point would that difference start to matter to a real user of a real login
screen, and is "always use `Promise.allSettled`" actually the right default, or are
there situations where checking sequentially, one at a time, is the more correct
choice? (Hint: think about what "in order" means for Module 2's consecutive-failure
lockout check.)
