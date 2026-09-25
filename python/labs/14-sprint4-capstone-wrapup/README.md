# Module 14 Lab - Capstone: Building the Analytics Dashboard & Wrap-up

## Scenario

PaySprint's head of card payments wants a one-page monthly dashboard for February 2026: where
customers spend their money, how often payments are declined, what fraud cost, and whether the
numbers can be trusted. The only source available today is the raw monthly export, which has
every problem you met in Module 6. Your team will build the dashboard end to end, from the messy
file to charts and a plain-language summary, and then explain your choices to a non-technical
stakeholder.

## Objectives

By the end of this lab you will have:

- Applied Modules 1-13 together to build a small analytics dashboard surfacing at least three
  business insights, each backed by a specific number
- Structured the work as an ETL (extract, transform, load) pipeline with a validation gate that
  stops the run before bad data reaches a chart
- Reported data quality alongside the insights: rows received, rejected and why, and held for
  review
- Rehearsed explaining your data-access and analysis choices to a non-technical stakeholder
- Reviewed what Friday's assessment will check

## Setup

- Everything installed across this week: `pandas`, `matplotlib`, `scipy`, `scikit-learn`,
  `flask`, `requests`, `pytest`
- Starter file: `starter_payments_dashboard.py`, in `labs/14-sprint4-capstone-wrapup/`. Run it
  from any folder with `python labs/14-sprint4-capstone-wrapup/starter_payments_dashboard.py`.
  Until you complete `extract()` it stops with `NotImplementedError`.
- Outputs (the loaded CSV (comma-separated values) file and the PNG (Portable Network Graphics)
  charts) go into an `output/` folder next to the script.
- Team template: `stakeholder-explanation.md`, in the same folder.
- Work in your team. Split the functions between you, but agree the definitions (for example,
  what counts as "customer spend") before anyone writes analysis code.

## The data

| File | Contents |
|---|---|
| `shared/messy-transactions-raw.csv` | 143 raw rows of February card transactions: the same file you cleaned in Module 6 |
| `shared/fx_rates.csv` | FX (foreign exchange) rates: `currency`, `rate_to_gbp` (GBP 1.00, EUR 0.85, USD 0.79) |
| `shared/customers.csv` | Customer reference data (Extensions 3 and 4 only) |

Columns you will use most: `txn_id`, `txn_timestamp`, `customer_id`, `merchant`,
`merchant_category`, `channel`, `country`, `currency`, `amount`, `status`, `is_fraud` (1 = fraud
confirmed by the fraud team). `amount` is in the row's own currency, so convert to GBP (pounds
sterling) before adding amounts together. The reporting period is Mon 2 Feb to Sun 1 Mar 2026;
payday was Fri 27 Feb.

## Task

The demo dashboard read a clean file and its `transform()` did nothing. Yours starts from the
raw export, so every stage has work to do.

1. **Extract.** Complete `extract()`: read the raw file with every column as text
   (`dtype=str, keep_default_na=False`) and the FX rates file. In a comment, explain why the
   extract stage should not convert types.
2. **Transform.** Complete `transform(raw, fx)` with your Module 6 / Module 12 cleaning, copied
   into this file so it is self-contained. Order the steps so that normalisation happens before
   duplicate removal. Reject rows that cannot be recovered and record each rejected `txn_id`
   with a reason. Add `amount_gbp`. Do not delete the contactless payment above the GBP 100
   contactless limit: mark it `held_for_review` and leave it out of spend figures.
3. **Validate.** Complete `validate(df)` so it returns a list of failed checks, each a readable
   sentence (an empty list means the data passed). The main block already stops the run if the
   list is not empty. Prove the gate works: temporarily break something (for example, remove
   `USD` from the FX rates DataFrame) and confirm the script stops with your message and
   writes nothing.
4. **Load.** Complete `load()` to write the validated data to `output/dashboard_data.csv`.
5. **Insights.** Complete `compute_insights()`. Produce at least three insights in GBP, each
   with a specific number (not "Online payments are declined more often" but "Online payments
   are declined 15.9% of the time (11 of 69)"). Suggested areas: spend by merchant category,
   decline rate by channel, what confirmed fraud cost and how much of it was stopped, activity
   before and after payday. Write down your definition of "customer spend" in a comment.
6. **Charts.** Build at least two charts that support your insights, following Module 10:
   honest axes (bars start at zero, rates on a 0-100% axis), a title that states the finding,
   labelled axes with units. Save them as PNGs in `output/`.
7. **Dashboard.** Complete `print_dashboard()`: a plain-text summary a non-technical reader can
   follow without opening a chart. Include the reporting period, the insights with their
   numbers, and one data-quality line: rows received, rows rejected (with reasons and
   `txn_id`s), rows loaded, and transactions held for review.
8. **Stakeholder explanation.** As a team, complete `stakeholder-explanation.md` in plain
   language: why you read the data from the monthly export rather than Module 11's API (or the
   reverse), and why you are confident the numbers are trustworthy, naming the specific
   problems your cleaning and validation caught.
9. **Rehearse (pairs).** Present your dashboard and explanation to a partner from another team
   playing a non-technical stakeholder. The listener stops you at every piece of jargon, every
   unexplained acronym, and every claim without a number. Swap roles, then fix what they
   caught.

## What Friday's assessment checks

Two things: a **data analytics submission** (your dashboard code and its output) and a
**presentation** on your solution and approach. Both are things your team will have already
produced by the end of this lab.

## Acceptance criteria

- `extract`, `transform`, `validate`, `load`, `compute_insights`, `build_charts` and
  `print_dashboard` are separate, named functions, and the script runs from any folder.
- The pipeline receives 143 rows, rejects 5 and loads 138: P0095 and P0102 as duplicates (P0102
  only after normalisation), P0057 and P0086 for unusable amounts, P0131 for an impossible date
  (29 Feb 2026). P0141 is loaded but held for review.
- `validate()` returns an empty list for the cleaned data, and the script stops with a clear
  message, before writing any output, when a check fails.
- At least three insights are printed, each citing a specific GBP amount, count or percentage
  from the data. Self-check: defining customer spend as approved, not confirmed fraud and not
  held for review gives GBP 7,295.33 across 119 transactions, with Travel the largest category;
  Online payments are declined in 11 of 69 transactions.
- The dashboard includes a data-quality line with the rejected `txn_id`s and their reasons.
- At least two charts are produced, each with a title that states a finding, labelled axes, and
  an honest axis.
- `stakeholder-explanation.md` is written in plain language, with no unexplained acronyms or
  jargon, and gives a reason for the data-access choice that is specific to this dataset.
- Every team member can present at least one insight and explain the reasoning behind it,
  unprompted.

## Extension exercises

1. **Switchable source.** Add a `--source file|api` command-line option (`argparse`). In API
   (Application Programming Interface) mode, `extract()` fetches the transactions from the
   Module 11 payments API (`python shared/mock_api/payments_api.py`, port 5051, bearer token
   `paysprint-lab-token`), following `next_cursor` and waiting `Retry-After` seconds on a `429`.
   Convert the API rows to the raw file's shape (same column order, every value as text) so
   `transform()` and everything after it stay unchanged. Done: both modes produce a dashboard;
   API mode loads 140 rows with 0 rejected, and you can explain in one sentence why the two
   dashboards differ.
2. **Markdown report.** Write `output/dashboard.md`: a title, the period, the insights, the
   charts embedded with relative image links, a spend-by-category table and the data-quality
   lines. Reuse the same text as the console dashboard rather than writing the wording twice.
   Done: the file renders with all charts visible in a Markdown preview (for example, VS Code's).
3. **Fraud-rules panel.** Apply Module 4-style rules to the cleaned data: HIGH_VALUE
   (`amount_gbp` over 500), FOREIGN (country differs from the customer's `home_country` in
   `customers.csv`), UNKNOWN_CUSTOMER (no customer record), NIGHT_ONLINE (Online between 00:00
   and 04:59) and VELOCITY (3 or more transactions by one customer on one day). For each rule
   and for "any rule", report transactions flagged, confirmed fraud caught and false alarms, and
   name any fraud no rule catches. Done: a panel table, the precision (share of flagged
   transactions that are fraud) and recall (share of fraud that is flagged) of "any rule", and a
   comment on which customers the FOREIGN rule inconveniences.
4. **Customer statements.** For the top 3 customers by spend, print a short statement: spend,
   number of transactions, share of all customer spend, largest transaction, top category, and
   February spend as a share of `credit_limit_gbp` from `customers.csv`. K012 has transactions
   but no customer record: your join must keep K012 and report that the credit limit is not on
   file, not crash or silently drop the customer. Done: three statements, and a line naming any
   customer with no reference record.
