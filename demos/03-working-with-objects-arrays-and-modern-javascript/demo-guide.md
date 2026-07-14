# Module 3 Demo Guide — Working with Objects, Arrays & Modern JavaScript

This module takes Module 2's `login-attempts.js` and rebuilds it with what real-world
JavaScript actually looks like: objects and arrays as first-class data, destructuring,
spread/rest, arrow functions, and code split across ES modules instead of one file.
Nothing here is a new problem to solve — it's the same login-attempts problem, written
properly.

## Part 1: Objects and Arrays as Core Data Structures

An **object** groups related values under named keys:

```javascript
const attempt = { username: "alice", outcome: "success" };
console.log(attempt);
```

Real output:

```
{ username: 'alice', outcome: 'success' }
```

An **array** is an ordered list of values:

```javascript
const usernames = ["alice", "bob", "carol"];
console.log(usernames);
```

Real output:

```
[ 'alice', 'bob', 'carol' ]
```

Module 2 already used both without naming them: `parseAttempt` returned an object
(`{ username: username, outcome: outcome }`), and `rawAttempts` was an array. Nothing new
is happening here — this module just gives those two shapes their proper names and shows
what else they can do.

## Part 2: Destructuring

**Destructuring** pulls values out of an object or array into their own named variables,
instead of accessing them one property/index at a time.

Object destructuring:

```javascript
const attempt = { username: "alice", outcome: "success" };
const { username, outcome } = attempt;
console.log(username, outcome);
```

Real output:

```
alice success
```

Array destructuring:

```javascript
const usernames = ["alice", "bob", "carol"];
const [first, second, third] = usernames;
console.log(first, second, third);
```

Real output:

```
alice bob carol
```

Object destructuring pulls by **name**; array destructuring pulls by **position**. Compare
this to Module 2's `parseAttempt`, which did the array-position version manually with
`parts[0]` and `parts[1]` — destructuring is that same idea, built into the language.

## Part 3: Spread and Rest

Both use `...`, but in opposite directions.

**Spread** expands a collection out:

```javascript
const morning = ["alice", "bob"];
const afternoon = ["carol"];
const everyone = [...morning, ...afternoon];
console.log(everyone);
```

Real output:

```
[ 'alice', 'bob', 'carol' ]
```

It works on objects too — useful for adding a field without mutating the original:

```javascript
const base = { username: "alice", outcome: "success" };
const withTimestamp = { ...base, timestamp: "09:00" };
console.log(withTimestamp);
```

Real output:

```
{ username: 'alice', outcome: 'success', timestamp: '09:00' }
```

**Rest** does the opposite — it gathers any number of arguments INTO an array, inside a
function's parameter list:

```javascript
const logAll = (label, ...items) => {
  console.log(label, items);
};
logAll("usernames:", "alice", "bob", "carol");
```

Real output:

```
usernames: [ 'alice', 'bob', 'carol' ]
```

`label` takes the first argument; `...items` takes everything after it, however many
there are.

## Part 4: Arrow Functions

A third way to write a function, on top of Module 2's declaration and expression forms:

```javascript
const square = (n) => n * n;
console.log(square(4));
```

Real output:

```
16
```

One parameter, one expression, no `function` keyword, no `return` keyword — the
expression's value is returned automatically. With a full function body, `return` is
needed again, same as before:

```javascript
const greet = (name) => {
  return `hello ${name}`;
};
console.log(greet("alice"));
```

Real output:

```
hello alice
```

Arrow functions are **function expressions** under the hood — Module 2's rule still
applies: not hoisted, doesn't exist until the assignment line runs.

## Part 5: ES Modules — Splitting Code Across Files

Everything so far has lived in one file per demo. Real projects split code by
responsibility and connect the pieces with `export`/`import`.

`attempts-data.mjs` — just the data, exported:

```javascript
export const morningAttempts = [
  { username: "alice", outcome: "success" },
  { username: "bob", outcome: "fail" },
  { username: "alice", outcome: "success" },
];

export const afternoonAttempts = [
  { username: "carol", outcome: "fail" },
  { username: "bob", outcome: "fail" },
  { username: "alice", outcome: "fail" },
];
```

`report.mjs` — imports it by name:

```javascript
import { morningAttempts, afternoonAttempts } from "./attempts-data.mjs";
```

The `.mjs` extension is what tells Node to treat the file as an ES module (so `import`/
`export` work) without needing a build tool or a `package.json` change. This is the same
`import`/`export` syntax used throughout TypeScript and NestJS later in this sprint.

## Part 6: Everything Together — the Full Demo

```bash
node report.mjs
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

First attempt: alice, second attempt: bob
```

Walk through `report.mjs` top to bottom and point at each concept as it appears:

- `describeOutcome` — an arrow function with an object destructured directly in its
  parameter list (Parts 2 and 4 combined)
- `allAttempts` — two imported arrays combined with spread (Part 3)
- `summarize` — same destructuring-in-a-loop idea as Module 2, now over objects
- `checkLockouts` — a rest parameter (`...usernames`) letting it check any number of
  users without an array argument (Part 3)
- `[firstAttempt, secondAttempt]` — array destructuring on the combined list (Part 2)

Same behaviour as Module 2's script, same `bob` lockout result — because it's genuinely
the same data and the same logic, just expressed with the tools this module introduces.

## Transition to the Lab

Learners take Module 2's `login-attempts.js` (the string-parsing version) and refactor it
into this module's style: object/array data, destructuring, arrow functions, and split
across two `.mjs` files — verified by confirming the printed output matches Module 2's
original, unchanged.
