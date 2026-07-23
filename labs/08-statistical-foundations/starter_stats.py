"""Lab 08: Statistical foundations — skew, correlation, and t-test."""

from pathlib import Path
import pandas as pd
from scipy import stats

DATA_PATH = Path(r"C:\Users\zackt\Documents\fidelity-leap-sprint4\shared\trades.csv")
df = pd.read_csv(DATA_PATH)

# 1. Skew of quantity and value
qty_skew = df["quantity"].skew()
val_skew = df["value"].skew()
print(f"Skew of quantity: {qty_skew:.4f}")
print(f"Skew of value:    {val_skew:.4f}")
# Comment: quantity skew is large and positive — the distribution has a long right tail, meaning
# most trades are small-to-mid quantity but a few very large trades (e.g. bond notionals of 5000)
# pull the mean well above the median. value skew is also positive for the same reason — a
# handful of high-value trades (AAPL at $37,510, VUSA at $25,266) stretch the right tail.

# 2. Pearson correlation between quantity and value
r, p = stats.pearsonr(df["quantity"], df["value"])
print(f"\nPearson r(quantity, value): {r:.4f}, p-value: {p:.4f}")
# Comment: r is weakly positive at best, and the p-value is well above 0.05, so we cannot
# reject the null hypothesis that there is no linear relationship between quantity and value
# in this dataset. This is surprising but explained by the fact that bond trades use large
# notional quantities at sub-$100 prices, while crypto uses tiny quantities at $42,000 each —
# quantity alone is not a reliable predictor of value across different asset classes.

# 3. Causation discussion
# Comment: even if the correlation between quantity and value had been strong (r ~ 1),
# it would NOT prove causation. Value is arithmetically derived from quantity * price, so any
# correlation here is definitional rather than causal — price is the confounding third variable.
# More generally, correlation shows association but cannot rule out reverse causality or confounders.

# 4. Two-sample t-test: BUY value vs. SELL value
buy_values = df.loc[df["side"] == "BUY", "value"]
sell_values = df.loc[df["side"] == "SELL", "value"]
t_stat, p_val = stats.ttest_ind(buy_values, sell_values)
print(f"\nt-test BUY vs SELL value: t={t_stat:.4f}, p={p_val:.4f}")
print(f"BUY  n={len(buy_values)}, mean=${buy_values.mean():,.2f}")
print(f"SELL n={len(sell_values)}, mean=${sell_values.mean():,.2f}")
# Comment: p > 0.05, so we do not have statistically significant evidence that BUY and SELL
# trades differ in mean value at the 5% level. HOWEVER, there are only 6 SELL trades in this
# dataset — a t-test with n=6 in one group has very low statistical power, meaning the test
# is unlikely to detect a real difference even if one exists. This result should not be trusted
# as a meaningful finding; a much larger dataset would be needed to draw conclusions.
