# Lab 7 — Angular Project Structure, Dev Server & Build Tooling

## Setup

Node.js 22.22.3+ or 24.15.0+ and npm (check with `node --version`). The Angular CLI itself
doesn't need a separate global install — `npx @angular/cli@21` downloads and runs it on
demand, pinned to Angular 21 (this sprint's required version, paired with TypeScript 5.9) so
`npx @angular/cli` alone doesn't silently grab whatever's newest,
exactly as today's demo did.

## Task

Scaffold `mission-ui` yourself, in your own workspace — **not** inside this labs repo clone.
This is the actual Angular application the rest of Sprint 9 builds, module by module, so pick
a location you'll keep coming back to for the next ten modules.

1. Run the exact command from today's demo:

   ```bash
   npx @angular/cli@21 new mission-ui --routing --style=css --ssr=false --skip-git
   ```

2. Once it finishes (a real `npm install` runs as part of scaffolding — this takes a minute),
   `cd mission-ui` and start the dev server:

   ```bash
   npx ng serve
   ```

3. Open `http://localhost:4200/` in a browser.

## Verify

1. The default Angular page loads — "Hello, `mission-ui`", matching today's demo screenshot.
2. With the dev server still running, open `src/app/app.html` and change any visible text.
   Save the file, and check the browser updates **without you refreshing it** — that's the
   dev server's watch mode, not a coincidence.
3. Stop the dev server (Ctrl+C) and run a production build:

   ```bash
   npx ng build
   ```

   Confirm a `dist/mission-ui/` folder appears, containing at least one `.js` and one `.html`
   file — real, static, deployable output, no dev server required to view it (though you'd
   need to serve those static files from somewhere to load them in a browser).
4. Open `angular.json` and find the `budgets` section under `architect.build.configurations
   .production`. Note (don't change) the `maximumWarning`/`maximumError` sizes — what do you
   think happens to `ng build` if the app's bundle grows past `maximumError`?

## A Question Worth Sitting With

`src/index.html` is the *only* real HTML file in the entire project — compare it to how many
`.html` files Module 1-4's page needed (one, total, the whole time). Given that Angular apps
often have dozens of components, each with a full UI, where does the rest of the markup
actually live, and what does `index.html` itself contain that suggests Angular is going to
inject content into it rather than replace it outright?

A second question: today's demo pointed out that `app.ts` no longer writes `standalone: true`
explicitly, even though Module 6's own example did. Why would a real Angular codebase written
before this CLI version still have `standalone: true` scattered through it, and would removing
it change how those components actually behave?
