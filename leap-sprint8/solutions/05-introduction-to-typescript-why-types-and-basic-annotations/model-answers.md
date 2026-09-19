# Lab 5 Model Answers

## Verified Output

```
logged in successfully
{ username: 'dave', outcome: 'success' }
dave logged in successfully
```

`npx tsc report.ts --strict --noEmit` reports zero errors once all three TODOs are
done.

## Key Points

- **TODO 1** and **TODO 3** are the same fix applied twice: a `: string` (or
  `: Attempt`) after each parameter name, and a `: string` after the closing `)` for
  the return type. Both errors (`TS7006`) appear together the first time `tsc` runs,
  since `--strict` checks the whole file in one pass, not one TODO at a time.
- **TODO 2**: the `interface` only needs to be DEFINED once — `username: string;` and
  `outcome: string;` on their own lines, no `=` and no trailing commas needed (`;` or a
  newline separates members). The `attempt` constant then just gets `: Attempt` added
  after its name.

## The Reflection Question

```
report.ts(15,46): error TS2561: Object literal may only specify known properties,
but 'outcom' does not exist in type 'Attempt'. Did you mean to write 'outcome'?
```

In Module 3's plain JavaScript, this exact typo compiles fine, runs fine, and fails
silently: `attempt.outcome` is `undefined` wherever it's read, and nothing points at
the actual mistake — the bug surfaces later, wherever `undefined` causes a visible
problem, if it ever does. Here, `tsc` refuses to compile at all, names the exact line
and column, and even suggests the fix. This is the entire pitch of this module in one
concrete example: the same class of mistake, caught before the code runs instead of
discovered after it's already caused a problem.
