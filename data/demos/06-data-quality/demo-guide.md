# Demo: Module 06 - Data Quality, Validation, Missing, Duplicate & Inconsistent Data

**Duration:** 12 minutes
**Prerequisite:** `shared/enterprise-schema.sql` and `shared/raw-client-intake.sql`, both loaded
in the same database.

## Part 1: Why data quality comes before modelling (1 min)

Narration: from Module 07 onward, you design and build your own schema for the Model Portfolio
service. A well-designed schema can still be filled with bad data if nobody checks it first.
Data quality is a discipline applied before data is trusted enough to model, not a final step
tacked on afterward. `raw_client_intake` holds client applications exactly as they'd arrive from
an intake form: unchecked, unvalidated.

## Part 2: Finding missing data (1.5 min)

```sql
SELECT * FROM raw_client_intake
WHERE full_name IS NULL
   OR date_of_birth IS NULL;
```

Narration: `IS NULL`, never `= NULL`, a reminder from Module 03. Two rows here are missing
critical fields, one has no name, one has no date of birth. Neither should be silently loaded
into a real clients table.

## Part 3: Finding exact duplicates (2 min)

```sql
SELECT full_name, date_of_birth, email, COUNT(*)
FROM raw_client_intake
GROUP BY full_name, date_of_birth, email
HAVING COUNT(*) > 1;
```

Narration: `GROUP BY` the columns that should uniquely identify a person, `HAVING COUNT(*) > 1`
finds any combination appearing more than once. This finds Tomasz Nowak, submitted twice, a few
days apart. A near-duplicate (same person, slightly different email) needs a different, harder
technique, not covered today.

## Part 4: Inconsistent data, casing and invalid values (3 min)

```sql
SELECT DISTINCT risk_profile
FROM raw_client_intake
ORDER BY risk_profile;
```

Narration: `DISTINCT` surfaces every actual variant of a column's values, the fastest way to
spot casing drift before writing any complex logic. Point at the result: `ADVENTUROUS`,
`Adventurous`, `adventurous` are the same underlying value in three casings. So are `Balanced`
and `balanced`, `Cautious` and `cautious`. `Moderate` is different, and that's the trap.

```sql
SELECT * FROM raw_client_intake
WHERE LOWER(risk_profile) NOT IN ('cautious', 'balanced', 'adventurous');
```

Narration: `LOWER(...) NOT IN (...)` distinguishes invalid from merely differently-cased.
`Moderate` isn't a casing problem, normalising case wouldn't fix it, it just isn't a real risk
profile. This needs a human decision (reject the application, or ask the client to clarify),
not an automatic fix.

## Part 5: Whitespace and referential consistency (3 min)

```sql
SELECT full_name, LENGTH(full_name), LENGTH(TRIM(full_name))
FROM raw_client_intake
WHERE full_name != TRIM(full_name);
```

Narration: compare a column's length to its trimmed length. Invisible in a normal `SELECT`, but
very real once compared exactly downstream, a join or a uniqueness check against this column
would silently fail. Unlike an invalid value, this one is safe to fix automatically with
`TRIM()`.

```sql
SELECT r.full_name, r.advisor_name
FROM raw_client_intake r
LEFT JOIN advisors a
  ON LOWER(TRIM(r.advisor_name)) = LOWER(a.name)
WHERE a.advisor_id IS NULL;
```

Narration: reuses Module 04's `LEFT JOIN ... WHERE ... IS NULL` pattern to find unmatched rows.
A row can pass every other check and still reference something that doesn't exist. Point at the
two results: `Priya Shaw` is a likely typo for the real advisor, `Priya Shah`, `Sam Whitmore`
doesn't match any advisor at all, not a typo, a fabricated name. Same query, two different root
causes.

## Key message

Missing, duplicate, and inconsistent data are three different problems needing three different
techniques, `IS NULL`, `GROUP BY ... HAVING COUNT(*) > 1`, and `DISTINCT`/casing/whitespace
checks. Not every issue has the same right fix: whitespace is safe to automate away, an invalid
value or an unmatched advisor needs a human to decide. Today's checks become the standard you'll
hold your own mission model data to, starting in Module 13.
