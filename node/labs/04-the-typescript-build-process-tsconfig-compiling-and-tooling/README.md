# Lab 4: The TypeScript Build Process - tsconfig, Compiling & Tooling

## Setup

```bash
npm install
```

## Task

This is a two-file TypeScript project (`src/verification.ts`, `src/index.ts`) with a
starter `tsconfig.json` that's missing key settings. Two TODOs:

1. **`tsconfig.json`** - add `"module": "NodeNext"`, `"moduleResolution": "NodeNext"`,
   and `"strict": true` to `compilerOptions` (matching the demo's config).
2. **`src/index.ts`**'s import - missing its required file extension under `NodeNext`
   resolution. Leave it alone until TODO 1 is done; fixing the import first would hide
   what TODO 1 actually causes `tsc` to catch.

Run this now, before changing anything:

```bash
npm run build
npm run start
```

It builds "successfully" - but crashes at RUNTIME with `ERR_MODULE_NOT_FOUND`, not a
compile error. That's the starting point, and it's deliberate: the starter
`tsconfig.json` is missing the settings that would have caught this at compile time
instead.

Do TODO 1 first, then rerun `npm run build` - now `tsc` itself refuses to compile, with
a real `TS2835` error naming the exact fix. Do TODO 2 using that suggested fix, then
rerun both commands.

## Expected Output (once both TODOs are done)

```
dave is verified
```

## A Question Worth Sitting With

Before TODO 1, the broken import was NOT a compile error - `tsc` reported success, and
the project only broke once `node dist/index.js` actually ran. After TODO 1, the exact
same broken import IS a compile error, caught before anything runs. What changed
between those two runs was only `tsconfig.json` - the source code was identical both
times. What does that tell you about how much a `tsconfig.json` is actually doing in a
real project, beyond just "settings"?
