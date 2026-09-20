# Lab 3 Model Answers

## Verified Output

```
2 successful, 2 failed
sync A
sync B
nextTick
promise.then
setTimeout
```

## Key Points

- **TODO 1**: a plain `for...of` loop with an `if`/`else`, identical in shape to
  Module 2's original summary logic - CommonJS changes how the function is EXPORTED
  (`module.exports = { countByOutcome };` at the bottom), not how the function itself
  is written.
- **TODO 2**: the correct order is sync code first (`sync A`, `sync B`), then
  `process.nextTick` (Node's own microtask queue, drained first), then `Promise.then`
  (the standard microtask queue), then `setTimeout` (a macrotask) - matching Module 3's
  demo exactly, since this file is `.cjs`, not `.mjs`.

## The Reflection Question

Rebuilding this lab as `.mjs` would need more than swapping `module.exports`/`require`
for `export`/`import`:

- `require("./count-utils.cjs")` has no extension requirement; Module 4's `NodeNext`
  ESM resolution rule would require `import { countByOutcome } from "./count-utils.js"`
  - note also that the FILENAME would need to change from `.cjs` to `.mjs` for the
  import to even make sense, since the extension in the import path names the compiled/
  actual file.
- `require()` is synchronous, callable anywhere including conditionally inside an
  `if`; `import` is hoisted and static - it can't be called conditionally or with a
  computed path (without switching to dynamic `import()`, an entirely different thing).
- CommonJS's `module.exports` is a single object assigned once; ESM's multiple named
  `export`s are individual bindings - functionally similar here, but not the same
  mechanism underneath.

This is genuinely more than a syntax swap - it's why Module 4 spent an entire module
on `NodeNext` resolution rules that only matter for ESM, not CommonJS.
