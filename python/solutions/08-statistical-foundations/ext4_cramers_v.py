from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats.contingency import association

SHARED = Path(__file__).resolve().parents[2] / "shared"
txns = pd.read_csv(SHARED / "transactions.csv")


def cramers_v(table):
    """Cramer's V = sqrt(chi2 / (n * (min(rows, cols) - 1))), between 0 (none) and 1 (perfect)."""
    chi2 = stats.chi2_contingency(table, correction=False).statistic
    n = table.to_numpy().sum()
    return np.sqrt(chi2 / (n * (min(table.shape) - 1)))


channel_table = pd.crosstab(txns["channel"], txns["status"] == "DECLINED")
chi = stats.chi2_contingency(channel_table)
v = cramers_v(channel_table)
print(f"channel x declined: chi2 = {chi.statistic:.2f}, p = {chi.pvalue:.3f}, Cramer's V = {v:.3f}")
print(f"scipy check: association(method='cramer') = {association(channel_table, method='cramer'):.3f}")

# A table with the same proportions but 10 times as many rows: V is unchanged, p collapses.
scaled = channel_table * 10
chi_scaled = stats.chi2_contingency(scaled)
print(f"same proportions x10: chi2 = {chi_scaled.statistic:.2f}, p = {chi_scaled.pvalue:.1e}, "
      f"Cramer's V = {cramers_v(scaled):.3f}")
# Cramer's V of 0.218 is a small-to-moderate association (for a table with one degree of freedom
# in its smaller dimension, 0.1 is often read as small, 0.3 as medium, 0.5 as large).
# The p-value measures how surprising the data would be if there were no association, and it
# depends heavily on sample size: the x10 table has exactly the same pattern and the same V, but
# a far smaller p. A p-value alone therefore says nothing about how strong the relationship is;
# report an effect size alongside it. For a 3x2 table scipy's chi2_contingency applies no
# continuity correction, so V computed from the core-task statistic gives the same value.
