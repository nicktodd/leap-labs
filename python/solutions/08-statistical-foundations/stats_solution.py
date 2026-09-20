from pathlib import Path
import pandas as pd
from scipy import stats

DATA_PATH = Path(__file__).resolve().parents[2] / "shared" / "trades.csv"
df = pd.read_csv(DATA_PATH)

# 1. Skew
quantity_skew = df["quantity"].skew()
value_skew = df["value"].skew()
print(f"quantity skew: {quantity_skew:.2f}")
print(f"value skew: {value_skew:.2f}")
# Both are strongly positive (quantity ~2.76, value ~1.42): a long tail of large values
# pulls the mean well above the median in both columns — neither is close to a symmetric,
# "normal-ish" shape, so the mean alone is a misleading single-number summary for either.

# 2. Correlation
r, p = stats.pearsonr(df["quantity"], df["value"])
print(f"\nquantity vs value: r={r:.2f}, p={p:.3f}")
# r is weak-to-moderate and p is above 0.05: not enough evidence, in this 20-row sample,
# of a real relationship between quantity and value. Note this is somewhat expected —
# value = quantity * price, so any relationship is also diluted by price's variation.

# 3. Correlation vs causation discussion
# Conclusion: no. Even a strong correlation would only show that quantity and value tend
# to move together in this sample, never that one causes the other. Both are also
# mechanically linked to price (value = quantity * price), which is a clearer example of
# why "correlated" and "one causes the other" are different claims — here we already know
# the mechanical relationship, and even that doesn't show up as a strong statistical
# correlation, which itself is a useful caution about reading too much into any r value.

# 4. Hypothesis test: BUY vs SELL value
buy_values = df.loc[df["side"] == "BUY", "value"]
sell_values = df.loc[df["side"] == "SELL", "value"]
t_stat, p_value = stats.ttest_ind(buy_values, sell_values, equal_var=False)
print(f"\nBUY mean: {buy_values.mean():,.2f}  SELL mean: {sell_values.mean():,.2f}")
print(f"t-test: t={t_stat:.2f}, p={p_value:.3f}")

if p_value < 0.05:
    print("p < 0.05: conventionally treated as evidence against the null hypothesis")
else:
    print("p >= 0.05: not enough evidence against the null hypothesis")
# Caveat: p is close to 0.05 (borderline), and the SELL group has only 6 trades — a single
# unusually large or small SELL trade could flip this result. Treat it as a starting point
# for a properly powered follow-up analysis, not as a settled conclusion.
