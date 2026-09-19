# Module 8 Lab — Model Answer Notes

See `stats_solution.py`. Verified results against `shared/trades.csv`:

- **Skew:** `quantity` ≈ 2.76, `value` ≈ 1.42 — both strongly right-skewed.
- **Correlation:** `quantity` vs. `value`, r ≈ -0.21, p ≈ 0.38 — weak and not statistically
  significant at this sample size.
- **t-test:** BUY vs. SELL `value`, t ≈ 2.12, p ≈ 0.049 — just under the conventional 0.05
  threshold, directly confirming Module 7's hypothesis, with the caveat that it's borderline.

Key points to check in a delegate's solution:

- **Skew interpretation must reference shape, not just repeat the number.** "quantity skew is
  2.76" is not an interpretation; "a long tail of large trades pulls the mean well above the
  median, so mean alone is misleading" is.
- **The correlation interpretation must address both `r` and `p` together**, not just one. A
  delegate who says "r is negative so there's an inverse relationship" without addressing the
  high p-value has missed that the evidence doesn't actually support that claim in this sample.
- **The causation discussion must reach a specific conclusion** ("no, correlation never proves
  causation, and here we even know the mechanical relationship value = quantity * price, which
  doesn't show up as a strong correlation") rather than a generic restatement of "correlation
  isn't causation" with no connection to this dataset.
- **The t-test caveat must name the actual small-sample issue** (only 6 SELL trades), not just
  say "small sample sizes can be unreliable" in the abstract.
