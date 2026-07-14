# Fidelity LEAP Program — Sprint 7 Lab Exercises

This repository contains the hands-on lab exercises accompanying **Sprint 7: Enterprise Data &
Engineering Excellence**, week 7 of the Fidelity LEAP graduate programme.

## Prerequisites

- Java 21 (JDK) and Maven
- Docker (for running Kafka locally in Modules 5-9, and SonarQube in Module 12)
- Postgres (the Sprint 3 enterprise schema, reused for batch loading — see `shared/`)
- Python 3 with `pandas`, `psycopg2-binary`, and `kafka-python` (Module 14's dashboard — see
  `requirements.txt` in that module)
- GitHub Copilot Chat (continuing as a learning aid — Module 9 has you critically interpret a
  GenAI-suggested explanation of an unfamiliar Kafka consumer error, not accept it outright)

## Coming from Sprint 6

This sprint runs two threads in parallel. The trading platform (Sprint 6's mission service) gains
a real-time event stream — every accepted order also publishes a trade event to Kafka, so any
number of downstream consumers can react without polling or coupling to the mission service
directly. Separately, a deliberately neglected starter codebase gets refactored safely across the
week — characterisation tests, automated quality gates, and security scanning, all against one
real codebase rather than isolated toy examples. Both threads meet in Module 14, where the Sprint
4 analytics dashboard is extended to consume from both the new Kafka stream and a batch-loaded
warehouse table. See `shared/mission-brief.md`.

## Structure

Each module has its own folder under `demos/`, `labs/`, and `solutions/`. Java modules are
self-contained Maven projects (`pom.xml` in each), runnable independently:

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
| 1 | The Cost of Technical Debt & the Refactor Mission | [labs/01-the-cost-of-technical-debt-and-the-refactor-mission/README.md](labs/01-the-cost-of-technical-debt-and-the-refactor-mission/README.md) |
| 2 | Data Movement at Enterprise Scale: Batch vs Real-Time | [labs/02-data-movement-at-enterprise-scale-batch-vs-real-time/README.md](labs/02-data-movement-at-enterprise-scale-batch-vs-real-time/README.md) |
| 3 | Event-Driven Architecture Concepts: Events vs Requests | [labs/03-event-driven-architecture-concepts-events-vs-requests/README.md](labs/03-event-driven-architecture-concepts-events-vs-requests/README.md) |
| 4 | Kafka Fundamentals: Topics, Producers, Consumers, Partitions, Offsets | [labs/04-kafka-fundamentals-topics-producers-consumers-partitions-offsets/README.md](labs/04-kafka-fundamentals-topics-producers-consumers-partitions-offsets/README.md) |
| 5 | Hands-on: Standing Up Kafka & Producing/Consuming Messages | [labs/05-hands-on-standing-up-kafka-and-producing-consuming-messages/README.md](labs/05-hands-on-standing-up-kafka-and-producing-consuming-messages/README.md) |
| 6 | Designing a Kafka Pipeline for Trade Events | [labs/06-designing-a-kafka-pipeline-for-trade-events/README.md](labs/06-designing-a-kafka-pipeline-for-trade-events/README.md) |
| 7 | Batch Loading in Practice & ETL Patterns | [labs/07-batch-loading-in-practice-and-etl-patterns/README.md](labs/07-batch-loading-in-practice-and-etl-patterns/README.md) |
| 8 | Data Quality in Event & Batch Pipelines | [labs/08-data-quality-in-event-and-batch-pipelines/README.md](labs/08-data-quality-in-event-and-batch-pipelines/README.md) |
| 9 | Mission Build: Implementing Kafka Topics, Producers & Consumers | [labs/09-mission-build-implementing-kafka-topics-producers-and-consumers/README.md](labs/09-mission-build-implementing-kafka-topics-producers-and-consumers/README.md) |
| 10 | Code Quality Fundamentals & Code Smell Hunt | [labs/10-code-quality-fundamentals-and-code-smell-hunt/README.md](labs/10-code-quality-fundamentals-and-code-smell-hunt/README.md) |
| 11 | Safe Refactoring: Characterisation Tests & Refactoring Techniques | [labs/11-safe-refactoring-characterisation-tests-and-refactoring-techniques/README.md](labs/11-safe-refactoring-characterisation-tests-and-refactoring-techniques/README.md) |
| 12 | Quality Tooling & CI Quality Gates | [labs/12-quality-tooling-and-ci-quality-gates/README.md](labs/12-quality-tooling-and-ci-quality-gates/README.md) |
| 13 | DevSecOps: Shifting Security Left | [labs/13-devsecops-shifting-security-left/README.md](labs/13-devsecops-shifting-security-left/README.md) |
| 14 | Mission Build: Batch + Real-Time Dashboard Integration & Sprint 7 Wrap-up | [labs/14-mission-build-batch-and-real-time-dashboard-integration/README.md](labs/14-mission-build-batch-and-real-time-dashboard-integration/README.md) |

## Support

Ask your trainer or Scrum team lead during class, or raise a question in the cohort's usual
support channel.
