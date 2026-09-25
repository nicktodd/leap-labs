# Module 9 Lab - Pair Exercise: One-Page Payments Summary

## Scenario

PaySprint's head of card payments wants a one-page summary of February's card activity for the
monthly review: who is spending, where, through which channel, and how spend moved through the
month. The data sits in three files that have to be combined first, and one of them is known to
lag behind. You and your partner will build the summary as a single script.

## Objectives

By the end of this lab you will have:

- Merged tables safely, using `validate=` to check key relationships and `indicator=True` to
  find rows with no match
- Compared inner and left joins and chosen one for a stated reason
- Used named aggregation to produce several differently named summary columns in one call
- Built a `pivot_table` with margins and checked its totals
- Summarised a time series by day and week, and smoothed it with a rolling mean
- Written evidence-based takeaways with a partner

## Setup

- `pip install pandas`
- Data: `shared/transactions.csv`, `shared/customers.csv` and `shared/fx_rates.csv` (in the
  repo's `shared/` folder)
- Starter file: `starter_payments_deep_dive.py`, in `labs/09-pandas-deeper-dive/`. It loads the
  three files. Run it with `python starter_payments_deep_dive.py` from any folder.
- Pair up with a partner for this exercise

## The data

- `transactions.csv` (140 rows, 2 Feb to 1 Mar 2026): `txn_id`, `txn_timestamp`, `customer_id`,
  `customer_name`, `merchant_category`, `channel`, `currency`, `amount`, `status`, `is_fraud`.
- `customers.csv` (11 rows): `customer_id`, `segment` (Standard / Premium / Business),
  `credit_limit_gbp`, and others.
- `fx_rates.csv` (3 rows): `currency`, `rate_to_gbp`. FX (foreign exchange) rates used to
  convert `amount` to GBP.

In this lab, "spend" means the `amount_gbp` of APPROVED transactions: a declined payment moves
no money. Steps 1-3 use all 140 transactions; steps 4-5 use approved transactions only.

## Task

Print each section under a clear heading so that the output reads as a one-page summary.

1. **FX merge.** Merge `fx_rates.csv` onto the transactions on `currency` with
   `validate="many_to_one"` and add `amount_gbp = amount * rate_to_gbp`, rounded to 2 decimal
   places. Check (with `assert` or a printed check) that the row count is still 140 and no rate
   is missing. In a comment, explain what `validate="many_to_one"` protects against.
2. **Customer merge.** Merge `customers.csv` (without its `customer_name` column) with
   `how="left"` and `indicator=True`. Print the counts of the `_merge` column, and describe the
   orphan rows (`left_only`): which customer, how many rows, how much GBP. Print the row count
   of an inner join for comparison. Fill the missing `segment` with `"Unknown"`. In a comment,
   state which join you keep and why.
3. **Named aggregation.** In one `groupby("segment").agg(...)` call, produce the columns
   `txn_count`, `customers` (distinct customers), `total_gbp`, `avg_gbp`, `decline_rate` (the
   mean of a boolean "is declined" column) and `fraud_count`. Sort by `total_gbp`.
4. **Pivot table.** Approved spend with rows `merchant_category`, columns `channel`, values
   `amount_gbp`, `aggfunc="sum"`, `fill_value=0`, `margins=True` (use
   `margins_name="Total"`). Check in code that the bottom-right total equals the total approved
   spend.
5. **Time series.** Using approved spend with `txn_timestamp` as the index:
   - daily spend with `resample("D").sum()`; print the number of days and the number of days
     with zero spend;
   - a 7-day rolling mean of the daily spend, printed next to the daily values for the last 10
     days;
   - weekly spend and transaction count with `resample("W-SUN")`, and the highest week;
   - the average number of transactions per day before and from payday (Friday 27 Feb 2026).
6. **Takeaways.** Write 3-5 one-line takeaways as comments at the end of the script, with your
   partner. Each takeaway must cite a specific number from your output.

## Pairing notes

- Decide together who drives (types) for which section; swap at least twice.
- Before writing the takeaways, each of you should look at the output on your own and note what
  stands out, then compare notes and agree the final 3-5 lines together.
- Each partner should be able to explain a section the other one typed.

## Acceptance criteria

- The script runs with `python starter_payments_deep_dive.py` with no errors or warnings.
- Step 1: 140 rows after the FX merge; total `amount_gbp` for all transactions is 18,084.88.
- Step 2: `_merge` shows 130 `both` and 10 `left_only` (all customer K012, 479.02 GBP); the inner
  join has 130 rows. The comment gives a reason for the choice of join.
- Step 3: one `.agg` call with named outputs; four segment rows including `Unknown`. Standard
  has 66 transactions, a decline rate of about 0.152 and 9 fraud cases.
- Step 4: no `NaN` cells; the margin total is 11,471.55 GBP and your code confirms it matches.
- Step 5: 28 daily rows; the highest week ends Sunday 1 Mar 2026 with 3,978.87 GBP.
- Step 6: 3-5 takeaways, each citing a number that appears in your output.

## Extension exercises

1. **Cumulative spend against credit limit.** Sort approved transactions by customer and time,
   compute a running total per customer with `groupby().cumsum()`, and divide by
   `credit_limit_gbp`. Inspect the month-end percentages, choose a meaningful threshold (25%
   works well), and find the first transaction where each customer reaches it. Done: a table of
   one row per customer that crosses the threshold, plus a comment on how much of that
   customer's spend is approved fraud.
2. **Melt the pivot back.** Take the pivot from step 4 without margins, `reset_index()` and
   `melt` it back to long form (one row per category and channel). Done: the long-form totals
   per channel and overall match the source data (checked in code), and you can explain what
   happens if you melt the version with margins.
3. **Weekly spend per category.** Use
   `groupby([pd.Grouper(key="txn_timestamp", freq="W-SUN"), "merchant_category"])` and then
   `unstack` to build a week x category table. Done: the table has one row per week and one
   column per category with no `NaN`, its row totals match step 5's weekly totals, and a comment
   names the category that drives the large weeks.
4. **Time between transactions.** Use `groupby("customer_id")["txn_timestamp"].diff()` (after
   sorting) to compute the time since each customer's previous transaction. Done: the six
   shortest gaps are printed with merchant, amount and `is_fraud`, and a comment links the
   shortest ones to the K009 card-testing burst on 12 Feb and explains why a gap alone is not a
   fraud signal.
