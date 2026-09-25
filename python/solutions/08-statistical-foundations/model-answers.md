# Module 8 Lab - Model Answer Notes

See `stats_payments.py`. Verified results against `shared/transactions.csv` and
`shared/fx_rates.csv` (140 rows, `amount_gbp` rounded to 2 decimal places):

- **Shape:** skew of `amount_gbp` 4.20; skew of `log1p(amount_gbp)` 0.41. Mean 129.18, median
  39.75.
- **Correlation, amount_gbp vs distance_from_home_km:** Pearson r = 0.66 (p = 4.8e-19);
  Spearman rho = 0.20 (p = 0.019).
- **Distance and fraud:** 9 of 20 transactions more than 300 km from home are fraud (45.0%),
  against 3 of 120 within 300 km (2.5%). The 11 legitimate far-from-home rows are K004 in ES
  (7) and K007 in US (4).
- **Chi-square, channel x declined:** chi2 = 6.66, p = 0.036, dof = 2. Observed declines:
  Online 11/71, Contactless 1/45, In-store 1/24. Expected declined counts: Contactless 4.18,
  In-store 2.23, Online 6.59, so 2 of 6 cells are below 5.
- **Fraud vs non-fraud amount_gbp:** fraud n = 12, median 740.63, mean 778.18; non-fraud
  n = 128, median 35.52, mean 68.33. Mann-Whitney U = 1267, p = 0.00021. Welch t = 4.02,
  p = 0.0020.

Key points to check in a delegate's solution:

- **Skew is interpreted as shape.** A good answer links the skew of 4.20 to the mean being more
  than three times the median, and explains that `log1p` compresses large values much more than
  small ones (and handles 0). "Skew is 4.20" alone is not an interpretation.
- **Both correlations are interpreted with their p-values, and the difference is explained.**
  The explanation must mention that Spearman uses ranks, so the handful of large, very distant
  payments dominate Pearson but not Spearman. A delegate who reports only Pearson and calls it
  a "strong relationship" has missed the point of the step.
- **The causation answer is specific to this data.** It should name the mechanism (fraud is
  mostly card-not-present, committed from abroad, so distance reflects where the fraudster is)
  and cite K004's holiday in Spain and K007's US trip as legitimate distance. Bonus: noting
  the 3 fraud rows within 300 km (K009 card testing, K011 cloned card).
- **The chi-square assumption is checked from the returned expected frequencies**, not from
  the observed table. The observed In-store/declined count is 1, but the rule is about the
  expected count (2.23). A delegate who says "p < 0.05 so channel causes declines" should be
  corrected on both the causal wording and the reliability caveat.
- **Mann-Whitney is chosen for a reason**: rank-based, no normality assumption, robust to the
  2,145.31 payment. The small-sample caveat should mention the 12 fraud rows and, ideally, the
  two 1.00 / 1.50 card-testing payments inside that group.
- **`equal_var=False` is present** on the t-test (the groups have very different spreads).

## Extension notes

**E1 Bootstrap CI.** Observed median difference 705.11. With `default_rng(42)` and 5,000
resamples per group the percentile interval is 320.43 to 1,100.73 (bootstrap standard error
194.12). The interval excludes 0, agreeing with Mann-Whitney. Good answers explain the width
through the 12-row fraud group, whose resampled median jumps between a few values. Common
pitfalls: resampling the combined 140 rows instead of each group separately (the group sizes
then vary between resamples), sampling without replacement (which reproduces the original
data every time), and forgetting the seed so the numbers do not match.

**E2 Permutation test.** Online decline rate 15.5% (11 of 71), card-present 2.9% (2 of 69),
difference 12.6 percentage points. With seed 42 and 10,000 shuffles the two-sided p-value is
0.0176. For the same 2x2 table, chi-square gives p = 0.0229 with Yates' correction and
p = 0.0103 without; the core 3-channel test gave 0.0358. All agree at 0.05. Good answers note
that the permutation test builds its null distribution from the data instead of relying on a
large-sample approximation. Pitfalls: shuffling the channel and the declined columns
together (which changes nothing), a one-sided comparison without saying so, and exact float
comparisons that miss ties (the solution uses a small tolerance).

**E3 Fisher's exact test.** Table: Online 11 declined / 60 not; card-present 2 / 67. Odds ratio
6.14, p = 0.0169, very close to the permutation estimate. The 2x2 expected declined counts are
6.59 and 6.41, so the chi-square rule is met here, but with only 13 declines in total Fisher's
exact test is the safer choice. Good answers explain that Fisher computes the probability from
all tables with the same margins (hypergeometric distribution), so it does not need large
expected counts. Pitfall: indexing a crosstab with `[True, False]` column labels, which pandas
treats as a boolean mask; map the booleans to string labels first.

**E4 Cramer's V.** V = 0.218 for the channel x declined table (matches
`association(..., method="cramer")`), a small-to-moderate association. The same table
multiplied by 10 gives chi2 = 66.60, p = 3.5e-15, and exactly the same V. Good answers use this
to show that p depends on sample size while V does not, so a p-value alone cannot describe
strength. Pitfall: computing V from a Yates-corrected 2x2 statistic, which understates V
(pass `correction=False`).
