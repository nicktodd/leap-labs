# LEAP Program - This Week's Lab Exercises

This repository contains the hands-on lab exercises accompanying **This Week: Data Systems and
Data Modelling**, taught as part of week 2 of the LEAP graduate programme (alongside
`pipelines/`, which covers this same week's engineering-practices content).

## Prerequisites

- PostgreSQL (server) and `psql`
- pgAdmin (a Postgres-native GUI client, used alongside `psql` from Module 02 onward)
- A Snowflake trial/sandbox account, provisioned by your trainer (Module 12 only)
- GitHub Copilot Chat (continuing as a learning aid, and for critiquing alternative query
  formulations in Module 05)

## Three datasets run through this whole week

- **`shared/enterprise-schema.sql`** - a pre-loaded, read-heavy "PaySprint Wealth Platform"
  schema (advisors, clients, accounts, instruments, holdings, transactions). Used for query
  practice in Modules 02-05, and referenced again in Module 10. You explore and query this,
  you don't design it.
- **`shared/raw-client-intake.sql`** - unchecked client applications, loaded alongside the
  enterprise schema for Module 06's data quality lab. It reuses the enterprise schema's
  `advisors` table for a referential consistency check.
- **`shared/mission-brief.md`** - the business brief for the **Model Portfolio service**, a
  separate, narrower system your team designs from scratch starting in Module 07, implements
  in Postgres in Module 13, and extends for historical trade data in the Module 14 capstone.
  `shared/messy-flat-file.csv` is a denormalized starting point used in Module 07's
  normalization exercise.

## Structure

Each module has its own folder under `demos/`, `labs/`, and `solutions/`:

- `demos/<module>/` - instructor-led demo assets and guides
- `labs/<module>/` - your starter files and the task README for that module
- `solutions/<module>/` - reference solutions (try the lab first!)

## Modules

| # | Module | Lab |
|---|---|---|
| 1 | Data Systems Concepts | [labs/01-data-systems-concepts/README.md](labs/01-data-systems-concepts/README.md) |
| 2 | Postgres Essentials & Environment Setup | [labs/02-postgres-essentials/README.md](labs/02-postgres-essentials/README.md) |
| 3 | SQL Fundamentals Refresher | [labs/03-sql-fundamentals/README.md](labs/03-sql-fundamentals/README.md) |
| 4 | Advanced SQL Part 1 - Joins & Aggregation | [labs/04-sql-joins-aggregation/README.md](labs/04-sql-joins-aggregation/README.md) |
| 5 | Advanced SQL Part 2 - Subqueries, CTEs & Derived Tables | [labs/05-sql-subqueries-ctes/README.md](labs/05-sql-subqueries-ctes/README.md) |
| 6 | Data Quality: Validation, Missing, Duplicate & Inconsistent Data | [labs/06-data-quality/README.md](labs/06-data-quality/README.md) |
| 7 | RDBMS Modelling Part 1 - Entities, Relationships & Normalization | [labs/07-rdbms-modelling-part1/README.md](labs/07-rdbms-modelling-part1/README.md) |
| 8 | ER Diagrams: Translating Requirements into Schemas | [labs/08-er-diagrams/README.md](labs/08-er-diagrams/README.md) |
| 9 | RDBMS Modelling Part 2 - Keys, Indexes & Constraints | [labs/09-rdbms-modelling-part2/README.md](labs/09-rdbms-modelling-part2/README.md) |
| 10 | Structured Problem-Solving | [labs/10-structured-problem-solving/README.md](labs/10-structured-problem-solving/README.md) |
| 11 | NoSQL Overview | [labs/11-nosql-overview/README.md](labs/11-nosql-overview/README.md) |
| 12 | Cloud Data Warehouses & Snowflake Overview | [labs/12-snowflake-overview/README.md](labs/12-snowflake-overview/README.md) |
| 13 | Implementing the Data Model in Postgres | [labs/13-implementing-the-model/README.md](labs/13-implementing-the-model/README.md) |
| 14 | Capstone: Extending the Schema for Historical Trade Data | [labs/14-capstone-historical-trades/README.md](labs/14-capstone-historical-trades/README.md) |
| 15 | Week 2 Wrap-up & Assessment Prep (Data) | [labs/15-sprint3-wrapup/README.md](labs/15-sprint3-wrapup/README.md) |

## Getting started

1. Clone this repository.
2. Load `shared/enterprise-schema.sql` into a local Postgres database (Module 02 walks through
   this step by step).
3. Work through the modules in order, starting with `labs/01-data-systems-concepts/README.md`.

## Support

Ask your trainer or Scrum team lead during class, or raise a question in the cohort's usual
support channel.
