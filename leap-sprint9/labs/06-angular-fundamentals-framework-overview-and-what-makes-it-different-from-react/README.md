# Lab 6 — Angular Fundamentals: Framework Overview & What Makes It Different from React

## Format

A 20-minute reading exercise, in pairs. No project to run, no npm install — that's Module 7.
Today's file, `holdings-list.component.ts`, is real, syntactically valid Angular code
(standalone component, signals, `@for`, dependency injection) that you read and annotate, the
same way today's demo walked through `mission-status.component.ts`.

## Task

Go through `holdings-list.component.ts` line by line. For every line (or meaningful chunk —
the template counts as one block per binding), decide which bucket it belongs in:

1. **Already known** — something Sprint 8 (TypeScript, classes, decorators, interfaces) or
   Day 1 (events, reading/updating something on screen) already covered, just with
   Angular's specific syntax around it.
2. **New, Angular-specific** — a concept or piece of syntax that didn't exist before today:
   Angular's own decorator config, its reactivity primitives, its template control-flow, or
   its dependency injection.

Write your answers as a simple two-column list (a shared doc, a whiteboard, or annotations
directly in a copy of the file) — there's no code to run or modify.

Specifically identify and explain, in your own words:

- What `@Component({...})`'s three config properties (`selector`, `standalone`, `template`)
  each control
- What `inject(Router)` is doing, and how it's different from writing
  `new Router()` yourself
- What `effect(() => { ... })` does, and when you'd guess it runs, based on what's inside it
- What `@for (holding of holdings(); track holding.ticker)` is doing, and why you think it
  needs `track` at all (compare it to a plain JavaScript `for...of` loop, which doesn't)
- Whether `holdings` (a signal) or `Holding` (the interface) is the Angular-specific concept,
  and which one is just an ordinary TypeScript type Sprint 8 already covered

## Verify

Compare notes with another pair. Two disagreements worth specifically resolving, out loud,
before moving on:

1. Is the *decorator syntax itself* (`@Something(...)` above a class) Angular-specific, or is
   it a general TypeScript feature Angular happens to use? (Hint: where else has this shown
   up this programme?)
2. Is `holdings()` — calling a signal like a function — reading its value, or reassigning it?
   What line in the file actually changes what `holdings` holds?

Full answers, with reasoning: `solutions/06-.../model-answers.md` — check it after your own
pass, not before.
