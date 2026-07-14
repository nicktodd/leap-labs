# Module 2 Demo Guide — JavaScript Fundamentals: Syntax, Variables, Functions & Control Flow

First JavaScript of the sprint. No frameworks, no build step, no npm install — just `node` and
two small files. Everything is introduced in order: a concept is never used before it's been
named, and every code example is run for real, not just shown as a snippet next to its output.

## Part 1: Values and Variables

A JavaScript value has a **type** — the ones used today are `string` (text, in quotes),
`number`, and `boolean` (`true`/`false`). A **variable** is a name bound to a value.

```javascript
const username = "alice";   // string
const attemptCount = 3;     // number
const isLockedOut = false;  // boolean
```

`const` declares a variable that can never be reassigned. Try it live:

```javascript
const username = "alice";
username = "bob"; // TypeError: Assignment to constant variable.
```

**Default to `const`.** Only reach for something reassignable when a value genuinely needs to
change after it's created — covered properly once loops are introduced later in this guide.

## Part 2: What Is a Function?

A function is a named, reusable block of code that can take **parameters** (inputs) and produce
a **return value** (an output). Before looking at two different ways to WRITE one, see what one
IS:

```javascript
function shout(word) {
  return word.toUpperCase() + "!";
}

console.log(shout("hello")); // "HELLO!"
```

`word` is the parameter — a placeholder name for whatever gets passed in when the function is
CALLED (`shout("hello")`). `return` sends a value back out to wherever the function was called
from. A function that never calls `return` implicitly returns `undefined`.

## Part 3: Two Ways to Write a Function

Same idea, two syntaxes:

```javascript
function parseAttempt(rawLine) {   // FUNCTION DECLARATION
  // ...
}

const describeOutcome = function (outcome) {  // FUNCTION EXPRESSION
  // ...
};
```

Both are called identically: `parseAttempt(...)`, `describeOutcome(...)`. The difference between
them depends on something not covered yet — **scope** — so it's picked up properly in Part 5,
after scope has an actual name.

## Part 4: Scope — What "Sees" What

**Scope** is the answer to: from this line of code, what variables can I actually see?
`let`/`const` are **block-scoped** — a variable only exists inside the `{ }` it was declared in.

```bash
node scope-demo.js
```

Verified real output:

```
Inside the block: only exists in here
Outside the block: insideBlock is not defined
```

```javascript
if (true) {
  let insideBlock = "only exists in here";
  console.log("Inside the block:", insideBlock);
}
console.log(insideBlock); // ReferenceError - it's gone
```

This is deliberate, useful behaviour: a variable that's only meaningful inside one `if` block
shouldn't be visible (or accidentally reusable) outside it.

### Now, `var` — With a Real Reason, Not Just an Assertion

`var` **ignores block scope**. It "leaks" out to the nearest enclosing function (or, at the top
level, the whole file):

```javascript
if (true) {
  var leaksOut = "declared inside the block...";
}
console.log(leaksOut); // WORKS - var leaked straight through the block
```

Verified real output:

```
Outside the block: declared inside the block... (var leaked out!)
```

**This is the concrete, reproducible reason `var` causes real bugs** — a variable a reader
assumes is local to one `if` or one loop iteration is still hanging around afterwards, and can
silently collide with anything else reusing that name elsewhere in the same function. `let` and
`const` were introduced specifically to fix this. Nobody writing new JavaScript should reach for
`var`.

## Part 5: Hoisting, Now That Scope Has a Name

Back to Part 3's two function forms. **Hoisting** means: a function DECLARATION is fully set up
before any code in its scope runs — so it's callable even from a line that appears earlier in
the file. A function EXPRESSION is just a variable assignment, and — like any `const`/`let` — it
doesn't exist until that assignment line actually executes.

Demonstrate live: temporarily move the call to `parseAttempt` above its own definition in
`login-attempts.js` and rerun — it still works. Do the same with `describeOutcome` — it throws
`Cannot access 'describeOutcome' before initialization`.

## Part 6: Control Flow

Every example below is shown as complete, runnable code, followed by what actually happens when
it runs — never one without the other.

### `if` / `else`

```javascript
function describeOutcome(outcome) {
  if (outcome === "success") {
    return "logged in successfully";
  } else {
    return "failed to log in";
  }
}

console.log(describeOutcome("success"));
console.log(describeOutcome("fail"));
```

Real output:

```
logged in successfully
failed to log in
```

`===` compares value AND type. `==` silently converts types first (`"1" == 1` is `true`) — a
real, frequently-cited source of bugs. Always use `===`.

### `for`

```javascript
const rawAttempts = ["alice,success", "bob,fail", "alice,success"];

for (let i = 0; i < rawAttempts.length; i++) {
  console.log(i, rawAttempts[i]);
}
```

Real output:

```
0 alice,success
1 bob,fail
2 alice,success
```

`i` starts at `0`, the loop runs while `i < rawAttempts.length`, and `i++` increments it after
each pass — the classic counting loop, iterating an array by index.

### `while`

```javascript
let count = 0;
while (count < 3) {
  console.log("count is", count);
  count = count + 1;
}
```

Real output:

```
count is 0
count is 1
count is 2
```

Use `while` when the stopping condition isn't naturally "count from 0 to N" — `login-attempts.js`
uses one to stop as soon as a repeat offender is found, OR the list runs out, whichever comes
first: `while (index < rawAttempts.length && lockedOutUser === null)`.

## Part 7: Everything Together — the Full Demo

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

Walk through the file top to bottom: variables (Part 1), two function forms (Part 3), a `for`
loop building a summary (Part 6), a `while` loop checking a stopping condition based on real
data, not just a count (Part 6).

## A Deliberate Preview, Named Honestly

`parseAttempt` returns `{ username: username, outcome: outcome }` — an object literal. That's
genuinely Module 3 content, appearing one module early. Say so directly: today's task doesn't
require understanding objects deeply, only that a function can bundle more than one return value
together. Module 3 revisits this exact function and makes it more idiomatic.

## Transition to the Lab

Learners write their own version processing a different (given) list of login attempts —
building the parsing function, the outcome-describing function, and the `for` loop themselves,
verified by running the script and checking the printed summary against expected counts.
