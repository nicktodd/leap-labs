# Module 2 Demo Guide — JavaScript Fundamentals: Syntax, Variables, Functions & Control Flow

First JavaScript of the sprint. No frameworks, no build step, no npm install — just `node` and a
single file. Everything here is deliberately plain: variables, functions, and control flow,
applied to something already familiar from Module 1 — a short log of login attempts.

## Run It

```bash
node login-attempts.js
```

Verified real output:

```
alice logged in successfully
bob failed to log in
alice logged in successfully
carol failed to log in
bob failed to log in
alice failed to log in

Summary: 2 successful, 4 failed
bob had 2+ consecutive failures - would trigger a lockout in a real system
```

## Walk Through It, Piece by Piece

### Variables: `const` vs `let`

```javascript
const rawAttempts = [ ... ];   // never reassigned
let successCount = 0;          // reassigned every loop iteration
```

**Rule of thumb, stated explicitly**: default to `const`. Only reach for `let` when a value
genuinely needs to change after it's created — `successCount` does (it's incremented every
successful attempt); `rawAttempts` doesn't (the array itself is never replaced with a different
array, even though — foreshadowing Module 3 — its *contents* technically could be mutated).

Point out `var` exists in older JavaScript and is deliberately not used here — it has confusing
scoping rules `let`/`const` were introduced specifically to fix. Nobody writing new JavaScript in
2026 should reach for `var`.

### Functions: two ways to write one

```javascript
function parseAttempt(rawLine) { ... }        // function DECLARATION

const describeOutcome = function (outcome) { ... };  // function EXPRESSION
```

Both are called the same way (`parseAttempt(...)`, `describeOutcome(...)`). The practical
difference worth naming today: a function **declaration** is hoisted — usable even from code that
appears earlier in the file than the declaration itself. A function **expression** is not — it
only exists from the point of assignment onward. Demonstrate live: temporarily move the
`parseAttempt` call above its declaration and show it still works; do the same with
`describeOutcome` and show it throws.

### Control Flow: `if`/`else`, `for`, `while`

- `if (outcome === "success") { ... } else { ... }` — note `===`, not `==`. JavaScript's `==`
  performs type coercion (`"1" == 1` is `true`); `===` does not. Default to `===` always; `==`
  is a real, frequently-cited source of bugs.
- `for (let i = 0; i < rawAttempts.length; i++)` — the classic counting loop, iterating over an
  array by index.
- `while (index < rawAttempts.length && lockedOutUser === null)` — used specifically because the
  loop's stopping condition ("found a repeat offender, OR ran out of attempts") isn't naturally
  "count from 0 to N." Point out the `&&` — both conditions must hold for the loop to continue.

## A Deliberate Preview, Named Honestly

`parseAttempt` returns `{ username: username, outcome: outcome }` — an object literal. That's
genuinely Module 3 content, appearing one module early. Say so directly: today's task doesn't
require understanding objects deeply, only that a function can bundle more than one return value
together. Module 3 revisits this exact function and makes it more idiomatic.

## Transition to the Lab

Learners write their own version processing a different (given) list of login attempts —
building the parsing function, the outcome-describing function, and both loop styles themselves,
verified by running the script and checking the printed summary against expected counts.
