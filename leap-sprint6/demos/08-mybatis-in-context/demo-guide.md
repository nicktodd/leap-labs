# Module 8 Demo Guide — MyBatis in Context: vs JPA/Hibernate

This is a short, discussion-led module — the goal is a clear mental model of the trade-off, not
another kata. Module 7's real depth with MyBatis already happened; today just gives it a
name and a comparison.

## Run Both, Side by Side

Module 7's `InstrumentMapper` (MyBatis) and today's `InstrumentRepository` (Spring Data JPA) do
the *exact same job* — `GET /instruments/{ticker}` against the same `instruments` table. Have
both projects open side by side.

```bash
# Module 7 (MyBatis) - already built
cd ../07-persistence-with-mybatis && mvn spring-boot:run
curl http://localhost:8080/instruments/AAPL

# Stop it, then Module 8 (JPA)
cd ../08-mybatis-in-context && mvn spring-boot:run
curl http://localhost:8080/instruments/AAPL
```

Same URL, same JSON response. **Say this explicitly**: from the outside, a client of this API
cannot tell which persistence technology is behind it, and shouldn't need to.

## The Repository Interface: Compare Directly

Open `InstrumentMapper.java` (Module 7) and `InstrumentRepository.java` (today) side by side.

**MyBatis:**
```java
public interface InstrumentMapper {
    @Select("SELECT ticker, name, asset_class, currency FROM instruments WHERE ticker = #{ticker}")
    Instrument findByTicker(String ticker);
}
```

**Spring Data JPA:**
```java
public interface InstrumentRepository extends JpaRepository<Instrument, Integer> {
    Optional<Instrument> findByTicker(String ticker);
}
```

**Point at the difference directly**: there is no SQL anywhere in the JPA version — not even a
method body. Spring Data JPA parses the method *name* (`findByTicker`) and derives the query at
startup. `JpaRepository<Instrument, Integer>` also hands you `findById`, `save`, `deleteById`,
`findAll`, and more, for free, with zero code written.

## Turn On `spring.jpa.show-sql=true` and Look at What Ran

```
select
    i1_0.instrument_id,
    i1_0.asset_class,
    i1_0.currency,
    i1_0.name,
    i1_0.ticker
from
    instruments i1_0
where
    i1_0.ticker=?
```

Hibernate generated this — nobody wrote it. Ask the group: is that a good thing or a bad thing?
Land on: **it depends what you need.** For a straightforward lookup like this, it's a non-event.
For a five-table join with conditional filters, generated SQL can become something you're
reverse-engineering from a log line instead of just reading.

## The Real Difference: What Is `Instrument` Now?

Open `Instrument.java` in both projects.

- **Module 7's `Instrument`** — a plain class. Getters/setters, nothing else. It exists for the
  duration of one method call and is then just a Java object like any other.
- **Module 8's `Instrument`** — `@Entity`. Once Hibernate loads it, it's under **persistence
  context management**: Hibernate tracks it, and if a field changes before the transaction
  commits, Hibernate can write that change back to the database automatically (`dirty checking`)
  — nobody has to call an explicit `update`.

**This is the trade-off in one sentence**: JPA buys you less code for the common case, at the
cost of query behaviour that isn't always visible by reading the Java — you're trusting a
framework's SQL generation and object lifecycle instead of reading the SQL yourself.

## When Would You Reach for Each?

Discussion, not a definitive rule — but a reasonable default:

- **JPA/Hibernate**: CRUD-heavy domains with a genuine object graph (entities that reference each
  other, need cascading saves, etc.) — you get a lot of correct behaviour for very little code.
- **MyBatis**: reporting-style or query-heavy work, complex joins, or teams that specifically want
  to see and control every query that runs against production data.
- Real organisations often use **both** in the same codebase — JPA for the transactional core,
  MyBatis (or plain JDBC) for reporting queries where hand-written SQL is genuinely clearer.

## Transition to the Lab

No kata today. The lab is a short written discussion, using both `InstrumentMapper.java` and
`InstrumentRepository.java` as concrete evidence rather than abstract opinions.
