# Lab 6 Model Answers

There's no code to run — `holdings-list.component.ts` compiles as valid Angular
(verified with `tsc` against the real `@angular/core`/`@angular/router` types), but this
lab is a reading exercise. Below is the line-by-line sort.

## Already Known (Sprint 8 / Day 1)

- `import { ... } from '@angular/core'` / `'@angular/router'` — ES module syntax, unchanged
  from every Node.js and browser import so far.
- `interface Holding { ticker: string; quantity: number; }` — an ordinary TypeScript
  interface, exactly as Sprint 8 used them for DTOs.
- `export class HoldingsListComponent { ... }` — an ordinary exported class.
- `private router = ...` — a typed class field, same as any NestJS service field in Sprint 8.
- `constructor() { ... }` — an ordinary constructor.
- `goToOrders(): void { ... }` — a typed method.
- The *decorator syntax itself* — `@Component({...})` sitting above a class is the same
  TypeScript decorator feature Sprint 8's NestJS controllers used (`@Controller`,
  `@Injectable`). What's Angular-specific is which decorator (`@Component`) and its config
  shape, not decorators as a language feature.
- `{{ holding.ticker }}` reading a value onto the screen and `(click)="goToOrders()"`
  handling a click — conceptually the same "read a value" / "handle an event" ideas Module 3
  built with `textContent` and `addEventListener`, just spelled differently.

## New, Angular-Specific

- `@Component({ selector, standalone, template })`'s three properties: `selector` names the
  custom HTML tag this component becomes (`<app-holdings-list>`); `standalone: true` means
  it declares its own dependencies rather than belonging to an NgModule; `template` is the
  component's own HTML, written as a TypeScript template string.
- `inject(Router)` — Angular's dependency injection asking the framework for the *shared*
  `Router` instance the whole app uses, rather than `new Router()` constructing a private
  one that wouldn't know about the rest of the app's navigation state. This is the same idea
  Module 9 formalises properly.
- `effect(() => { ... })` — runs once immediately, then again automatically every time a
  signal it reads (`this.holdings()`) changes — the reactivity model itself, not a one-off
  method call.
- `@for (holding of holdings(); track holding.ticker) { ... }` — Angular's template
  control-flow syntax for rendering a list. It needs `track` (unlike a plain JS `for...of`)
  because Angular has to know *which* DOM element corresponds to which list item across
  re-renders, so it can update just the changed rows instead of rebuilding the whole list —
  `track holding.ticker` tells it a ticker uniquely identifies a row.
- `signal<Holding[]>([])` and calling it as `holdings()` — Angular's signal API; the interface
  `Holding` is ordinary TypeScript, but wrapping it in `signal()` and reading it via `()` is
  new today.
- `this.router.navigate(['/orders'])` — Angular Router's own API for a client-side
  navigation (no full page reload, similar in spirit to Module 4's `preventDefault()` but
  handled by the framework).

## Resolving the Two Disagreements

1. **Decorator syntax vs Angular-specific**: the syntax (`@Name(...)` above a class) is a
   general TypeScript feature — Sprint 8's NestJS used it identically for `@Controller` and
   `@Injectable`. What's new is *this specific decorator*, `@Component`, and the shape of
   object it expects.
2. **`holdings()` reads, it doesn't reassign**: calling a signal like a function always
   *reads* its current value. The only line that changes what `holdings` holds would be a
   call to `.set()` or `.update()` — this file never actually updates `holdings`, which is
   itself worth noticing: `effect()` would fire again the moment something did.
