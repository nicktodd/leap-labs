# Module 7 Lab - Model Answer Notes

See `eda_payments.py` for the core solution and `ext1_pareto.py` to `ext4_foreign_fraud.py` for
the extensions.

## Verified results

Output of `python eda_payments.py`:

- 140 transactions, 02 Feb 2026 to 01 Mar 2026.
- `amount_gbp.describe()`: mean 129.18, std 291.75, min 1.00, median 39.75, 90th percentile
  295.33, 99th percentile 1,300.61, max 2,145.31.
- Spend by category (count, GBP total, share): Electronics 9, 6,680.95, 36.9%; Travel 6,
  4,704.40, 26.0%; Retail 24, 2,942.37, 16.3%; Groceries 26, 1,336.59, 7.4%; Transport 37,
  1,315.64, 7.3%; Dining 26, 657.81, 3.6%; Fuel 6, 378.18, 2.1%; Subscriptions 6, 68.94, 0.4%.
- Decline rate by channel: Online 11 of 71 (0.155), In-store 1 of 24 (0.042), Contactless 1 of
  45 (0.022). The `crosstab` with `normalize="index"` shows the same values in its `DECLINED`
  column.
- Hour bands (count, decline rate, fraud rate): Night 10, 0.600, 1.000; Morning 38, 0.000,
  0.000; Afternoon 44, 0.068, 0.023; Evening 48, 0.083, 0.021.
- Currency anomaly: `amount.sum()` 20,762.64, `amount_gbp.sum()` 18,084.88, difference
  2,677.76. By currency: EUR 20 rows, 5,024.15 raw vs 4,270.52 GBP (753.63); GBP 112 rows,
  difference 0.00; USD 8 rows, 9,162.52 raw vs 7,238.39 GBP (1,924.13).

## Key points to check in a delegate's solution

- **All money comparisons use `amount_gbp`.** A delegate who ranks categories by `amount`
  reports Electronics as 7,912.79 instead of 6,680.95 and Travel as 5,709.58 instead of
  4,704.40. Every category except Subscriptions (all GBP) is overstated.
- **The median is recommended as the typical payment**, with the reason: a mean more than three
  times the median, and a 99th percentile far above the 90th, show a long right tail.
- **Count and value are both shown for categories.** The point of Step 3 is that Transport has
  the most transactions but only 7.3% of spend, while Electronics and Travel have 15
  transactions between them and 62.9% of spend.
- **Rates come from the mean of a boolean column**, not from dividing hand-typed counts.
  `groupby("channel")["declined"].mean()` and the `DECLINED` column of the normalised crosstab
  must agree.
- **The `pd.cut` edges are right.** With the default `right=True`, edges `[-1, 5, 11, 17, 23]`
  give 0-5, 6-11, 12-17, 18-23. Edges `[0, 6, 12, 18, 24]` with the default give (0, 6],
  (6, 12] and so on: every boundary hour moves into the earlier band, and the counts become
  16, 50, 45, 29 instead of 10, 38, 44, 48 (the 6 transactions at 06:xx join Night, for
  example). They would also turn any hour-0 transaction into NaN; this data has none, so the
  total still reaches 140 and the mistake is easy to miss. `right=False` with edges
  `[0, 6, 12, 18, 24]` is also correct. Check the counts against the acceptance criteria.
- **The Night finding is stated with its sample size.** All 10 Night transactions are fraud, but
  10 is a small group, and the data contains no legitimate night-time payments. It is a pattern
  to investigate, not a rule.
- **The currency anomaly is quantified and attributed**, not only mentioned: the GBP rows
  contribute nothing to the difference, and the 8 USD rows contribute 1,924.13 of the 2,677.76.
- **The hypothesis names a test and a comparison.** The Online vs card-present decline
  hypothesis hands straight to Module 8, which runs a chi-square test of independence on
  channel x declined (Step 4 of that lab) and a 2x2 Online vs card-present version in its
  extensions. Send back hypotheses such as "Online is riskier" that do not say what would be
  compared or how.

## Extension notes

**E1 - Pareto check.** Using approved transactions only, the top 20% of 12 customers rounds up
to 3 customers: K006 (2,632.04), K004 (2,002.88) and K011 (1,865.67), together 56.7% of approved
GBP spend. The top 4 reach 72.6%. Approved fraud inflates two of the top 3: K006's total
includes the 2,145.31 fraudulent flight (P0094), and K011's includes the 412.54 (P0054) and
780.00 cloned-card (P0136) payments. A good answer notices that "top customer" here partly
means "most defrauded customer", and may repeat the check with `is_fraud == 0`. Pitfalls: including
declined payments (money that did not move), and rounding 2.4 customers down to 2 without saying
so. Either rounding is acceptable if it is stated.

**E2 - Weekday vs weekend.** The period has 20 weekdays and 8 weekend days. Per day: weekdays
average GBP 590.04 and 4.8 transactions, weekends GBP 785.50 and 5.5 transactions. Per
transaction: weekday mean 122.93 (96 transactions), weekend mean 142.82 (44 transactions). Here
both views point the same way, but they answer different questions: the per-transaction mean
measures payment size, the per-day mean measures how much happens on a day. Comparing totals
would favour weekdays because there are 2.5 times as many of them. `resample("D")` is preferred
to grouping on the date because it keeps days with no transactions as zeros.

**E3 - Per-customer anomalies.** 19 transactions exceed 5 times their customer's median; 10 of
them are fraud, which is 10 of the 12 fraud rows. The rule catches K011's cloned card (P0136,
22.6x the median) because it compares with the customer's own history, not a fixed threshold.
It misses K009's card-testing payments (P0043 and P0044, GBP 1.50 and 1.00), which are tiny by
design. The 9 false alarms include K004's Airbnb booking in Spain (P0057), K007's US flight
(P0100) and four K009 rows: K009 has a low median (14.645), so any ordinary purchase looks
extreme. Check that the delegate uses `transform`, not `agg` followed by a manual lookup, and
can explain that `transform` returns a value per row aligned to the original index.

**E4 - Domestic vs foreign fraud.** The left merge gives 130 matched rows and 10 `left_only`
rows, all K012. Domestic: 110 transactions, 3 fraud (0.027). Foreign: 20 transactions, 9 fraud
(0.450). The 11 legitimate foreign transactions are K004 in ES (7) and K007 in US (4). K012
must be a separate group ("Unknown home"): `country != home_country` is True when
`home_country` is NaN, so without handling, all 10 K012 rows are silently counted as foreign.
`country != "GB"` flags 28 rows against 20 truly foreign ones, because it treats K003's spending
in France and K008's in Ireland as foreign.
