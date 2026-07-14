# Module 3 Demo Guide — Working with Objects, Arrays & Modern JavaScript

This module takes Module 2's `login-attempts.js` and rebuilds it with what real-world
JavaScript actually looks like: objects and arrays as first-class data, destructuring,
spread/rest, arrow functions, template literals, and code split across ES modules
instead of one file. Nothing here is a new problem to solve — it's the same
login-attempts problem, written properly.

Everyone in the room already knows Java (Sprint 5) and Python (Sprint 4). Every new
JavaScript idea in this module has a direct equivalent in at least one of those
languages — the fastest way in is naming that equivalent, then showing where the
JavaScript version differs.

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

**Compare to Java:** an object literal like this is doing the job of a small class —
roughly a `record Attempt(String username, String outcome)`, minus the type
declaration and the need to define the shape anywhere in advance. There's no
`Attempt` class to write; the object's shape is just whatever keys you give it. That's
a real trade-off, not a free upgrade: Java's `record` catches a typo in a field name
at compile time; JavaScript's object literal doesn't catch it at all until the code
runs and the value is `undefined`.

An **array** is an ordered list of values:

```javascript
const usernames = ["alice", "bob", "carol"];
console.log(usernames);
```

Real output:

```
[ 'alice', 'bob', 'carol' ]
```

**Compare to Java:** this is closer to a `List<String>` than a raw Java array — it
resizes freely (`push`, `pop`, `splice`), same as `ArrayList`. There's no
`List<String> usernames = new ArrayList<>();` ceremony and no generic type parameter;
the array just holds whatever you put in it, of any type, mixed if you really want to
(don't).

Module 2 already used both without naming them: `parseAttempt` returned an object
(`{ username: username, outcome: outcome }`), and `rawAttempts` was an array. Nothing
new is happening here — this module just gives those two shapes their proper names and
shows what else they can do.

## Part 2: Destructuring

**Destructuring** pulls values out of an object or array into their own named
variables, instead of accessing them one property/index at a time.

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

**Compare to Java:** there is no direct Java equivalent for this — Java has no syntax
for unpacking a record's fields into loose local variables in one step (`var username
= attempt.username(); var outcome = attempt.outcome();` is the closest, and it's two
lines, not one). Java 21's `record` pattern matching in `switch`/`instanceof` is the
nearest cousin (`if (attempt instanceof Attempt(var username, var outcome))`), but
it's a pattern-match construct, not a plain assignment — worth mentioning if anyone in
the room has touched Java 21, otherwise skip it.

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

**Compare to Java:** this one Python developers in the room will recognise instantly —
it's Python's tuple unpacking (`first, second, third = usernames`), same idea, slightly
different punctuation. Java has nothing like it for arrays or lists at all; the closest
is manually indexing (`String first = usernames.get(0);`).

Object destructuring pulls by **name**; array destructuring pulls by **position**.
Compare this to Module 2's `parseAttempt`, which did the array-position version
manually with `parts[0]` and `parts[1]` — destructuring is that same idea, built into
the language.

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

**Compare to Java:** this replaces the mild ceremony of combining two lists —
`List<String> everyone = new ArrayList<>(morning); everyone.addAll(afternoon);`, or
`Stream.concat(morning.stream(), afternoon.stream()).toList()` if reaching for
streams. Spread does the same job as `Stream.concat` in one expression, without
building a `Stream` to do it.

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

**Compare to Java:** this is the same shape as a Java `record`'s "wither" pattern —
`record Attempt(String username, String outcome, String timestamp)` has no built-in
way to say "same as this one, but with a timestamp added" without a custom method;
spread gives JavaScript that for free, at the cost of Java's compile-time field
checking.

**Rest** does the opposite — it gathers any number of arguments INTO an array, inside
a function's parameter list:

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

**Compare to Java:** this is JavaScript's version of **varargs** —
`void logAll(String label, String... items)`. Same idea, same "gather everything after
the named parameters into an array-like thing," different syntax (`...items` at the
front of the name instead of `String...` before it).

`label` takes the first argument; `...items` takes everything after it, however many
there are.

## Part 4: Arrow Functions

A third way to write a function, on top of Module 2's declaration and expression
forms:

```javascript
const square = (n) => n * n;
console.log(square(4));
```

Real output:

```
16
```

**Compare to Java:** an arrow function is JavaScript's lambda expression —
`(n) => n * n` reads almost identically to Java's `n -> n * n`. Same motivation too:
a short, throwaway function passed around as a value, without the ceremony of a full
method declaration.

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

### Template Literals, While We're Building Strings

Run live from `bonus-examples.mjs` (`node bonus-examples.mjs`) alongside Part 5 below.

Backtick strings embed expressions directly with `${...}`, instead of `+`-concatenation:

```javascript
const username = "alice";
const attemptCount = 3;
console.log(`${username} has made ${attemptCount} attempts`);
```

Real output:

```
alice has made 3 attempts
```

**Compare to Java:** this is JavaScript's `String.format("%s has made %d attempts",
username, attemptCount)`, or Java 15+'s own text-block-adjacent formatted strings —
except the value goes directly inline in the string, not as a separate positional
argument, so there's no risk of the arguments being in the wrong order.

## Part 5: Two Array Methods Worth Knowing Now (map, filter)

These aren't in this module's formal objectives, but they're the natural next step
once arrow functions and arrays are both in place, and they map directly onto
something Java developers already know: **streams**.

```javascript
const attempts = [
  { username: "alice", outcome: "success" },
  { username: "bob", outcome: "fail" },
];
const usernames = attempts.map((a) => a.username);
console.log(usernames);
```

Real output:

```
[ 'alice', 'bob' ]
```

**Compare to Java:** `attempts.stream().map(a -> a.username()).toList()`. JavaScript's
`.map()` doesn't need `.stream()` first or `.toList()` after — arrays already have
these methods directly on them.

```javascript
const failed = attempts.filter((a) => a.outcome === "fail");
console.log(failed);
```

Real output:

```
[ { username: 'bob', outcome: 'fail' } ]
```

**Compare to Java:** `attempts.stream().filter(a -> a.outcome().equals("fail")).toList()`.
Same idea again — `.filter()` is directly on the array, no stream pipeline required.
These aren't required for this module's lab, but they're worth a mention: Module 3's
`report.mjs` walks arrays with `for...of` loops for now, deliberately, because that's
what's actually being taught here — `.map()`/`.filter()` are a preview of where this
naturally goes.

## Part 6: ES Modules — Splitting Code Across Files

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

**Compare to Java:** `export` is JavaScript's `public`, applied per-declaration rather
than per-class; `import { x } from "./file.mjs"` is doing the same job as Java's
`import com.fidelity.attempts.Data;`, except the "package" here is just a relative file
path, not a directory structure mapped to a namespace. There's no `package` declaration
to keep in sync with the folder layout — the file path *is* the reference.

The `.mjs` extension is what tells Node to treat the file as an ES module (so `import`/
`export` work) without needing a build tool or a `package.json` change. This is the
same `import`/`export` syntax used throughout TypeScript and NestJS later in this
sprint.

## Part 7: Everything Together — the Full Demo

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

## A Running Comparison Table

Worth putting up as a reference while the room works through the lab:

| JavaScript | Closest Java equivalent | Closest Python equivalent |
|---|---|---|
| Object literal `{ a, b }` | `record`, minus compile-time shape checking | `dict` / dataclass |
| Array `[...]` | `ArrayList<T>` / `List<T>` | `list` |
| Object destructuring | No direct equivalent (Java 21 record patterns come close) | `dict` unpacking via `**` in limited contexts |
| Array destructuring | No direct equivalent | Tuple unpacking (`a, b = items`) |
| Spread `...arr` | `Stream.concat(...)` / `addAll` | `*args` unpacking into a call, or `[*a, *b]` |
| Rest `...args` | Varargs (`String... items`) | `*args` |
| Arrow function | Lambda (`x -> x * 2`) | Lambda (`lambda x: x * 2`) |
| Template literal | `String.format(...)` | f-string |
| `export` / `import` | `public` + `import` (package-based) | `import` (module-based) |

## Transition to the Lab

Learners take Module 2's `login-attempts.js` (the string-parsing version) and refactor
it into this module's style: object/array data, destructuring, arrow functions, and
split across two `.mjs` files — verified by confirming the printed output matches
Module 2's original, unchanged.
