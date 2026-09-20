# Module 7 Demo Guide - Introduction to TypeScript: Why Types & Basic Annotations

Everything in this module is JavaScript plus one new idea: a **type** written next to a
variable, parameter, or return value, checked by a separate tool (`tsc`, the TypeScript
compiler) BEFORE the code ever runs. This module deliberately stays narrow - just enough
`tsc` to compile a single file by hand. Module 8 covers a real project's needs beyond that
in depth; nothing here should be treated as the full picture of how a real TypeScript
project is set up.

**Compare to Java, up front:** everyone in the room already writes typed code every day -
Java has never NOT had types. TypeScript adds exactly the same idea to JavaScript,
optionally, checked by a separate compilation step rather than baked into the language
runtime.

**Compare to Python:** Python has optional type hints (`def f(x: int) -> str:`) that look
almost identical to TypeScript's syntax - but Python never enforces them at runtime
without a separate tool like `mypy`. TypeScript's `tsc` is that tool, except running it is
mandatory to produce runnable JavaScript at all (Part 4 explains why).

## Part 1: Primitive Type Annotations

```typescript
const username: string = "alice";
const attemptCount: number = 3;
const isLockedOut: boolean = false;
```

A colon after the name, then the type. Assigning the wrong type to `username` (a number,
for instance) is a compile error - the exact class of mistake plain JavaScript happily
allows and Module 3 never had a way to catch.

## Part 2: Typing a Function

```typescript
function describeOutcome(outcome: string): string {
  if (outcome === "success") {
    return "logged in successfully";
  } else {
    return "failed to log in";
  }
}
console.log(describeOutcome("success"));
```

Verified real output:

```
logged in successfully
```

Each parameter gets a type; the return type comes after the parameter list's closing
`)`. **Compare to Java:** `String describeOutcome(String outcome)` - same information,
reversed order (Java puts the return type first, TypeScript puts it last, after the
parameters).

## Part 3: Typing an Object Shape with an Interface

```typescript
interface Attempt {
  username: string;
  outcome: string;
}

const attempt: Attempt = { username: "alice", outcome: "success" };
console.log(attempt);

function describeAttempt(attempt: Attempt): string {
  return `${attempt.username} ${describeOutcome(attempt.outcome)}`;
}
console.log(describeAttempt(attempt));
```

Verified real output:

```
{ username: 'alice', outcome: 'success' }
alice logged in successfully
```

This is the exact `Attempt` object from Module 4's "Objects vs Java Records" comparison,
which said plainly: *"nothing enforces that every attempt object has both a username AND
an outcome... that flexibility is also the risk: a typo'd key silently becomes undefined,
never a compile error."* An `interface` is TypeScript's answer to exactly that gap - it
writes the object's shape down and has `tsc` enforce it. **Compare to Java:** an
`interface` here is doing almost exactly what a Java `record` does - naming a shape once,
reusable everywhere that shape is needed.

## Part 4: Seeing It Actually Catch a Bug

```bash
npx tsc login-attempt-broken.ts --strict --noEmit
```

`login-attempt-broken.ts` has two deliberate mistakes. Verified real compiler output:

```
login-attempt-broken.ts(18,47): error TS2561: Object literal may only specify known
properties, but 'outcom' does not exist in type 'Attempt'. Did you mean to write
'outcome'?
login-attempt-broken.ts(21,29): error TS2345: Argument of type 'number' is not
assignable to parameter of type 'string'.
```

Mistake 1: `outcom` instead of `outcome` - the exact typo Module 4 said plain JavaScript
would silently accept. TypeScript doesn't just refuse it, it *suggests the fix*.
Mistake 2: passing `200` where `describeOutcome` expects a `string`. Neither of these
would even be visible in plain JavaScript until the code ran and something downstream
broke, possibly in production, long after `outcome` came back `undefined`.

`--noEmit` tells `tsc` to only check, not produce a `.js` file - useful for a demo where
the point is the ERROR, not the output. Without it, `tsc` still reports the same errors
but ALSO writes a `.js` file anyway, unless told otherwise - TypeScript's type checking
and its compilation are two separate steps that happen to run together by default.

## Part 5: Type Erasure - What Actually Runs

Compile the clean version and look at what comes out the other side:

```bash
npx tsc login-attempt.ts --strict
```

The generated `login-attempt.js` has no types in it anywhere - every `: string`,
`: number`, `interface Attempt { ... }` is gone. This is **type erasure**: types exist
only at compile time, purely to let `tsc` check the code, and vanish completely from what
actually runs. Node never sees a single type annotation.

**Compare to Java:** genuinely different here, not just similar-with-different-syntax.
Java's types survive into the compiled `.class` bytecode and are checked again at
runtime in places (an invalid cast still throws `ClassCastException` at runtime).
TypeScript's types are checked once, by `tsc`, and then thrown away - there is no runtime
type safety at all once the JavaScript is running. A `.js` file that started as `.ts` is
exactly as trusting at runtime as a `.js` file that never went through `tsc`.

## Part 6: Type Inference and `any`

TypeScript infers types even without an explicit annotation - it's not required
everywhere, only where it can't be worked out from context:

```typescript
let username = "alice"; // inferred as string, no annotation needed
username = "bob"; // fine - still a string
```

`any` opts a variable OUT of type checking entirely:

```typescript
let riskyValue: any = "alice";
riskyValue = 42; // no error - any accepts anything, which defeats the point
```

Verified real output: no compiler error, `42` prints fine. `any` is sometimes
unavoidable (working with untyped third-party JavaScript, for instance), but reaching
for it routinely throws away everything this module just demonstrated - it's the escape
hatch, not the default.

## A Running Comparison

| TypeScript | Java | Python |
|---|---|---|
| `const x: string` | `String x` | `x: str` (type hint, unenforced without mypy) |
| `function f(x: string): string` | `String f(String x)` | `def f(x: str) -> str:` |
| `interface Attempt { ... }` | `record Attempt(...)` | `dataclass` (unenforced without mypy) |
| Checked once by `tsc`, then erased | Checked at compile time AND partly at runtime | Checked only if `mypy` (or similar) is run |
| `any` | No real equivalent - Java's type system has no escape hatch this total | `Any` from the `typing` module |

## Transition to the Lab

Learners take a small, untyped JavaScript file and add type annotations: primitives,
a typed function, and an `interface` for an object shape already used in the file -
verified by running `tsc --strict` and getting zero errors, then deliberately
reintroducing one of Module 4's typo bugs to see `tsc` catch it.
