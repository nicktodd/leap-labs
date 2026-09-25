from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

SHARED = Path(__file__).resolve().parents[2] / "shared"

txns = pd.read_csv(SHARED / "transactions.csv")
fx = pd.read_csv(SHARED / "fx_rates.csv")

# Convert every amount to GBP so that amounts in different currencies are comparable.
txns = txns.merge(fx, on="currency", how="left", validate="many_to_one")
txns["amount_gbp"] = (txns["amount"] * txns["rate_to_gbp"]).round(2)

print(f"Loaded {len(txns)} transactions")

# TODO 1 - Distribution shape
# - Print the skew of amount_gbp and the skew of np.log1p(amount_gbp).
# - Print the mean and the median of amount_gbp.
# - Comment: what do the skew and the mean/median gap tell you about the shape?
#   What does the log transform do to the long right tail, and why is that useful?

# TODO 2 - Pearson and Spearman correlation
# - stats.pearsonr and stats.spearmanr between amount_gbp and distance_from_home_km.
# - Print r (or rho) and p for both.
# - Comment: interpret r and p together for each, and explain why the two coefficients differ.

# TODO 3 - Correlation and causation
# - Compare the fraud rate for transactions more than 300 km from home with the rest.
# - Count how many of the far-from-home transactions are NOT fraud, and which customers they
#   belong to.
# - Comment: distance is associated with fraud. Does distance cause fraud? Name the explanation.

# TODO 4 - Chi-square test of independence
# - Build a contingency table: channel (rows) x declined (columns) with pd.crosstab.
# - Run stats.chi2_contingency on it; print the statistic, p-value, degrees of freedom and the
#   expected frequencies.
# - Comment: interpret p, then check the expected frequencies. How many cells are below 5,
#   and what does that mean for the test?

# TODO 5 - Mann-Whitney U and Welch t-test
# - Split amount_gbp into fraud and non-fraud groups (is_fraud).
# - Print the size, median and mean of each group.
# - Run stats.mannwhitneyu and stats.ttest_ind(..., equal_var=False).
# - Comment: which test suits this skewed data better, and why? Why can the two p-values
#   differ? Add a caveat about the size of the fraud group.
