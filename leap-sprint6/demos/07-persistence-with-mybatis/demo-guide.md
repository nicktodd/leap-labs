# Module 7 Demo Guide — Persistence with MyBatis: Mappers & Connecting to Postgres

Everything before today has run on hardcoded data (`InMemoryPortfolioRepository`,
`InMemoryOrderRepository`). Today the service talks to the real Sprint 3 Postgres schema — the
same `enterprise-schema.sql` learners already know from Sprint 3.

```bash
# Confirm the local mission database exists (created earlier in the sprint, from
# Sprint 3's enterprise-schema.sql) - see the lab README's Setup section if not

mvn spring-boot:run

curl http://localhost:8080/instruments/AAPL
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/instruments/NOPE
curl http://localhost:8080/clients/1/holdings
```

Expect: real instrument data for `AAPL`; a clean `404` for an unknown ticker; a list of Alice
Johnson's holdings across both her accounts, joined from three tables.

## Two Mappers, Two Styles — Side by Side

Open `InstrumentMapper.java` and `HoldingMapper.xml` next to each other.

**`InstrumentMapper`** — annotation-based. The SQL lives in `@Select`, right on the method:

```java
@Select("SELECT ticker, name, asset_class, currency FROM instruments WHERE ticker = #{ticker}")
Instrument findByTicker(String ticker);
```

**`HoldingMapper`** — XML-based. The interface (`HoldingMapper.java`) declares only the method
signature; the SQL lives in a separate file, `HoldingMapper.xml`, joining three tables:

```xml
<mapper namespace="com.neueda.leap.sprint6.HoldingMapper">
  <select id="findByClientId" resultType="com.neueda.leap.sprint6.Holding">
    SELECT c.client_id AS clientId, c.name AS clientName, i.ticker AS ticker, h.quantity AS quantity
    FROM holdings h
    JOIN accounts a    ON h.account_id = a.account_id
    JOIN clients c     ON a.client_id = c.client_id
    JOIN instruments i ON h.instrument_id = i.instrument_id
    WHERE c.client_id = #{clientId}
    ORDER BY i.ticker
  </select>
</mapper>
```

**Ask the group**: why would you pick one over the other? Land on: annotations are fine for a
one-line, single-table query — there's nowhere else worth looking. Once there's a join and several
aliased columns, cramming it into a Java string annotation gets unreadable fast; XML lets the SQL
read like SQL.

**Point out the wiring, not just the syntax**: the `namespace` in `HoldingMapper.xml` is the
Java interface's *fully qualified name*, and the `id` is the method name. That's the entire
connection between the two files — no annotation on the Java side at all. Get the namespace wrong
and MyBatis fails at startup with a clear "no statement found" error — worth deliberately breaking
it live if there's time, to show what that looks like.

## `#{ticker}` Is Not String Concatenation

Point at `#{ticker}` in the `@Select` annotation. This compiles to a JDBC `PreparedStatement` with
a bound parameter — the same SQL-injection protection Sprint 3 covered for raw SQL. Contrast
(don't demo) what `"...WHERE ticker = '" + ticker + "'"` would open up.

## `Instrument`/`Holding`: Plain Classes, Not Entities

Open `Instrument.java`. No `@Entity`, no `@Id`, no JPA annotations at all — just fields and
getters/setters. MyBatis populates it by matching column names (helped here by
`mybatis.configuration.map-underscore-to-camel-case=true` in `application.properties`, which turns
`asset_class` into `assetClass` automatically). There's no persistence context, no dirty-checking,
no entity lifecycle — the object exists only as the shape of one query's result. Module 8 picks
this contrast up directly against JPA/Hibernate.

## Transition to the Lab

Learners write one of each: an annotation-based `AdvisorMapper.findById` and the XML-based
`TransactionMapper.xml`, against the same live local Postgres database.
