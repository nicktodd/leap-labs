# Module 7 Lab - Exploratory Data Analysis (EDA)

## Scenario

The PaySprint card-payments team has one month of card transactions and no settled view of what
is in them. Before anyone builds fraud rules or reports, they want an exploratory pass: how
payment amounts are distributed, where the money goes, which channels and times of day are
declined or defrauded most, and whether any simple total in the data is misleading. Your output
is a short set of findings and one hypothesis that the fraud team can test formally in Module 8.

## Objectives

By the end of this lab you will have:

- Described a skewed distribution with `describe()` and chosen between the mean and the median
- Segmented spend by category with counts, totals and shares of the total
- Calculated rates (decline rate, fraud rate) from boolean columns with `groupby().mean()` and
  `pd.crosstab(..., normalize="index")`
- Binned a numeric column into labelled bands with `pd.cut`
- Found and quantified a data anomaly that a naive total hides
- Written one pattern, one anomaly and one specific, checkable hypothesis

## Setup

- `pip install pandas`
- Data: `shared/transactions.csv` and `shared/fx_rates.csv` (in the repo's `shared/` folder)
- Starter file: `starter_eda_payments.py`, in `labs/07-eda/`. It loads both files. Run it with
  `python starter_eda_payments.py` from any folder.

## The data

`transactions.csv` has 140 card transactions from Mon 2 Feb to Sun 1 Mar 2026. The columns used
here:

| Column | Meaning |
| --- | --- |
| `txn_timestamp` | date and time of the payment |
| `merchant_category` | one of 8 categories, e.g. Groceries, Travel, Electronics |
| `channel` | `Online`, `In-store` or `Contactless` |
| `currency`, `amount` | the amount is in this currency: GBP (pounds sterling), EUR (euro) or USD (US dollar) |
| `status` | `APPROVED` or `DECLINED` |
| `is_fraud` | 1 if the fraud team confirmed the transaction as fraud, else 0 |

`fx_rates.csv` gives `rate_to_gbp` per currency (FX, foreign exchange): GBP 1.00, EUR 0.85,
USD 0.79.

## Task

Work through the TODOs in the starter file. Print each result, and write your interpretation as
a comment below the code that produces it.

1. **Derived columns.** Merge the FX rates onto the transactions and add `amount_gbp`
   (`amount * rate_to_gbp`, rounded to 2 decimal places). Add `hour` and `weekday` from
   `txn_timestamp` with the `.dt` accessor.
2. **Distribution.** Print `amount_gbp.describe(percentiles=[0.5, 0.9, 0.99])`. In a comment,
   compare the mean with the median, say what the gap and the 90th/99th percentiles tell you
   about the shape, and state which of mean or median you would report as a typical payment.
3. **Spend by merchant category.** Build one table with `txn_count`, `total_gbp` and
   `share_pct` (share of total GBP spend, in %) per `merchant_category`, sorted by `total_gbp`
   descending. Comment on which categories are frequent and which carry the money.
4. **Decline rate by channel.** Add a boolean column `declined`. Calculate the decline rate per
   channel with `groupby("channel")["declined"].mean()` (show the count and number of declines
   alongside). Then produce the same view with
   `pd.crosstab(txns["channel"], txns["status"], normalize="index")`. The demo used `crosstab`
   for counts; here you use it for proportions within each row.
5. **Hour bands.** Use `pd.cut` on `hour` to create `hour_band` with the labels
   `Night 00-05`, `Morning 06-11`, `Afternoon 12-17` and `Evening 18-23`. Check your bin edges:
   by default `pd.cut` includes the right edge of each bin and excludes the left. For each band,
   print the transaction count, decline rate and fraud rate.
6. **The currency anomaly.** Print `amount.sum()`, `amount_gbp.sum()` and the difference. Then
   break the difference down by currency, and say in a comment which rows cause it.
7. **Findings.** As comments, one sentence each, with a number from your output in each:
   - **one pattern** (something consistent across a segment)
   - **one anomaly** (something that is wrong or would mislead)
   - **one hypothesis** that is specific and checkable, and names the Module 8 test that would
     check it. Example: "Online transactions are declined more often than card-present
     (In-store and Contactless) transactions, and the difference is larger than chance would
     explain; testable with a chi-square test of independence on channel x declined."
     "Online seems riskier" is an observation, not a hypothesis.

## Acceptance criteria

- The script runs with `python starter_eda_payments.py` from any folder with no errors or
  warnings.
- Step 2: mean 129.18, median (50%) 39.75, 90th percentile 295.33, 99th percentile 1,300.61,
  max 2,145.31; the comment recommends the median and explains why.
- Step 3: Electronics is first with 9 transactions and 36.9% of GBP spend, Travel second with
  26.0%; Transport has the most transactions (37). The shares add up to 100%.
- Step 4: decline rates Online 15.5% (11 of 71), In-store 4.2% (1 of 24), Contactless 2.2%
  (1 of 45), from both methods.
- Step 5: band counts Night 10, Morning 38, Afternoon 44, Evening 48; the Night band has a
  fraud rate of 100% and a decline rate of 60%.
- Step 6: raw total 20,762.64 against a GBP total of 18,084.88, a difference of 2,677.76
  (EUR 753.63, USD 1,924.13, GBP 0.00).
- Step 7: the three findings are present, each contains a number, and the hypothesis could be
  confirmed or rejected with a named statistical test.

## Extension exercises

1. **Pareto check.** Calculate the share of approved GBP spend that comes from the top 20% of
   customers.
   Sum approved `amount_gbp` per customer, sort descending, and add a cumulative share column
   with `cumsum()`. Decide how to turn "20% of 12 customers" into a whole number and say why.
   Done: the table with cumulative shares is printed, and one line names the top customers and
   their combined share.
2. **Weekday vs weekend.** Compare mean daily spend and mean daily transaction count for
   weekdays and weekends. Aggregate to one row per calendar day first (`resample("D")`), then
   average the days. Done: both per-day averages are printed next to the per-transaction mean
   for each group, with a comment explaining why averaging transactions answers a different
   question from "is a weekend day busier?".
3. **Per-customer anomalies.** Flag transactions greater than 5 times that customer's median
   `amount_gbp`, using `groupby("customer_id")["amount_gbp"].transform("median")`. Done: the
   flagged rows are printed with the customer median and the ratio, together with how many
   flagged rows are fraud, how many of the 12 fraud rows the rule catches, and which fraud rows
   it misses and why.
4. **Domestic vs foreign fraud.** Merge `shared/customers.csv` to get each customer's
   `home_country` (a preview of Module 9), and compare the fraud rate for transactions in the
   customer's home country with the rest. Use `indicator=True` on the merge. Done: the fraud
   rate is printed for each group, customer K012 is handled explicitly (check what the merge
   gives for K012), and a comment explains why `country != "GB"` is the wrong test for
   "foreign".
