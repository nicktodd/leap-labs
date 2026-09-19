# Module 6 Demo Guide — Angular Fundamentals: Framework Overview & What Makes It Different from React

**Duration:** 25 minutes
**Prerequisite:** Day 1 (Modules 1-4) — HTML, CSS, the DOM, events, and `fetch()`, all by
hand. No Angular project exists yet; that's Module 7. Today is entirely conceptual — reading
code, not writing or running it.

Day 1 asked "what does a browser actually do." Today asks a different question: "what does a
*framework* add on top of that, and specifically, what does Angular add that's different from
other frameworks candidates may already have seen?"

## Part 0: What a Framework Actually Buys You (4 min)

Modules 1-4 wired up one page by hand: select an element, add a listener, update the DOM,
`fetch()` a response, update the DOM again. That worked — but imagine doing it for a real
trading app with a dozen screens, shared state (the logged-in trader, their portfolio), and
dozens of forms. Three problems show up fast, none of them solved by more `fetch()` calls:

- **Structure** — where does each screen's code live, and how do screens share code?
- **State** — when the token or the portfolio changes, every screen that shows it has to
  update, without manually calling `document.querySelector` again everywhere it's used.
- **Consistency** — a dozen developers writing a dozen forms need one agreed-upon way to
  do it, or the codebase becomes a dozen different styles.

A framework's whole job is answering those three questions with an actual opinion, so a team
doesn't reinvent the answer per feature. Angular answers all three; so does React; so does
every other framework a candidate may know. Today is about how Angular's *specific* answers
differ.

## Part 1: Angular's Philosophy — Batteries Included (5 min)

Angular is deliberately **opinionated and complete**: routing, HTTP, forms, dependency
injection, testing utilities, and a CLI ship as part of Angular itself, not as separately
chosen third-party packages. Four ideas underpin nearly everything Angular does:

- **Components** — a unit of UI that owns its own template, styling, and logic. Not new
  today — Module 3's `elements-demo.html` composed similar logic by hand, just without a
  name for the pattern or a place to put it.
- **TypeScript-first** — Angular is written in and for TypeScript, not JavaScript with types
  bolted on. Everything from Sprint 8 (interfaces, generics, classes) applies directly.
- **Dependency injection** — a service class is requested, not manually constructed
  (`inject()` or a constructor parameter) — the framework decides what instance to hand
  back. Module 9 covers this properly; today just names it.
- **Signals** — Angular's newer, fine-grained reactivity model (2023+): a `signal()` holds a
  value, and anything reading it automatically re-runs when it changes. No manual
  `document.querySelector` + update, the way Module 3 required by hand.

## Part 2: What's Different From React (7 min)

Both are legitimate, widely-used choices — this isn't "Angular is better," it's "here's what
transfers and what doesn't" for anyone who's used React before.

| | Angular | React |
|---|---|---|
| **UI syntax** | HTML-based templates, with Angular-specific syntax (`{{ }}`, `@if`) added on top | JSX — JavaScript with HTML-like syntax mixed directly in |
| **Language** | TypeScript required | JavaScript by default, TypeScript optional |
| **Included vs chosen** | Routing, HTTP, forms, DI ship built-in | Routing, HTTP, state management are separate libraries you pick |
| **Reactivity model** | Signals — a value that tracks its own readers | Hooks (`useState`, `useEffect`) — re-runs a whole function component |
| **Structure** | CLI generates and enforces a project shape | No single enforced shape — conventions vary by team |
| **Change detection** | Fine-grained — only what reads a changed signal re-renders | Re-renders the whole component function, then diffs a virtual DOM |

The practical upshot for this sprint: everything Module 1-4 wrote by hand — templates,
event handling, reactive updates — Angular now does *for* the app, just with its own syntax
and its own opinions about where the pieces go.

## Part 3: Reading Real Angular Code — Annotate What's New (9 min)

Open `mission-status.component.ts` — deliberately small, using patterns Modules 7-8 will
build for real. Don't run it (there's no project yet); read it line by line and sort each
piece into one of two buckets:

```typescript
import { Component, signal, computed, input } from '@angular/core';

@Component({
  selector: 'app-mission-status',
  standalone: true,
  template: `
    <div class="status-card">
      <h2>{{ missionName() }}</h2>
      <p>Holdings: {{ holdingCount() }}</p>
      @if (holdingCount() > 0) {
        <button (click)="refresh()">Refresh</button>
      } @else {
        <p>No holdings yet.</p>
      }
    </div>
  `,
})
export class MissionStatusComponent {
  missionName = input.required<string>();
  private holdings = signal<number>(0);
  holdingCount = computed(() => this.holdings());

  refresh(): void {
    this.holdings.set(this.holdings() + 1);
  }
}
```

**Already known, from Sprint 8 or Day 1:**
- `import { ... } from '...'` — ES module syntax
- `class MissionStatusComponent { ... }` — an ordinary TypeScript class
- `private holdings = ...` and `refresh(): void { ... }` — class fields and typed methods
- The *decorator* syntax itself, `@Something(...)` above a class — Sprint 8's NestJS used
  `@Controller`, `@Injectable` the exact same way
- `{{ missionName() }}` reading a value and `(click)="refresh()"` running a method on a
  click — conceptually the same read-a-value/handle-an-event ideas Module 3 built by hand,
  just with different syntax

**New today, Angular-specific:**
- `@Component({ selector, standalone, template })` — *this specific* decorator and its
  config shape are Angular's component model, not a general TypeScript idea
- `signal()`, `computed()`, `input.required()` — Angular's reactivity primitives; calling a
  signal like a function (`holdingCount()`) reads its current value
- `{{ }}` interpolation and `(click)="..."` binding syntax inside the template string —
  Angular's own template language, not HTML and not JavaScript
- `@if (...) { ... } @else { ... }` inside the template — Angular's control-flow syntax
  (this replaced an older `*ngIf` syntax; @if is what current Angular uses)
- `this.holdings.set(...)` — signals are updated by calling `.set()`, not by reassignment

## Key message

Nothing in Angular replaces what Days 1 taught — TypeScript, events, the DOM, `fetch()` are
all still exactly what's happening underneath. Angular adds a *specific, opinionated* set of
patterns (components, signals, DI, templates) on top of that foundation, and today's whole
point was learning to tell the two apart on sight, before Module 7 scaffolds a real project
and Module 8 builds a real component.

## Transition to the Lab

Learners get a second, different short Angular snippet and annotate it the same way — sorting
each line into "already knew this from Sprint 8/Day 1" or "new, Angular-specific" — reinforcing
the read *before* Module 7 asks them to write any Angular of their own.
