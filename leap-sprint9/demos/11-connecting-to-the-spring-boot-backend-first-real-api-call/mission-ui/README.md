# MissionUi

> **Sprint 9 note**: this is the canonical reference project the `solutions/` folders for
> Modules 7-17 build up incrementally, module by module — Module 7's solution is exactly
> `ng new mission-ui --routing --style=css --ssr=false` with nothing added yet. `node_modules/`
> and `dist/` are gitignored; run `npm install` before `ng serve`/`ng build`. Learners scaffold
> their own copy per `labs/07-.../README.md` and keep building in it for the rest of the sprint
> — this folder is the instructor-facing answer key, not something learners clone directly.
>
> Pinned to **Angular 21** and **TypeScript 5.9** (not the latest Angular 22/TS 6.0) —
> deliberately, to match this cohort's required toolchain.

This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 21.2.19.

## Development server

To start a local development server, run:

```bash
ng serve
```

Once the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.

## Code scaffolding

Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

```bash
ng generate --help
```

## Building

To build the project run:

```bash
ng build
```

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

## Running unit tests

To execute unit tests with the [Vitest](https://vitest.dev/) test runner, use the following command:

```bash
ng test
```

## Running end-to-end tests

For end-to-end (e2e) testing, run:

```bash
ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

## Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.
