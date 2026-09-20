# Lab 3: Node.js Fundamentals - Event Loop, Modules & npm

## Task

1. **TODO 1** (`count-utils.cjs`) - implement `countByOutcome(attempts)`, returning
   `{ successCount, failCount }`, using `module.exports` (CommonJS style, no `export`
   keyword).
2. **TODO 2** (`report.cjs`) - PREDICT the print order of the commented-out
   sync/`nextTick`/`Promise.then`/`setTimeout` block first (on paper, or out loud),
   THEN uncomment it and run it for real to check your prediction.

Run this now, before changing anything:

```bash
node report.cjs
```

It throws at TODO 1. That's the starting point.

## Expected Output (once TODO 1 is done)

```
2 successful, 2 failed
```

## Expected Output (once TODO 2 is uncommented)

```
sync A
sync B
nextTick
promise.then
setTimeout
```

If your prediction didn't match, that's the point of predicting first - it's a cheap
way to find out which parts of Module 3's demo actually stuck.

## A Question Worth Sitting With

`count-utils.cjs` uses `module.exports = { countByOutcome };` and `report.cjs` uses
`require("./count-utils.cjs")`. If this lab were rebuilt as `.mjs` files with
`export`/`import` instead, what would actually need to change beyond the file
extensions and those two lines? (Hint: re-read Module 4's `NodeNext` resolution rule.)
