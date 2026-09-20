# Module 8 - Model Answers

1. **Code volume.** MyBatis: one method signature plus one `@Select` annotation (effectively one
   line of real content - the SQL string). JPA: one method signature, zero lines of query logic -
   Spring Data JPA derives the query from the method name `findByTicker` itself. JPA is shorter
   here because this is exactly the kind of simple, single-table lookup query derivation is built
   for.

2. **Visibility.** In JPA, the SQL comes from Hibernate's query generation, driven by the entity
   mapping and the derived query. To see what actually ran, you'd need to turn on
   `spring.jpa.show-sql=true` (or a SQL logging library) and read it out of the application log -
   it doesn't exist anywhere as a static, readable artifact the way the MyBatis `@Select` string
   or the XML mapper does.

3. **The `Instrument` class itself.** Module 8's `Instrument` is `@Entity`-managed: once Hibernate
   loads it inside a transaction, it's tracked by the persistence context. If a field on it is
   changed, Hibernate can detect that ("dirty checking") and write an `UPDATE` back to the
   database automatically when the transaction commits - no explicit save call needed. Module 7's
   `Instrument` is just a plain object; once MyBatis returns it, it has no ongoing relationship
   with the database at all. Changing a field on it does nothing.

4. **Trade a join.** In JPA, this would normally mean adding `@OneToMany`/`@ManyToOne`
   relationships between `Client`, `Account`, `Holding`, and `Instrument` entities, then either
   navigating the object graph (`client.getAccounts().stream().flatMap(...)`) or writing a JPQL
   query with joins. It's *less* code to declare the relationships once, but the query itself
   (walking an object graph, or writing JPQL) is arguably less direct than the plain SQL join in
   `HoldingMapper.xml` - and getting the relationship mappings wrong (wrong fetch type, missing
   cascade) is a common, sometimes subtle source of bugs. This is exactly the kind of multi-table,
   read-heavy query where MyBatis's directness has an edge.

5. **Your call.** A reasonable position: order submission and holdings updates are transactional,
   object-graph-shaped work with a genuine domain model (`Order`, `Holding`, `Account`) - JPA fits
   naturally there, and dirty checking removes a lot of manual `UPDATE` bookkeeping. Transaction
   history and reporting-style queries (Module 7's `TransactionMapper`) are read-heavy, join-heavy,
   and benefit from SQL you can see and tune directly - MyBatis fits there. A mixed approach,
   which is common in real enterprise Java codebases, isn't a compromise; it's picking the right
   tool per access pattern. There's no single "correct" answer here - mark for a *specific,
   justified* choice, not for matching this exact split.
