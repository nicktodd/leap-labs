# Module 8 Lab - Statistical Foundations

## Scenario

The PaySprint card-payments fraud team wants evidence, not impressions. Before they change any
fraud rules, they have asked you to test a few beliefs about last month's card transactions:
that fraud payments are larger, that fraud happens far from home, and that some channels are
declined more often than others. Each answer must say how strong the evidence is and what it
does not prove.

## Objectives

By the end of this lab you will have:

- Described a skewed distribution with skew, mean and median, and seen what a log transform
  does to it
- Calculated and compared Pearson and Spearman correlation coefficients, interpreting both the
  coefficient and the p-value
- Explained, with evidence from the data, why an association does not establish causation
- Run a chi-square test of independence on a contingency table and checked its assumptions
- Compared two groups with a non-parametric test (Mann-Whitney U) and a Welch t-test, and
  chosen between them

## Setup

- `pip install pandas numpy scipy`
- Data: `shared/transactions.csv` and `shared/fx_rates.csv` (in the repo's `shared/` folder)
- Starter file: `starter_stats_payments.py`, in `labs/08-statistical-foundations/`. It already
  loads both files and adds an `amount_gbp` column. Run it with
  `python starter_stats_payments.py` from any folder.

## The data

`transactions.csv` has 140 card transactions from 2 Feb to 1 Mar 2026. The columns used here:

| Column | Meaning |
| --- | --- |
| `amount_gbp` | added by the starter: `amount` converted to GBP using `fx_rates.csv` (FX, foreign exchange) |
| `distance_from_home_km` | distance between the transaction location and the customer's home |
| `channel` | `Online`, `In-store` or `Contactless` |
| `status` | `APPROVED` or `DECLINED` |
| `is_fraud` | 1 if the fraud team confirmed the transaction as fraud, else 0 |

## Task

Write each interpretation as a comment directly below the code that produces the numbers. An
interpretation says what the numbers mean for PaySprint; repeating the number is not enough.

1. **Distribution shape.** Print the skew of `amount_gbp` and the skew of
   `np.log1p(amount_gbp)`, and the mean and median of `amount_gbp`. In a comment, describe the
   shape, explain why the mean and median differ so much, say what the log transform does to
   the long right tail, and why `log1p` is used rather than `log`.
2. **Pearson and Spearman.** Use `scipy.stats.pearsonr` and `scipy.stats.spearmanr` to
   correlate `amount_gbp` with `distance_from_home_km`. Print both coefficients and both
   p-values. Interpret each coefficient together with its p-value, then explain why the two
   coefficients are so different. (Hint: Spearman correlates ranks.)
3. **Correlation and causation.** Print the fraud rate for transactions more than 300 km from
   home, and for the rest. Then list the far-from-home transactions that are not fraud, by
   customer and country. Distance is clearly associated with fraud. In a comment, answer: does
   distance cause fraud? Name the underlying explanation, and use the legitimate
   far-from-home customers you found as evidence.
4. **Chi-square test of independence.** Build a contingency table of `channel` (rows) against
   declined / not declined (columns) with `pd.crosstab`. Run `scipy.stats.chi2_contingency` and
   print the statistic, p-value, degrees of freedom and the expected frequencies it returns.
   Interpret the p-value, then count the cells with an expected frequency below 5 and state
   what that means for the reliability of the test.
5. **Comparing two groups.** Split `amount_gbp` into fraud and non-fraud. Print the size,
   median and mean of each group. Run `scipy.stats.mannwhitneyu` (two-sided) and
   `scipy.stats.ttest_ind(..., equal_var=False)` (a Welch t-test, which does not assume equal
   variances). In a comment, say which test is more appropriate for this data and why, why the
   two p-values differ, and what caveat the size of the fraud group requires.

## Acceptance criteria

- The script runs with `python starter_stats_payments.py` with no errors or warnings.
- Step 1 prints a skew of about 4.20 for `amount_gbp` and about 0.41 after `log1p`; mean about
  129.18 and median about 39.75.
- Step 2 prints Pearson r of about 0.66 and Spearman rho of about 0.20, each with its p-value,
  and the comment explains the difference in terms of ranks and extreme values.
- Step 3 shows 9 of 20 far-from-home transactions are fraud, identifies the 11 legitimate ones
  (customers K004 and K007), and the comment reaches a specific conclusion about causation.
- Step 4 prints chi2 of about 6.66 with p of about 0.036 and 2 degrees of freedom, shows the
  expected frequencies, and the comment notes that 2 of the 6 cells have expected counts
  below 5.
- Step 5 prints both test results (the fraud group has 12 rows) and the comment names the
  more appropriate test with a reason, plus a small-sample caveat that refers to this data.

## Extension exercises

1. **Bootstrap confidence interval.** Estimate a 95% CI (confidence interval) for the
   difference in median `amount_gbp` between fraud and non-fraud transactions by
   bootstrapping: use `np.random.default_rng(42)`, draw 5,000 resamples of each group with
   replacement (each at its own group size), and take the 2.5th and 97.5th percentiles of the
   differences. Done: the observed difference and the interval are printed, and a comment says
   whether the interval includes 0 and why it is so wide.
2. **Permutation test by hand.** Compute the difference in decline rate between Online and
   card-present (In-store plus Contactless) transactions. Shuffle the declined labels 10,000
   times (`rng.permutation`, seed 42), recompute the difference each time, and estimate a
   two-sided p-value as the share of shuffles at least as extreme as the observed difference.
   Done: your p-value is printed next to the chi-square p-values for the same 2x2 table (with
   Yates' continuity correction, the default, and with `correction=False`) and the core
   3-channel test, with a comment comparing them.
3. **Fisher's exact test.** Build the 2x2 table (Online vs card-present) x (declined vs not)
   and run `scipy.stats.fisher_exact`. Done: the odds ratio and p-value are printed, and a
   comment explains why Fisher's exact test suits tables with small expected counts and how
   its p-value compares with the chi-square result.
4. **Effect size.** Compute Cramer's V from the core chi-square statistic:
   `sqrt(chi2 / (n * (min(rows, cols) - 1)))`, and check it against
   `scipy.stats.contingency.association`. Then multiply the contingency table by 10 and rerun
   the test. Done: both V values and both p-values are printed, and a comment explains why a
   p-value alone does not describe the strength of an association.
