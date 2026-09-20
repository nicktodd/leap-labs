# Lab 8: TypeScript Deeper - Interfaces, Generics & Type Inference

## Setup

```bash
npm install
```

## Task

`report.ts` has three TODOs:

1. **`BaseRecord` / `LoginAttempt`** - `BaseRecord` needs a `readonly id: number` and a
   `createdAt: string`. `LoginAttempt` needs to `extend BaseRecord`, adding
   `username: string`, `outcome: string`, and an OPTIONAL `notes?: string`.
2. **`Result<T>`** - a generic interface with `success: boolean`, an optional
   `value?: T`, and an optional `error?: string` - same shape as the demo's `Result<T>`.
3. **`describeByUsername`** - a generic function, constrained so `T` must have at least
   a `username: string` field, returning `` `Record for ${record.username}` ``.

Run this now, before changing anything:

```bash
npx tsc report.ts --strict --noEmit
```

It fails with real compiler errors at TODO 2 (`TS2315`, `Result` isn't generic yet) and
TODO 3 (`TS7006`, implicit `any`). **TODO 1 does NOT cause an error yet**, even though
it's incomplete - an empty interface (`interface BaseRecord {}`) accepts any object at
all, so it provides zero type safety without ever erroring. Notice that before fixing
it - it's a real, useful observation about what an interface actually does (and
doesn't do) when it's empty.

Once all three TODOs are done and `tsc --strict --noEmit` reports zero errors, run it:

```bash
npx tsc report.ts --strict
node report.js
```

## Expected Output

```
{
  id: 1,
  createdAt: '2026-01-01T09:00:00Z',
  username: 'dave',
  outcome: 'success'
}
Verified: dave
Error: Unknown user: mallory
Record for dave
Record for erin
```

## A Question Worth Sitting With

`describeByUsername` works on the `LoginAttempt`-shaped object AND a completely
different `{ username, verified }` shape, without either one being declared as
implementing any interface. What is TypeScript actually checking when it accepts both
of those calls - and how is that different from what Java's generics would require of
the two argument types?
