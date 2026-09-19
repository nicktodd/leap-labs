# Lab 5: Introduction to TypeScript — Why Types & Basic Annotations

## Setup

```bash
npm install
```

(installs TypeScript locally into this folder, same as the demo)

## Task

`report.ts` is an untyped file with three TODOs:

1. **`describeOutcome`** — add a type annotation to the `outcome` parameter (`string`)
   and the function's return type (`string`).
2. **`Attempt` interface** — define an `interface Attempt` with two `string`
   properties, `username` and `outcome`, then annotate the `attempt` constant with it.
3. **`describeAttempt`** — add a type annotation to the `attempt` parameter
   (`Attempt`) and the function's return type (`string`).

Run this now, before changing anything:

```bash
npx tsc report.ts --strict --noEmit
```

It fails with real compiler errors (`TS7006`, `"implicitly has an 'any' type"`) at
TODO 1 and TODO 3. That's the starting point — work through the TODOs in order,
rerunning after each one, until `tsc` reports zero errors.

Once it compiles cleanly, run it for real:

```bash
npx tsc report.ts --strict
node report.js
```

## Expected Output

```
logged in successfully
{ username: 'dave', outcome: 'success' }
dave logged in successfully
```

## A Question Worth Sitting With

Once all three TODOs are done and `tsc --strict` reports zero errors, deliberately
break the `attempt` object — change `outcome: "success"` to `outcom: "success"` (the
exact typo from Module 3's "Objects vs Java Records" comparison) and rerun
`npx tsc report.ts --strict --noEmit`. What does `tsc` say, and how is that different
from what would have happened if this were still Module 3's plain JavaScript?
