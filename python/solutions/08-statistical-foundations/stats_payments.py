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

# --- 1. Distribution shape ---
amount = txns["amount_gbp"]
log_amount = np.log1p(amount)
print("\n1. Distribution shape")
print(f"skew of amount_gbp:        {amount.skew():.2f}")
print(f"skew of log1p(amount_gbp): {log_amount.skew():.2f}")
print(f"mean amount_gbp:   {amount.mean():,.2f}")
print(f"median amount_gbp: {amount.median():,.2f}")
# A skew of 4.20 is a very long right tail: most payments are small (coffee, travel cards,
# groceries) and a handful of large Electronics/Travel payments stretch the range to 2,145.31.
# Those few large values pull the mean (129.18) to more than three times the median (39.75),
# so the mean is a poor "typical payment". log1p compresses large values far more than small
# ones (1 -> 0.69, 40 -> 3.71, 2,000 -> 7.60), which brings the skew down to 0.41, close to
# symmetric. log1p is used instead of log so that an amount of 0 would map to 0, not -infinity.
# Working on the log scale is useful for charts, and for methods that assume a roughly
# symmetric shape.

# --- 2. Pearson and Spearman correlation ---
distance = txns["distance_from_home_km"]
pearson_r, pearson_p = stats.pearsonr(amount, distance)
spearman_rho, spearman_p = stats.spearmanr(amount, distance)
print("\n2. amount_gbp vs distance_from_home_km")
print(f"Pearson  r   = {pearson_r:.2f}, p = {pearson_p:.1e}")
print(f"Spearman rho = {spearman_rho:.2f}, p = {spearman_p:.3f}")
# Pearson r = 0.66 with p far below 0.05: a strong linear association that is very unlikely
# to be chance. Spearman rho = 0.20 (p = 0.019): still statistically significant at 0.05, but
# weak. The difference is the point: Pearson works on the raw values, so a few rows that are
# both very large and very far from home (the foreign Electronics/Travel fraud and K007's
# 1,202.97 flight, all 5,000+ km and 1,000+ GBP) dominate it. Spearman works on ranks, so
# each of those rows counts no more than any other row, and it is robust to extreme values.
# Across the bulk of transactions, larger payments are only slightly more likely to be further
# from home. With skewed data, report Spearman, or at least both.

# --- 3. Correlation and causation ---
far = distance > 300
print("\n3. Distance and fraud")
print(f"fraud rate, > 300 km from home:  {txns.loc[far, 'is_fraud'].mean():.1%} "
      f"({txns.loc[far, 'is_fraud'].sum()} of {far.sum()})")
print(f"fraud rate, <= 300 km from home: {txns.loc[~far, 'is_fraud'].mean():.1%} "
      f"({txns.loc[~far, 'is_fraud'].sum()} of {(~far).sum()})")
far_legit = txns[far & (txns["is_fraud"] == 0)]
print("legitimate far-from-home transactions by customer:")
print(far_legit.groupby(["customer_id", "country"]).size().to_string())
# Distance is strongly associated with fraud (45.0% fraud beyond 300 km, 2.5% within),
# but distance does not cause fraud. The common cause is how card fraud happens: stolen card
# details are mostly used card-not-present (online) by criminals located abroad, so the fraud
# shows up as "far from home" because of where the fraudster is. Distance is a symptom of that
# mechanism. Legitimate travel produces the same distance: 11 of the 20 far-from-home rows are
# genuine, K004 on holiday in Spain (7 rows) and K007 on a US business trip (4 rows). A rule
# that blocks on distance alone would decline those customers. Conversely, 3 fraud rows are
# within 300 km (the K009 card-testing payments at 0 km and the K011 cloned card in the UK),
# so distance is neither necessary nor sufficient.

# --- 4. Chi-square test of independence: channel x declined ---
txns["declined"] = txns["status"] == "DECLINED"
channel_table = pd.crosstab(txns["channel"], txns["declined"])
chi2, chi_p, dof, expected = stats.chi2_contingency(channel_table)
print("\n4. Chi-square: channel x declined")
print(channel_table)
print(f"chi2 = {chi2:.2f}, p = {chi_p:.3f}, dof = {dof}")
expected_df = pd.DataFrame(expected, index=channel_table.index, columns=channel_table.columns)
print("expected frequencies if channel and decline were independent:")
print(expected_df.round(2))
low_cells = (expected < 5).sum()
print(f"cells with expected count < 5: {low_cells} of {expected.size}")
# p = 0.036 < 0.05: evidence that decline rate depends on channel (Online 11/71 declined,
# against 1/45 Contactless and 1/24 In-store). The chi-square p-value is an approximation that
# assumes the expected count in each cell is reasonably large; the usual rule of thumb is no
# more than 20% of cells with an expected count below 5 (and none below 1). Here 2 of 6 cells
# (33%) are below 5 (Contactless/declined 4.18, In-store/declined 2.23), so the approximation
# is unreliable and this p-value should be treated as indicative only. Fisher's exact test (Extension 3) avoids the problem.

# --- 5. Mann-Whitney U and Welch t-test: fraud vs non-fraud amount ---
fraud_amounts = txns.loc[txns["is_fraud"] == 1, "amount_gbp"]
legit_amounts = txns.loc[txns["is_fraud"] == 0, "amount_gbp"]
print("\n5. amount_gbp, fraud vs non-fraud")
print(f"fraud:     n = {len(fraud_amounts)}, median = {fraud_amounts.median():,.2f}, "
      f"mean = {fraud_amounts.mean():,.2f}")
print(f"non-fraud: n = {len(legit_amounts)}, median = {legit_amounts.median():,.2f}, "
      f"mean = {legit_amounts.mean():,.2f}")
u_stat, u_p = stats.mannwhitneyu(fraud_amounts, legit_amounts, alternative="two-sided")
t_stat, t_p = stats.ttest_ind(fraud_amounts, legit_amounts, equal_var=False)
print(f"Mann-Whitney U = {u_stat:.0f}, p = {u_p:.5f}")
print(f"Welch t-test   t = {t_stat:.2f}, p = {t_p:.4f}")
# Both tests reject "no difference" at 0.05 (Mann-Whitney p = 0.00021, Welch p = 0.0020).
# Mann-Whitney is the more appropriate test here: it compares ranks, so it makes no assumption
# about the shape of the distribution and is not dragged around by the 2,145.31 payment. The
# Welch t-test compares means and relies on the sample means being approximately normal; with
# a skew of 4.20 and only 12 fraud rows that assumption is doubtful, and the fraud group's
# large spread (1.00 to 2,145.31) inflates its standard error, which is why its p-value is
# about ten times larger. The two tests also answer slightly different questions (a difference
# in means against a general shift in the distribution), so they need not agree.
# Caveat: 12 fraud rows is a very small sample, including two tiny card-testing payments
# (1.00 and 1.50). One or two different fraud cases could move these results a long way,
# and the fraud cases were chosen by what the fraud team confirmed, which may not be
# representative of all fraud.
