from pathlib import Path
import pandas as pd
from scipy import stats

SHARED = Path(__file__).resolve().parents[2] / "shared"
txns = pd.read_csv(SHARED / "transactions.csv")

# 2x2: rows = Online / not Online, columns = declined / not declined.
channel_group = txns["channel"].eq("Online").map({True: "Online", False: "Card-present"})
decline_group = txns["status"].eq("DECLINED").map({True: "Declined", False: "Not declined"})
table = pd.crosstab(channel_group, decline_group)
table = table.loc[["Online", "Card-present"], ["Declined", "Not declined"]]
print(table)

result = stats.fisher_exact(table)
print(f"\nFisher's exact test: odds ratio = {result.statistic:.2f}, p = {result.pvalue:.4f}")

chi = stats.chi2_contingency(table)
print(f"chi-square (Yates):  p = {chi.pvalue:.4f}")
print("expected frequencies:")
print(pd.DataFrame(chi.expected_freq, index=table.index, columns=table.columns).round(2))
# Fisher's exact test computes the p-value directly from the hypergeometric distribution (every
# table with the same row and column totals), so it does not rely on large expected counts.
# That makes it the right test for small tables where expected counts are low. Here p = 0.0169:
# Online payments have about 6 times the odds of being declined (11/60 against 2/67). Collapsing
# to 2x2 also lifts the smallest expected count to 6.41, but with only 13 declines in total,
# Fisher is still the safer choice.
