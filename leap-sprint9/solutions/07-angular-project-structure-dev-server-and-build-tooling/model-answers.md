# Lab 7 Model Answers

## Verified Output

The canonical `solutions/mission-ui/` project (repo root, alongside `demos/`/`labs/`/
`solutions/`) is exactly the result of running the scaffold command with nothing added yet —
confirmed by actually running it during this module's demo build:

- `npx @angular/cli@21 new mission-ui --routing --style=css --ssr=false --skip-git`
  completed with a real `npm install`, producing `angular.json`, `package.json`,
  `src/main.ts`, `src/app/app.ts`, `src/app/app.html`, `src/app/app.css`,
  `src/app/app.config.ts`, `src/app/app.routes.ts`.
- `npx ng serve --port 4300` produced "Application bundle generation complete" and served a
  real page at `http://localhost:4300/` — screenshotted in
  `demos/07-.../screenshots/ng-serve-default-page.png`, showing "Hello, mission-ui".
- `npx ng build` produced a real `dist/mission-ui/` with `main-*.js` and `styles-*.css`,
  214.72 kB raw / 58.92 kB estimated transfer for the default, empty app.

## Key Points

- **Where the rest of the markup lives**: `src/index.html` contains only a `<body>` with a
  single custom element, `<app-root></app-root>` (matching `app.ts`'s `selector: 'app-root'`)
  — Angular's `bootstrapApplication()` call in `main.ts` finds that tag and renders the whole
  component tree *inside* it. Every other component's markup lives in that component's own
  `.html` file (or inline `template` string), nested inside `<app-root>` at runtime — never
  written directly into `index.html` by hand. This is the single biggest structural
  difference from Module 1-4's one-HTML-file page: Angular has exactly one real HTML file,
  and everything else is templates the framework assembles into it.
- **The budgets question**: `ng build`'s production configuration treats
  `maximumWarning` as advisory (the build still succeeds, with a printed warning) and
  `maximumError` as a hard failure — the build exits non-zero and produces no output once
  the initial bundle exceeds it. This is a deliberate guardrail: without it, a bundle can grow
  silently, module by module, until a real user's page load noticeably slows down, with no
  single commit obviously "at fault."
- **`standalone: true` in older code**: earlier Angular versions (roughly 14-18) required
  every standalone component to declare `standalone: true` explicitly, because the *default*
  at the time was the older NgModule-based component model. Recent Angular versions flipped
  the default, so the CLI no longer writes it. A component from an older codebase with
  `standalone: true` still present behaves *identically* to one without it today — the
  property became redundant, not deprecated or wrong; removing it changes nothing at runtime.
