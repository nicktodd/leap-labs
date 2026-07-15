# Lab 6 Model Answers

## Verified Output

```
> tsc

> node dist/index.js

dave is verified
```

## Key Points

- **Before TODO 1**: the starter `tsconfig.json` has no `module`/`moduleResolution`
  setting, so `tsc` doesn't apply Node's ESM extension rule and happily compiles the
  extensionless import. `npm run build` reports success. The failure only shows up when
  `node dist/index.js` actually runs and Node's real module loader can't find a file
  called `verification` (no extension) — a REAL, verified `ERR_MODULE_NOT_FOUND`.
- **TODO 1**: adding `"module": "NodeNext"`, `"moduleResolution": "NodeNext"`, and
  `"strict": true` doesn't change the source code at all — it changes what `tsc` is
  willing to let through. The exact same broken import now fails to COMPILE, with a
  `TS2835` naming the exact fix.
- **TODO 2**: `./verification` becomes `./verification.js` — matching the COMPILED
  filename, not the `.ts` source filename, exactly as Module 6's demo covered.

## The Reflection Question

The `tsconfig.json` isn't just configuration — it's the difference between a bug being
caught by a teammate's `tsc` run in five seconds and a bug reaching production and
crashing at runtime, on a real request, in front of a real user. The two runs used
identical source code; only the compiler's own strictness changed. This is the entire
argument for `--strict` and `NodeNext` resolution as defaults, not optional extras: a
lenient `tsconfig.json` doesn't prevent bugs, it just moves them later, into runtime,
where they're far more expensive to find.
