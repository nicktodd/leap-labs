# LEAP Program — Sprint 5 Lab Exercises

This repository contains the hands-on lab exercises accompanying **Sprint 5: Software
Engineering Essentials, Java & OOAD**, week 5 of the LEAP graduate programme.

## Prerequisites

- Java 21 (JDK) and Maven
- An IDE with UML support helpful but not required (diagrams are drafted by hand/whiteboard
  first, then captured — see Module 4 onward)
- GitHub Copilot Chat (continuing as a learning aid — Module 9 specifically has you critically
  assess a GenAI-suggested refactor rather than accept it outright)

## Coming from Sprint 4

This sprint moves from Python back to Java (last used in Sprint 1/2). Module 1 is explicitly
framed as a Python-to-Java translation guide, not a from-scratch introduction — if a Java concept
feels unfamiliar, look for its Python equivalent first, most core ideas (types, collections,
exceptions, control flow) transfer directly, only the syntax and the compiler's strictness change.

## Structure

Each module has its own folder under `demos/`, `labs/`, and `solutions/`. Java modules are
self-contained Maven projects (`pom.xml` in each), runnable independently:

- `demos/<module>/` — instructor-led demo assets and guides
- `labs/<module>/` — your starter files and the task README for that module
- `solutions/<module>/` — reference solutions (try the lab first!)

## Modules

| # | Module | Lab |
|---|---|---|
| 1 | Core Java Refresher | [labs/01-core-java-refresher/README.md](labs/01-core-java-refresher/README.md) |
| 2 | Object-Oriented Principles in Practice | [labs/02-oo-principles-in-practice/README.md](labs/02-oo-principles-in-practice/README.md) |
| 3 | OOAD: From Requirements to Objects | [labs/03-ooad-from-requirements-to-objects/README.md](labs/03-ooad-from-requirements-to-objects/README.md) |
| 4 | UML Class Diagrams | [labs/04-uml-class-diagrams/README.md](labs/04-uml-class-diagrams/README.md) |
| 5 | UML Sequence Diagrams | [labs/05-uml-sequence-diagrams/README.md](labs/05-uml-sequence-diagrams/README.md) |
| 6 | Peer Review | [labs/06-peer-review/README.md](labs/06-peer-review/README.md) |
| 7 | SOLID Principles Part 1 (S, O, L) | [labs/07-solid-principles-part1/README.md](labs/07-solid-principles-part1/README.md) |
| 8 | SOLID Principles Part 2 (I, D) | [labs/08-solid-principles-part2/README.md](labs/08-solid-principles-part2/README.md) |
| 9 | Clean Code | [labs/09-clean-code/README.md](labs/09-clean-code/README.md) |
| 10 | TDD Fundamentals | [labs/10-tdd-fundamentals/README.md](labs/10-tdd-fundamentals/README.md) |
| 11 | JUnit | [labs/11-junit/README.md](labs/11-junit/README.md) |
| 12 | TDD in Practice | [labs/12-tdd-in-practice/README.md](labs/12-tdd-in-practice/README.md) |
| 13 | Mission Build | [labs/13-mission-build/README.md](labs/13-mission-build/README.md) |
| 14 | Sprint 5 Wrap-up & Design Rationale | [labs/14-sprint5-wrapup/README.md](labs/14-sprint5-wrapup/README.md) |

## Getting started

1. Clone this repository.
2. `cd` into a module's `labs/<module>/` folder and run `mvn test` to confirm your environment
   works before starting.
3. Work through the modules in order, starting with `labs/01-core-java-refresher/README.md`.

## Support

Ask your trainer or Scrum team lead during class, or raise a question in the cohort's usual
support channel.
