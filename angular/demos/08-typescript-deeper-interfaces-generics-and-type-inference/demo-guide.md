# Module 8 Demo Guide - TypeScript Deeper: Interfaces, Generics & Type Inference

Module 7 covered the basics: an `interface` names a shape, `tsc` enforces it. This
module covers what a real project actually needs beyond that - extending interfaces,
optional and `readonly` fields, method signatures, generics, and two inference
behaviours that only show up once generics are involved.

## Part 1: Interfaces, Deeper

```bash
node interfaces-deeper.js
```

**Extending an interface** - `Attempt` gets everything `BaseRecord` has, plus its own
fields:

```typescript
interface BaseRecord {
  readonly id: number;
  createdAt: string;
}

interface Attempt extends BaseRecord {
  username: string;
  outcome: string;
  notes?: string; // OPTIONAL - the ? means this key can be omitted
}
```

**Compare to Java:** `extends` here reads almost identically to a Java interface
extending another interface - `interface Attempt extends BaseRecord`. The optional `?`
has no clean Java equivalent; the nearest comparison is `Optional<String> notes`, which
is a wrapper TYPE rather than a modifier on the field itself.

**`readonly`** is enforced by `tsc`, not just documentation:

```typescript
attempt.id = 2; // error TS2540: Cannot assign to 'id' because it is a read-only property.
```

Verified real compiler output - try uncommenting that line in `interfaces-deeper.ts`
and rerunning `npx tsc interfaces-deeper.ts --strict --noEmit`. **Compare to Java:**
`readonly` is TypeScript's `final` on a field.

**A method signature inside an interface** - not just data, a shape that includes
behaviour:

```typescript
interface Verifier {
  verify(username: string): boolean;
}
```

This is exactly a Java interface with one abstract method - the same shape Module 7's
`describeOutcome` would take if it were an OBJECT'S method instead of a standalone
function.

Verified real output:

```
{
  id: 1,
  createdAt: '2026-01-01T09:00:00Z',
  username: 'alice',
  outcome: 'success'
}
true
false
```

## Part 2: Generics

```bash
node generics-demo.js
```

A **generic** is a type parameterised by another type, written in angle brackets - the
same `<T>` shape Java has used since generics arrived in Java 5.

**A generic function:**

```typescript
function first<T>(items: T[]): T | undefined {
  return items[0];
}

const firstUsername = first(["alice", "bob", "carol"]); // T inferred as string
const firstCount = first([3, 1, 4]); // T inferred as number
```

One function, works for an array of strings, numbers, or anything else - without
`any`, and without writing a separate function per type. **Compare to Java:**
`<T> T first(List<T> items)` - nearly identical syntax and behaviour, generics work the
same way in both languages.

**A generic interface** - `Result<T>` wraps a success value of ANY type `T`, without a
separate `Result` type for every kind of value:

```typescript
interface Result<T> {
  success: boolean;
  value?: T;
  error?: string;
}

function verifyCredentials(username: string): Result<{ username: string }> {
  // ...
}
```

Verified real output:

```
alice
3
Verified: alice
Error: Unknown user: mallory
```

This is the shape Module 6's async error handling was reaching for informally -
`Result<T>` names it properly: a value that's either a success (with a `value`) or a
failure (with an `error`), known at compile time, not discovered by checking `if (err)`
at runtime.

**A constrained generic** - `T extends { username: string }` means `T` can be ANY
shape, as long as it has at least a `username` field:

```typescript
function describeByUsername<T extends { username: string }>(record: T): string {
  return `Record for ${record.username}`;
}
```

Verified real output:

```
Record for alice
Record for bob
```

Works on an `Attempt`-shaped object AND a `Verification`-shaped object (Module 6) -
anything with at least a `username`. **Compare to Java:** `<T extends Named>` - Java's
bounded type parameters work identically, constraining `T` to types that implement a
given interface (or, in TypeScript's case, that merely HAVE a given shape).

## Part 3: Type Inference, Deeper

```bash
node inference-deeper.js
```

**Return type inference:** `describeOutcome`'s return type is never written, but `tsc`
infers it as `string` from the function body:

```typescript
function describeOutcome(outcome: string) {
  return outcome === "success" ? "logged in successfully" : "failed to log in";
}
```

Proof it's genuinely inferred as `string`, not `any`: assigning its result to a
`number` is a real compile error -

```
error TS2322: Type 'string' is not assignable to type 'number'.
```

**Generic type argument inference:** `first<T>` never needs `<string>` written
explicitly - `tsc` infers `T` from the ARGUMENT:

```typescript
const inferred = first(["alice", "bob"]); // T inferred as string
const explicit = first<string>(["alice", "bob"]); // same result, spelled out
```

**Where inference runs out:** an empty array gives `tsc` no element to look at, so `T`
silently falls back to `unknown` - not a compile error, just a much less useful type:

```typescript
const empty = first<string>([]); // explicit <string> fixes it
```

This is the one place in this module worth flagging as a real judgment call: `tsc`
won't stop you from writing `first([])` without the explicit type argument, but doing
so throws away the exact type safety this whole module has been building toward.

## A Running Comparison

| TypeScript | Java |
|---|---|
| `interface A extends B { ... }` | `interface A extends B { ... }` |
| `readonly id: number` | `final int id` |
| `notes?: string` | `Optional<String> notes` (a wrapper type, not a field modifier) |
| `interface Verifier { verify(u: string): boolean }` | `interface Verifier { boolean verify(String u); }` |
| `function first<T>(items: T[]): T` | `<T> T first(List<T> items)` |
| `interface Result<T> { value?: T }` | Closest: a custom generic `Result<T>` class - Java has no built-in one |
| `<T extends { username: string }>` | `<T extends Named>` (bounded by an interface) |
| Return type inference | Java requires an explicit return type always - no equivalent |

## Transition to the Lab

Learners extend an interface with a `readonly` field and an optional field, write a
constrained generic function, and use a generic `Result<T>` interface to wrap the
outcome of a check - verified by running `tsc --strict --noEmit` cleanly and confirming
output against a model answer.
