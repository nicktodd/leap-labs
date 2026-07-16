# Fidelity LEAP Program — Sprint 8 Lab Exercises

This repository contains the hands-on lab exercises accompanying **Sprint 8: Node.js / NestJS
Authentication Service**, week 8 of the Fidelity LEAP graduate programme.

## Prerequisites

- Node.js (LTS) and npm
- No prior JavaScript or TypeScript experience assumed — Days 1–2 build this from zero
- Postgres (the Sprint 3 enterprise schema, extended with a `users` table — see `shared/`)
- Java 21 (JDK) and Maven, and Docker — to run Sprint 6/7's mission service, which the new auth
  service integrates with from Module 15 onward
- GitHub Copilot Chat (continuing as a learning aid)

## Coming from Sprint 7

Sprint 6 built a Spring Boot mission service that trusts JWTs from `shared/auth-stub` — a
minimal, hardcoded-credentials Node service, good enough to build and test `SecurityConfig`
against, never intended to be real. Sprint 8 builds the real thing: a NestJS auth service with
genuine user registration, password hashing, and database-backed login, issuing tokens the
mission service already knows how to validate without any changes on its side. See
`shared/mission-brief.md`.

## Structure

Each module has its own folder under `demos/`, `labs/`, and `solutions/`. From Module 8 onward,
modules are self-contained Node/npm projects; Modules 2–7 are smaller, dependency-free JavaScript/
TypeScript exercises runnable directly with `node` or `ts-node`.

- `demos/<module>/` — instructor-led demo assets and guides
- `labs/<module>/` — your starter files and the task README for that module
- `solutions/<module>/` — reference solutions (try the lab first!)

## Getting started

1. Clone this repository.
2. `cd` into a module's `labs/<module>/` folder and check that module's README for setup.
3. Work through the modules in order, starting with `labs/01-.../README.md`.

## Modules

| # | Module | Lab |
|---|---|---|
| 1 | Identity, Access Management & Zero-Trust: Why This Service Matters | [labs/01-identity-access-management-and-zero-trust-why-this-service-matters/README.md](labs/01-identity-access-management-and-zero-trust-why-this-service-matters/README.md) |
| 2 | JavaScript Fundamentals: Syntax, Variables, Functions & Control Flow | [labs/02-javascript-fundamentals-syntax-variables-functions-and-control-flow/README.md](labs/02-javascript-fundamentals-syntax-variables-functions-and-control-flow/README.md) |
| 3 | Working with Objects, Arrays & Modern JavaScript | [labs/03-working-with-objects-arrays-and-modern-javascript/README.md](labs/03-working-with-objects-arrays-and-modern-javascript/README.md) |
| 4 | Asynchronous JavaScript: Callbacks, Promises & Async/Await | [labs/04-asynchronous-javascript-callbacks-promises-and-async-await/README.md](labs/04-asynchronous-javascript-callbacks-promises-and-async-await/README.md) |
| 5 | Introduction to TypeScript: Why Types & Basic Annotations | [labs/05-introduction-to-typescript-why-types-and-basic-annotations/README.md](labs/05-introduction-to-typescript-why-types-and-basic-annotations/README.md) |
| 6 | The TypeScript Build Process: tsconfig, Compiling & Tooling | [labs/06-the-typescript-build-process-tsconfig-compiling-and-tooling/README.md](labs/06-the-typescript-build-process-tsconfig-compiling-and-tooling/README.md) |
| 7 | TypeScript Deeper: Interfaces, Generics & Type Inference | [labs/07-typescript-deeper-interfaces-generics-and-type-inference/README.md](labs/07-typescript-deeper-interfaces-generics-and-type-inference/README.md) |
| 8 | Node.js Fundamentals: Event Loop, Modules & npm | [labs/08-nodejs-fundamentals-event-loop-modules-and-npm/README.md](labs/08-nodejs-fundamentals-event-loop-modules-and-npm/README.md) |
| 9 | NestJS Fundamentals: Modules, Controllers, Providers & DI | [labs/09-nestjs-fundamentals-modules-controllers-providers-and-di/README.md](labs/09-nestjs-fundamentals-modules-controllers-providers-and-di/README.md) |
| 10 | DTOs & Validation in NestJS | [labs/10-dtos-and-validation-in-nestjs/README.md](labs/10-dtos-and-validation-in-nestjs/README.md) |
| 11 | Building the Auth Service Skeleton: Login, Register, Refresh | [labs/11-building-the-auth-service-skeleton-login-register-refresh/README.md](labs/11-building-the-auth-service-skeleton-login-register-refresh/README.md) |
| 12 | Secure DB Access & Password Hashing | [labs/12-secure-db-access-and-password-hashing/README.md](labs/12-secure-db-access-and-password-hashing/README.md) |
| 13 | JWT Essentials: Issuing & Validating Tokens | [labs/13-jwt-essentials-issuing-and-validating-tokens/README.md](labs/13-jwt-essentials-issuing-and-validating-tokens/README.md) |
| 14 | Securing & Testing the Service — Lightweight Pass | _coming soon_ |
| 15 | Mission Build: OpenAPI Docs & Replacing the Sprint 7 Stub | _coming soon_ |

## Support

Ask your trainer or Scrum team lead during class, or raise a question in the cohort's usual
support channel.
