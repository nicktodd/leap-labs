# Fidelity LEAP Program — Sprint 6 Lab Exercises

This repository contains the hands-on lab exercises accompanying **Sprint 6: Software
Architecture & Enterprise Java**, week 6 of the Fidelity LEAP graduate programme.

## Prerequisites

- Java 21 (JDK) and Maven
- Docker (for Modules 12-13)
- Postgres (the Sprint 3 enterprise schema — see `shared/`)
- Node.js (for the auth stub used in Modules 9 and 13)
- GitHub Copilot Chat (continuing as a learning aid — Module 9 specifically has you critically
  interpret a GenAI-suggested explanation of an unfamiliar security stack trace, not accept it
  outright)

## Coming from Sprint 5

This sprint takes the Order Processing & Settlement Engine you built in Sprint 5 and turns it
into a real, deployable microservice. The core domain logic — `OrderValidator`, `HoldingUpdater`,
the `Instrument`/`Feeable` hierarchy — doesn't change; it gets wrapped in a Spring Boot service,
persisted to Postgres, secured with JWT, and containerised. See `shared/mission-brief.md`.

## Structure

Each module has its own folder under `demos/`, `labs/`, and `solutions/`. Java modules are
self-contained Maven projects (`pom.xml` in each), runnable independently:

- `demos/<module>/` — instructor-led demo assets and guides
- `labs/<module>/` — your starter files and the task README for that module
- `solutions/<module>/` — reference solutions (try the lab first!)

## Modules

| # | Module | Lab |
|---|---|---|
| 1 | Microservices & the Mission Service | [labs/01-microservices-and-the-mission-service/README.md](labs/01-microservices-and-the-mission-service/README.md) |
| 2 | Spring Boot Quickstart | [labs/02-spring-boot-quickstart/README.md](labs/02-spring-boot-quickstart/README.md) |
| 3 | Layered Architecture in Spring Boot | [labs/03-layered-architecture-in-spring-boot/README.md](labs/03-layered-architecture-in-spring-boot/README.md) |
| 4 | REST API Design Principles | [labs/04-rest-api-design-principles/README.md](labs/04-rest-api-design-principles/README.md) |
| 5 | Contract-First Design with OpenAPI | [labs/05-contract-first-design-with-openapi/README.md](labs/05-contract-first-design-with-openapi/README.md) |
| 6 | DTOs & Request Validation | [labs/06-dtos-and-request-validation/README.md](labs/06-dtos-and-request-validation/README.md) |
| 7 | Persistence with MyBatis: Mappers & Connecting to Postgres | [labs/07-persistence-with-mybatis/README.md](labs/07-persistence-with-mybatis/README.md) |
| 8 | MyBatis in Context: vs JPA/Hibernate | [labs/08-mybatis-in-context/README.md](labs/08-mybatis-in-context/README.md) |
| 9 | Securing the Service: JWT Validation | [labs/09-securing-the-service-jwt-validation/README.md](labs/09-securing-the-service-jwt-validation/README.md) |
| 10 | Handling Errors Gracefully | [labs/10-handling-errors-gracefully/README.md](labs/10-handling-errors-gracefully/README.md) |
| 11 | Mission Build: Assembling the Full Service | [labs/11-mission-build-assembling-the-full-service/README.md](labs/11-mission-build-assembling-the-full-service/README.md) |
| 12 | Containerising Spring Boot Services | [labs/12-containerising-spring-boot-services/README.md](labs/12-containerising-spring-boot-services/README.md) |
| 13 | Mission Build: Containerise, Integration Test & Wrap-up | [labs/13-mission-build-containerise-integration-test-wrap-up/README.md](labs/13-mission-build-containerise-integration-test-wrap-up/README.md) |

## Getting started

1. Clone this repository.
2. `cd` into a module's `labs/<module>/` folder and check that module's README for setup.
3. Work through the modules in order, starting with
   `labs/01-microservices-and-the-mission-service/README.md`.

## Support

Ask your trainer or Scrum team lead during class, or raise a question in the cohort's usual
support channel.
