from pathlib import Path
import numpy as np
import pandas as pd

SHARED = Path(__file__).resolve().parents[2] / "shared"

txns = pd.read_csv(SHARED / "transactions.csv")
fx = pd.read_csv(SHARED / "fx_rates.csv")
txns = txns.merge(fx, on="currency", how="left", validate="many_to_one")
txns["amount_gbp"] = (txns["amount"] * txns["rate_to_gbp"]).round(2)

fraud = txns.loc[txns["is_fraud"] == 1, "amount_gbp"].to_numpy()
legit = txns.loc[txns["is_fraud"] == 0, "amount_gbp"].to_numpy()
observed = np.median(fraud) - np.median(legit)

# Bootstrap: resample each group WITH replacement, at its own size, and recompute the statistic.
# Resampling the groups separately keeps 12 fraud and 128 non-fraud rows in every resample.
rng = np.random.default_rng(42)
N_RESAMPLES = 5000
diffs = np.empty(N_RESAMPLES)
for i in range(N_RESAMPLES):
    fraud_sample = rng.choice(fraud, size=len(fraud), replace=True)
    legit_sample = rng.choice(legit, size=len(legit), replace=True)
    diffs[i] = np.median(fraud_sample) - np.median(legit_sample)

low, high = np.percentile(diffs, [2.5, 97.5])
print(f"observed difference in median amount_gbp (fraud - non-fraud): {observed:,.2f}")
print(f"bootstrap 95% CI ({N_RESAMPLES} resamples, percentile method): {low:,.2f} to {high:,.2f}")
print(f"bootstrap standard error: {diffs.std(ddof=1):,.2f}")
# The interval runs from about 320 to about 1,100 GBP. It excludes 0, which agrees with the
# Mann-Whitney result: fraud payments are larger. The interval is wide, and most of that width
# comes from the fraud group: with only 12 values, the median of a resample jumps between a few
# neighbouring values (the fraud amounts are 1.00, 1.50, then several hundred GBP upwards).
# The CI describes sampling uncertainty only; it cannot fix a sample that is unrepresentative.
