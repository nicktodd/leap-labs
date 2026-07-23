# Module 8 Discussion — MyBatis vs JPA

## Question 1: Code volume

The MyBatis `findByTicker` requires one method declaration with an `@Select` annotation containing the SQL — roughly three lines of meaningful code. The JPA version requires a method declaration in the repository interface only (`findByTicker(String ticker)`), which is one line. JPA is shorter because Spring Data generates the query from the method name, so there is no SQL to write at all. For a simple single-table lookup, JPA wins on volume; MyBatis's verbosity pays off when the query is complex enough that generated SQL would be opaque or wrong.

## Question 2: Visibility

In the JPA version the SQL is generated at runtime by Hibernate, based on the entity mappings and the method name. You cannot see it in the source code. To find out what SQL actually ran in production you would enable `spring.jpa.show-sql=true` (or set `logging.level.org.hibernate.SQL=DEBUG`) and read the application logs — or query the database's slow query log. This makes performance tuning harder because the canonical version of the SQL does not exist until the JVM runs.

## Question 3: The Instrument class itself

Module 8's `Instrument` is a JPA entity, so after it is loaded from the database it is attached to Hibernate's persistence context (the "first-level cache" / session). Hibernate tracks every field on that object — this is called dirty checking. If any field changes before the transaction commits, Hibernate will automatically issue an `UPDATE` statement without you calling any save method. Module 7's `Instrument` is a plain Java object; once it is returned from the mapper there is no tracking at all — changing a field has no effect on the database unless you explicitly call an update method.

## Question 4: Trading a join with Spring Data JPA

To write "get a client's holdings joined across holdings → accounts → instruments" in Spring Data JPA you would need to: (a) annotate `Holding` with `@ManyToOne` pointing to `Account` and a second `@ManyToOne` pointing to `Instrument`; (b) annotate `Instrument` with `@Entity` and map all its columns; (c) annotate `Account` with `@Entity`; then (d) write a repository method `findByAccountId(int accountId)` or use `@Query` with JPQL. JPA would generate the joins automatically. It is arguably easier in the simplest case, but harder when you want to control exactly which columns are fetched, avoid N+1 selects (requiring `@EntityGraph` or `JOIN FETCH`), or use database-specific SQL hints. The MyBatis XML version makes the join completely explicit and is easier to tune.

## Question 5: My call

For Fidelity's mission service — order processing, holdings, and transaction history — I would choose MyBatis. The core queries (find a holding for a given account and ticker, update its quantity, insert a new row, pull transaction history with joined instrument data) are well-defined, finite, and performance-sensitive; having the exact SQL visible in the source makes code review, query plan analysis, and debugging straightforward. JPA's automatic dirty checking and entity lifecycle management add complexity that is not needed here: every write in this service is a deliberate, explicit business action (submit order → update holding), not a natural fit for the "load, mutate, let Hibernate figure out the update" pattern that JPA is optimised for.
