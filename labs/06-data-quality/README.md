# Module 06 Lab — Validate raw_client_intake

## Objectives

By the end of this lab you will have:

- Written SQL to find missing, duplicate, and inconsistent data in a real table
- Distinguished a genuinely invalid value from one that's merely differently-cased
- Written a referential consistency check using a technique from Module 04
- Decided, for each issue found, whether it's safe to fix automatically or needs a human call

## Setup

- `shared/enterprise-schema.sql`, loaded in Module 02 (this lab's referential check joins
  against its `advisors` table)
- `shared/raw-client-intake.sql`, loaded into the same database, run it now if you haven't
  already

## Task sheet

`raw_client_intake` holds client applications exactly as they arrived: nobody has checked them
yet. Write a query for each task below.

1. **Missing data**: find every row with a missing `full_name` or a missing `date_of_birth`.

2. **Exact duplicates**: find applications that are exact duplicates, same `full_name`, same
   `date_of_birth`, same `email`, submitted more than once.

3. **Distinct values**: list every distinct value present in `risk_profile`. How many actual
   underlying values do you think this represents?

4. **Invalid values**: find rows whose `risk_profile` is invalid, that is, not `Cautious`,
   `Balanced`, or `Adventurous` once you account for casing. Careful, one of these values isn't
   a casing problem at all, it's not a real risk profile no matter how you normalise it.

5. **Whitespace**: find rows where `full_name` has leading or trailing whitespace. This is
   invisible in a normal `SELECT`, think about how you'd prove it's there before you write the
   query.

6. **Referential consistency**: find rows whose `advisor_name` doesn't match any real advisor in
   the `advisors` table. Reuse the `LEFT JOIN ... WHERE ... IS NULL` pattern from Module 04.

7. **Classify the fix**: for each category of issue above (missing, duplicate, inconsistent
   casing, invalid value, whitespace, referential), write one line saying whether it's safe to
   fix automatically, and if so how, or whether it needs a human decision, and why.

## Acceptance criteria

- Six working queries, one per task 1-6, each returning the correct rows from
  `raw_client_intake`.
- Task 3's distinct-value list correctly separates casing variants of the same real value from
  the one genuinely invalid value.
- Task 6's query runs against the `advisors` table loaded from `shared/enterprise-schema.sql`,
  not a hardcoded list of advisor names.
- A short written answer for task 7, one line per issue category, with a reason.

If you finish early, write a single query that flags every application with at least one issue
from tasks 1-6, alongside a column naming which issue(s) it has.
