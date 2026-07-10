# Module 7 — Model Answers & Notes

## Kata A — `AdvisorMapper`

```java
@Select("SELECT advisor_id, name, region FROM advisors WHERE advisor_id = #{advisorId}")
Advisor findById(int advisorId);
```

`#{advisorId}` is a bound parameter, not a string-concatenated value — MyBatis compiles this to a
`PreparedStatement`. The same SQL-injection protection you'd get from raw JDBC.

## Kata B — `TransactionMapper.xml`

```xml
<select id="findByAccountId" resultType="com.fidelity.leap.sprint6.Transaction">
    SELECT
        t.transaction_id AS transactionId,
        i.ticker          AS ticker,
        t.txn_type        AS txnType,
        t.quantity        AS quantity,
        t.price           AS price,
        t.txn_date        AS txnDate
    FROM transactions t
    JOIN instruments i ON t.instrument_id = i.instrument_id
    WHERE t.account_id = #{accountId}
    ORDER BY t.txn_date
</select>
```

## Why two styles for one module?

Neither is "better" — they suit different SQL:

- **Annotation-based** (`AdvisorMapper`): one line of SQL, no joins. Keeping it next to the method
  signature means there's nowhere else to look.
- **XML-based** (`TransactionMapper`): a join across two tables, several aliased columns. Written
  as a Java string, this would be an unreadable single line (or an awkward `+`-concatenated block).
  As XML, it reads like SQL because it *is* SQL — no host-language syntax to escape around it.

Real codebases usually pick XML as the default and reserve annotations for genuinely trivial
single-table lookups, which is why `HoldingMapper`/`TransactionMapper` (join-heavy) are XML while
`InstrumentMapper`/`AdvisorMapper` (single-table lookups) are annotations in this module.

## `transactionId: 3` has `quantity: null`

That's real data, not a bug — check `enterprise-schema.sql`: transaction type `DIVIDEND` doesn't
carry a quantity in this schema, only a `price`. Worth pointing out if a learner asks about it:
this is what working against a real, pre-existing schema looks like, versus data you designed
yourself to always be complete.
