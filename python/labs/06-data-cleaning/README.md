# Module 6 Lab - Data Cleaning & Preparation

## Scenario

PaySprint's card-payments data arrives from several acquirers and a manual back-office feed, and
the raw extract for February 2026 is not fit for analysis: amounts contain currency symbols,
channels are spelt several ways, dates arrive in two formats and some rows are duplicated. Before
the fraud and analytics teams can use it, you must produce a clean table and document every
decision you took, so that an auditor can follow it.

## Objectives

By the end of this lab you will have:

- Quantified data-quality problems before changing anything
- Converted text amounts to numbers with a regular expression and `pd.to_numeric`, and decided
  what to do with values that cannot be recovered
- Normalised categorical values with an explicit mapping, and checked the result
- Recovered missing values from other rows, after verifying that the recovery is safe
- Parsed timestamps in two formats without guessing, and rejected an impossible date
- Shown that the order of cleaning steps changes which duplicates are found
- Flagged (not removed) an outlier using both a statistical rule and a business rule

## Setup

- `pip install pandas` (pandas 3.x)
- Data files in `shared/` (repo root): `messy-transactions-raw.csv` (the raw extract) and
  `fx_rates.csv` (FX (foreign exchange) rates to GBP, for the outlier step)
- Starter file: `labs/06-data-cleaning/starter_clean_transactions.py`. Run it with
  `python starter_clean_transactions.py` from any folder.

## The data

`shared/messy-transactions-raw.csv` has 143 rows and the same columns as
`shared/transactions.csv` (used in Module 5): `txn_id`, `txn_timestamp`, `customer_id`,
`customer_name`, `merchant`, `merchant_category`, `channel`, `country` (ISO (International
Organization for Standardization) 3166 country code), `currency`, `amount`, `status`,
`distance_from_home_km`, `is_fraud`. `txn_id` is the business key: one transaction should appear
exactly once.

Do not open the file and fix it by hand. Every problem must be found and fixed in code, so the
same script can clean next month's extract.

## Task

For **each** fix, write the code **and** a one-line comment explaining your reasoning. The
reasoning is graded, not only the resulting numbers.

Before you start coding, read all nine steps and decide the order in which you will run them.
Two of the steps depend on earlier ones: step 6 needs clean merchant names, and step 8 finds a
different number of duplicates depending on what has already been normalised. Your script should
print enough to show the effect of the order you chose.

1. **Quantify.** Print the nulls per column, the distinct raw `channel` values (print them with
   `repr()` so leading and trailing spaces are visible) and the number of exact duplicate rows
   (`df.duplicated().sum()`). Note which dtype pandas gave `amount`, and why.
2. **Amounts.** Remove currency symbols (`£`, `€`, `$`) and thousands separators with
   `.str.replace(..., regex=True)`, then convert with `pd.to_numeric(..., errors="coerce")`.
   Print the rows that became NaN (there are two: one blank, one containing text) and drop them.
   Your comment must say why these amounts cannot be reconstructed, unlike the recomputed trade
   values in the demo.
3. **Channel.** Strip whitespace and lower-case, then map every variant to exactly one of
   `Online`, `In-store`, `Contactless` using a dict. Assert that there are exactly three distinct
   values and no NaN. Comment on why `.str.title()` is not enough here.
4. **Country.** Replace `UK` with the ISO code `GB`. Comment on why this matters when the data is
   later joined to reference data such as `customers.csv`.
5. **Merchant.** Strip leading and trailing whitespace from `merchant`.
6. **Missing `merchant_category`.** Three rows have no category, but each merchant appears
   elsewhere with one. Build a merchant -> category lookup from the non-null rows, **verify** that
   every merchant has exactly one category (`nunique()`), then fill the gaps with `.map()` and
   `.fillna()`. Comment on why this fill is safe here, and when it would not be.
7. **Timestamps.** The column mixes `YYYY-MM-DD HH:MM` and `DD-Mon-YYYY HH:MM` (for example
   `03-Feb-2026 14:22`). Parse each format explicitly with `pd.to_datetime(..., format=...,
   errors="coerce")` and combine the results. Print any row that matches neither format and
   reject it. Do not guess a replacement date: comment on why.
8. **Duplicates.** Print `df.duplicated().sum()` again and compare it with the raw count from
   step 1. Explain the difference in a comment. Then remove duplicates on the business key
   `txn_id`.
9. **Outlier.** Convert amounts to GBP with `fx_rates.csv`, then flag rows whose GBP amount is
   above the upper IQR (interquartile range) fence `Q3 + 1.5 * IQR` **within their
   `merchant_category`**. Also apply the business rule that a UK contactless payment cannot
   exceed GBP 100. Print every flagged row with a column showing which rule(s) it broke. Do not
   drop anything. Write one sentence in a comment on how you would investigate the row that breaks
   both rules (who you would ask, and what would confirm or rule out a keying error).

## Acceptance criteria

- The script runs with `python starter_clean_transactions.py` with no errors or warnings.
- Step 1 reports 9 distinct raw channel values and 1 exact duplicate row.
- The final cleaned DataFrame has **138 rows** (143 raw, minus 2 unrecoverable amounts, 1
  invalid date and 2 duplicates).
- `channel` has exactly three values: `Contactless`, `In-store`, `Online`.
- No `country` value is `UK`.
- `amount` has a `float64` dtype and `txn_timestamp` a `datetime64` dtype.
- `merchant_category` has zero nulls.
- Step 8 finds 2 duplicates after normalisation (P0095 and P0102), not the 1 found on the raw
  file.
- P0141 is printed as flagged and is still present in the final DataFrame.
- Every step has a one-line reasoning comment.

## Extension exercises

1. **Before/after data-quality report.** Write a function that profiles a DataFrame (row count,
   nulls per column, distinct `channel` and `country` values, duplicate rows and duplicate
   `txn_id`s) and returns a Series. Print the raw and clean profiles side by side as one table with
   `before`, `after` and `change` columns, and save it to `output/quality_report.csv`. Done when
   every number in the table can be explained by one of your cleaning steps.
2. **A pipeline of small functions.** Refactor each step into a function that takes a DataFrame
   and returns a new DataFrame (no in-place modification), and chain them with `.pipe()`. Then use
   the functions to show, in code, that removing exact duplicates *before* normalising leaves
   P0102 in the data twice. Done when `clean(raw)` returns 138 rows and the wrong-order run
   returns 139.
3. **Quarantine instead of discard.** Write every rejected row, with its original raw values, to
   `output/rejected_rows.csv` with an extra `reject_reason` column (blank amount, non-numeric
   amount, invalid date, duplicate). Assign each rejected row exactly one reason. Done when the
   script asserts that raw rows = clean rows + rejected rows (143 = 138 + 5) and that no row is in
   both sets.
4. **Global versus segment-aware outlier rules.** Compute one IQR fence for all transactions and
   compare it with per-category fences. Print how many rows each rule flags per category, and list
   the legitimate (`is_fraud == 0`) Travel and Electronics purchases that only the global rule
   flags. Done when you have written a short comment explaining why segment-aware thresholds are
   better here, and what their remaining weakness is in categories such as Dining and Transport.
