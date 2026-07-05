# Module 8 Lab — Statistical Foundations

## Objectives

By the end of this lab you will have:

- Described a distribution's shape using skew, not just mean and median
- Calculated a correlation coefficient between two variables and interpreted it correctly
- Run a hypothesis test and interpreted the result, including its limitations

## Setup

- `pip install pandas scipy`
- `shared/trades.csv` (repo root)

## Task

Starter file: `starter_stats.py`, in `labs/08-statistical-foundations/`.

1. Calculate the skew of `quantity` and `value`. In a comment, say what the sign and size of each
   tells you about the shape of that column's distribution.
2. Calculate the Pearson correlation (`scipy.stats.pearsonr`) between `quantity` and `value`.
   Interpret both the correlation coefficient **and** the p-value in a comment — don't just print
   the numbers.
3. As a group (or with your partner), discuss: even if this correlation had been strong, would
   that prove one variable causes the other? Write your discussion's conclusion as a comment.
4. Run a two-sample t-test (`scipy.stats.ttest_ind`) comparing `value` for BUY trades against
   `value` for SELL trades — the same comparison Module 7's demo set up as a hypothesis.
   Interpret the p-value against the conventional 0.05 threshold, **and** note the caveat: with
   only 6 SELL trades in this dataset, how much should this result actually be trusted?

## Acceptance criteria

- The script runs with `python starter_stats.py` and produces no errors.
- Skew values for both `quantity` and `value` are printed, with a comment interpreting each.
- The correlation between `quantity` and `value` is printed with both `r` and the p-value, and a
  comment interprets what they mean together (not just "printed the numbers").
- Your causation discussion conclusion is written as a comment — a specific answer to "would a
  strong correlation here prove causation," not a restatement of the question.
- The t-test result is printed and interpreted against a 0.05 threshold, with an explicit caveat
  about the small SELL sample size.
