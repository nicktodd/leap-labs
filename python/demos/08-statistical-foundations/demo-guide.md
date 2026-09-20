# Demo: Module 8 - Statistical Foundations

**Duration:** 20 minutes
**Files:** `stats_demo.py`
**Prerequisite:** `pip install scipy`

## Part 1: Distribution shape (6 min)

Show `df["value"].skew()` (≈1.42) and `df["quantity"].skew()` (≈2.76). Narration: skew near 0
means roughly symmetric (a "normal-ish" shape); a large positive skew means a long tail of large
values pulling the mean above the median - exactly what Module 7's `describe()` output hinted at
when `std` was close to `mean`.

Show a simple text histogram with `pd.cut(df["value"], bins=5).value_counts()`. Narration: 14 of
20 trades sit in the lowest bucket, with a handful of much larger trades stretching the range -
visually, this is a right-skewed distribution, the shape you'd see if you plotted it (Module 10
covers doing that properly).

## Part 2: Correlation, and its limits (7 min)

Run `scipy.stats.pearsonr(df["quantity"], df["price"])` - a weak, not-statistically-significant
correlation (r ≈ -0.15, p ≈ 0.52). Narration: a correlation coefficient close to 0 with a large
p-value means "we can't rule out that this apparent relationship is just noise" - don't narrate
this as "no relationship," narrate it as "not enough evidence of one, in this sample."

Then narrate the classic caution explicitly: **correlation is not causation**. Even a strong
correlation between two variables doesn't tell you one causes the other - both could be driven
by a third factor, or the relationship could be coincidental in a small sample. Ask the room for
their own example of two things that correlate without one causing the other (ice cream sales
and drowning deaths, both driven by summer weather, is the classic one).

## Part 3: Hypothesis-testing intuition (7 min)

Recall Module 7's hypothesis: *"BUY trades are, on average, larger in value than SELL trades in
this book."* Test it properly with `scipy.stats.ttest_ind()`:

```python
t_stat, p_value = stats.ttest_ind(buy_values, sell_values, equal_var=False)
```

Narration, building the intuition without heavy theory: the null hypothesis is "there's no real
difference between BUY and SELL trade values, what we saw is just chance." The p-value
(≈0.049) is the probability of seeing a difference this large (or larger) *if the null hypothesis
were actually true*. A common convention treats p < 0.05 as "unlikely enough to doubt the null
hypothesis" - but stress the caveats: this result is barely under that line, and with only 20
trades (6 of them SELLs), a single unusual trade could flip the conclusion. A "statistically
significant" result from a small sample deserves caution, not certainty.

## Key message

A distribution's shape (via skew) tells you whether "mean" is even a meaningful summary.
Correlation measures association, never causation, and a coefficient near zero or a large
p-value means "not enough evidence," not "proven unrelated." A p-value gives hypothesis testing
a concrete number, but a small sample means that number deserves scepticism, not blind trust.
