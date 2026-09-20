# LEAP Program - This Week's Lab Exercises

This repository contains the hands-on lab exercises accompanying **This Week: Software
Engineering Essentials, Java & OOAD**, week 3 of the LEAP graduate programme.

## Prerequisites

- Java 21 (JDK) and Maven
- An IDE with UML support helpful but not required (diagrams are drafted by hand/whiteboard
  first, then captured - see Module 4 onward)
- GitHub Copilot Chat (continuing as a learning aid - Module 9 specifically has you critically
  assess a GenAI-suggested refactor rather than accept it outright)

## Coming from Week 2

Week 2 covered Agile/Scrum practice, Git, CI/CD, containerisation, secure coding, and a first
pass at data systems and SQL. This week shifts to Java: Module 1 is a refresher covering the
core language features (types, collections, exceptions, control flow) most learners will
already have seen, before moving into object-oriented design and software engineering
practice - OOAD, UML, SOLID, clean code, and test-driven development.

## Structure

Each module has its own folder under `demos/`, `labs/`, and `solutions/`. Java modules are
self-contained Maven projects (`pom.xml` in each), runnable independently:

- `demos/<module>/` - instructor-led demo assets and guides
- `labs/<module>/` - your starter files and the task README for that module
- `solutions/<module>/` - reference solutions (try the lab first!)

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
| 14 | Wrap-up & Design Rationale | [labs/14-mission-wrapup/README.md](labs/14-mission-wrapup/README.md) |

## Getting started

1. Clone this repository.
2. `cd` into a module's `labs/<module>/` folder and run `mvn test` to confirm your environment
   works before starting.
3. Work through the modules in order, starting with `labs/01-core-java-refresher/README.md`.

## Support

Ask your trainer or Scrum team lead during class, or raise a question in the cohort's usual
support channel.
