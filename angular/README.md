# LEAP Program - This Week's Lab Exercises

This repository contains the hands-on lab exercises accompanying **This Week: UI Development
with Angular**, week 9 of the LEAP graduate programme.

## Prerequisites

- Node.js 22.22.3+ or 24.15.0+ (the Angular CLI will refuse to run on older Node 22.x patch
  versions) and npm
- Angular CLI, pinned to **Angular 21** (`npm install -g @angular/cli@21`, or use
  `npx @angular/cli@21`) - paired with **TypeScript 5.9**, not the newest Angular/TS release
- No prior HTML, CSS, JavaScript, or TypeScript experience assumed - Modules 1-6 build
  HTML/CSS/JavaScript from zero, and Modules 7-8 cover TypeScript in full - basic types
  through interfaces, generics, and type inference - before Angular itself is introduced in
  Module 10
- A working checkout of the Spring week's mission service (Spring Boot) - Modules 6, 9, 15,
  and 16 make real calls against it and against this week's own `shared/auth-stub`
- Docker, and the same `missionservice-postgres` container used since the Spring week
- GitHub Copilot Chat (continuing as a learning aid)

## Coming from the Spring week

By the end of the Spring week the mission had a complete backend: Postgres (from the Data
Systems week) behind a Spring Boot service (from the Java and Spring weeks), secured with
JWTs, proven to work end to end with `curl`. This week builds the piece that turns that into
something a person can actually use: an Angular front end, logging in against a small auth
stub built specifically for this week (the Node week, later in the programme, replaces it
with a full identity service). See `shared/mission-brief.md`.

Nobody has touched HTML, CSS, the browser, JavaScript, or TypeScript yet at this point in the
programme. Modules 1-6 build HTML/CSS/browser-JS from zero (including full JavaScript
fundamentals, not just a browser-DOM primer), and Modules 7-8 cover TypeScript in full -
basic types and annotations, then interfaces, generics, and type inference - before Angular
itself is introduced in Module 10.

## Structure

Each module has its own folder under `demos/`, `labs/`, and `solutions/`, following the same
pattern as every previous sprint.

- `demos/<module>/` - instructor-led demo assets and guides
- `labs/<module>/` - your starter files and the task README for that module
- `solutions/<module>/` - reference solutions (try the lab first!)
- `solutions/mission-ui/` - from Module 11 onward, the one canonical Angular project that
  `solutions/11-.../` through `solutions/21-.../` build up incrementally, module by module.
  Your own `mission-ui` (scaffolded per Module 11) is where you keep building - this is the
  instructor-facing answer key, not something you clone directly.

## Getting started

1. Clone this repository.
2. `cd` into a module's `labs/<module>/` folder and check that module's README for setup.
3. Work through the modules in order, starting with `labs/01-.../README.md`.

## Modules

| # | Module | Lab |
|---|---|---|
| 1 | HTML Fundamentals: Structure, Semantic Elements & Forms | [labs/01-html-fundamentals-structure-semantic-elements-and-forms/README.md](labs/01-html-fundamentals-structure-semantic-elements-and-forms/README.md) |
| 2 | CSS Fundamentals: Selectors, the Box Model & Layout | [labs/02-css-fundamentals-selectors-the-box-model-and-layout/README.md](labs/02-css-fundamentals-selectors-the-box-model-and-layout/README.md) |
| 3 | JavaScript Fundamentals: Syntax, Variables, Functions & Control Flow | [labs/03-javascript-fundamentals-syntax-variables-functions-and-control-flow/README.md](labs/03-javascript-fundamentals-syntax-variables-functions-and-control-flow/README.md) |
| 4 | Working with Objects, Arrays & Modern JavaScript | [labs/04-working-with-objects-arrays-and-modern-javascript/README.md](labs/04-working-with-objects-arrays-and-modern-javascript/README.md) |
| 5 | JavaScript in the Browser: The DOM, Events & the Window Object | [labs/05-javascript-in-the-browser-the-dom-events-and-the-window-object/README.md](labs/05-javascript-in-the-browser-the-dom-events-and-the-window-object/README.md) |
| 6 | Fetch & Browser HTTP: Calling a Real API Without a Framework | [labs/06-fetch-and-browser-http-calling-a-real-api-without-a-framework/README.md](labs/06-fetch-and-browser-http-calling-a-real-api-without-a-framework/README.md) |
| 7 | Introduction to TypeScript: Why Types & Basic Annotations | [labs/07-introduction-to-typescript-why-types-and-basic-annotations/README.md](labs/07-introduction-to-typescript-why-types-and-basic-annotations/README.md) |
| 8 | TypeScript Deeper: Interfaces, Generics & Type Inference | [labs/08-typescript-deeper-interfaces-generics-and-type-inference/README.md](labs/08-typescript-deeper-interfaces-generics-and-type-inference/README.md) |
| 9 | The Full Stack So Far & Where Angular Fits | [labs/09-the-full-stack-so-far-and-where-angular-fits/README.md](labs/09-the-full-stack-so-far-and-where-angular-fits/README.md) |
| 10 | Angular Fundamentals: Framework Overview & What Makes It Different from React | [labs/10-angular-fundamentals-framework-overview-and-what-makes-it-different-from-react/README.md](labs/10-angular-fundamentals-framework-overview-and-what-makes-it-different-from-react/README.md) |
| 11 | Angular Project Structure, Dev Server & Build Tooling | [labs/11-angular-project-structure-dev-server-and-build-tooling/README.md](labs/11-angular-project-structure-dev-server-and-build-tooling/README.md) |
| 12 | Components & Templates: Standalone Components & Signals | [labs/12-components-and-templates-standalone-components-and-signals/README.md](labs/12-components-and-templates-standalone-components-and-signals/README.md) |
| 13 | Services & Dependency Injection in Angular | [labs/13-services-and-dependency-injection-in-angular/README.md](labs/13-services-and-dependency-injection-in-angular/README.md) |
| 14 | HTTP Communication: HttpClient, Observables & Error Handling | [labs/14-http-communication-httpclient-observables-and-error-handling/README.md](labs/14-http-communication-httpclient-observables-and-error-handling/README.md) |
| 15 | Connecting to the Spring Boot Backend: First Real API Call | [labs/15-connecting-to-the-spring-boot-backend-first-real-api-call/README.md](labs/15-connecting-to-the-spring-boot-backend-first-real-api-call/README.md) |
| 16 | OpenAPI-Generated API Clients | [labs/16-openapi-generated-api-clients/README.md](labs/16-openapi-generated-api-clients/README.md) |
| 17 | Reactive Forms: Building, Submitting & Handling Responses | [labs/17-reactive-forms-building-submitting-and-handling-responses/README.md](labs/17-reactive-forms-building-submitting-and-handling-responses/README.md) |
| 18 | Routing Fundamentals: Routes, Lazy Loading & Navigation | [labs/18-routing-fundamentals-routes-lazy-loading-and-navigation/README.md](labs/18-routing-fundamentals-routes-lazy-loading-and-navigation/README.md) |
| 19 | Building Authenticated Flows: Login, JWT Interceptors & Route Guards | [labs/19-building-authenticated-flows-login-jwt-interceptors-and-route-guards/README.md](labs/19-building-authenticated-flows-login-jwt-interceptors-and-route-guards/README.md) |
| 20 | Testing Angular: Unit Tests & End-to-End Tests with Playwright | [labs/20-testing-angular-unit-tests-and-end-to-end-tests-with-playwright/README.md](labs/20-testing-angular-unit-tests-and-end-to-end-tests-with-playwright/README.md) |
| 21 | Mission Build: Wiring Up Remaining Features, UX Review & Wrap-up | [labs/21-mission-build-wiring-up-remaining-features-ux-review-and-wrap-up/README.md](labs/21-mission-build-wiring-up-remaining-features-ux-review-and-wrap-up/README.md) |

## Support

Ask your trainer or Scrum team lead during class, or raise a question in the cohort's usual
support channel.
