# Module 7 Lab — Persistence with MyBatis: Mappers & Connecting to Postgres

## Objectives

By the end of this lab you will have:

- Written an annotation-based MyBatis mapper (SQL in Java, via `@Select`)
- Written an XML-based MyBatis mapper (SQL in a separate `.xml` file)
- Connected a Spring Boot service to the Sprint 3 Postgres schema and returned live data

## Setup

- Java 21 and Maven installed
- Your local Postgres server from Sprint 3 Module 2, with a fresh `mission` database seeded with
  the enterprise schema:

  ```bash
  psql -U postgres -h localhost -c "CREATE DATABASE mission;"
  psql -U postgres -h localhost -d mission -f ../../../leap-sprint3/shared/enterprise-schema.sql
  ```

  (If you already created this database earlier in the sprint, there's nothing to do — it's
  already seeded.)
- Given, don't modify: `MissionServiceApplication.java`, `Advisor.java`, `Transaction.java`,
  `TransactionMapper.java` (interface only), `PortfolioController.java`, `application.properties`
  — but do check `application.properties`' `spring.datasource.username`/`password` match your
  own local Postgres superuser credentials from Sprint 3, and update them if they don't

## Task

### Kata A — `AdvisorMapper` (annotation-based)

Add a `findById(int advisorId)` method to `AdvisorMapper`, annotated with `@Select`, that queries
the `advisors` table (`advisor_id`, `name`, `region`) for the matching row and maps it to an
`Advisor`.

### Kata B — `TransactionMapper.xml` (XML-based)

Write the `<select id="findByAccountId">` in `TransactionMapper.xml`. Join `transactions` to
`instruments` (on `instrument_id`) so each result includes the instrument's `ticker`. Select
`transaction_id`, `ticker`, `txn_type`, `quantity`, `price`, `txn_date`, filtered by
`account_id = #{accountId}`, ordered by `txn_date`.

Notice `mybatis.configuration.map-underscore-to-camel-case=true` is already set in
`application.properties` — that's why aliasing `txn_type AS txnType` isn't strictly required, but
it's good practice to be explicit.

### Verify

```bash
mvn spring-boot:run
```

```bash
curl http://localhost:8080/advisors/1
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/advisors/999
curl http://localhost:8080/accounts/1/transactions
```

## Deliverable

`AdvisorMapper.java` and `TransactionMapper.xml`, both fully implemented.

## Acceptance criteria

- `mvn compile` succeeds (it will not until `AdvisorMapper.findById` exists — `PortfolioController`
  already calls it)
- `GET /advisors/{id}` returns `200` with real advisor data for an id that exists, `404` for one
  that doesn't
- `GET /accounts/{id}/transactions` returns the account's transactions, each including the
  instrument ticker, ordered by date
