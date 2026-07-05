# Module 13 Lab — Model Answer Notes

See `predictive.py`. Verified results against `shared/trades.csv`:

- Model MAE ≈ 16,513, RMSE ≈ 19,507. Baseline (always predict the training mean) MAE ≈ 15,630,
  RMSE ≈ 18,357. The trained model is **worse** than the naive baseline.
- All three rows where `quantity * price != value` (T0003, T0009, T0017) are Bond trades. Every
  other asset class in the dataset satisfies `value = quantity * price` exactly.
- The actual Bond relationship is `value = quantity * price / 100` — a standard bond-market
  convention (price quoted per 100 of face value), not a data error.

Key points to check in a delegate's solution:

- **The investigation must actually run the row-by-row comparison**, not just assert "the model
  isn't great" without finding the specific rows and the specific asset class responsible.
- **The explanation must name the mechanism** (bonds priced per 100 face value), not just say
  "bonds are different" without saying how.
- **The plain-English paragraph must explicitly compare model MAE to baseline MAE with the real
  numbers**, and correctly conclude the model isn't yet useful — a delegate who reports the MAE
  without the baseline comparison, or claims the model is "good" without checking, has missed the
  point of Module 13's evaluation objective.
- **This lab's result is intentionally not tidy.** It exists specifically to demonstrate that
  small-sample models can underperform a trivial baseline, and that investigating *why* (rather
  than accepting a disappointing metric at face value) is where the real understanding comes
  from — a genuinely useful, unplanned discovery in this dataset, not a scripted "aha" moment.
