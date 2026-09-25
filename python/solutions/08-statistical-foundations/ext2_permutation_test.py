from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

SHARED = Path(__file__).resolve().parents[2] / "shared"
txns = pd.read_csv(SHARED / "transactions.csv")

online = (txns["channel"] == "Online").to_numpy()
declined = (txns["status"] == "DECLINED").to_numpy()


def rate_difference(declined_flags):
    """Decline rate for Online minus decline rate for card-present (In-store + Contactless)."""
    return declined_flags[online].mean() - declined_flags[~online].mean()


observed = rate_difference(declined)
print(f"Online decline rate:       {declined[online].mean():.1%} ({declined[online].sum()} of {online.sum()})")
print(f"card-present decline rate: {declined[~online].mean():.1%} ({declined[~online].sum()} of {(~online).sum()})")
print(f"observed difference:       {observed:.1%}")

# Null hypothesis: channel makes no difference to declines. If so, the DECLINED labels could be
# shuffled across rows without changing anything, so shuffle them many times and see how often a
# difference at least as large as the observed one appears by chance (two-sided: use abs).
rng = np.random.default_rng(42)
N_PERMUTATIONS = 10_000
null_diffs = np.array([rate_difference(rng.permutation(declined)) for _ in range(N_PERMUTATIONS)])
perm_p = np.mean(np.abs(null_diffs) >= abs(observed) - 1e-12)  # tolerance for float equality
print(f"\npermutation p-value ({N_PERMUTATIONS} shuffles): {perm_p:.4f}")

# Compare with chi-square on the same 2x2 table, with and without Yates' continuity correction,
# and with the 3-channel chi-square from the core task.
table = pd.crosstab(online, declined)
p_yates = stats.chi2_contingency(table).pvalue
p_no_correction = stats.chi2_contingency(table, correction=False).pvalue
p_three_channels = stats.chi2_contingency(pd.crosstab(txns["channel"], declined)).pvalue
print(f"chi-square 2x2, Yates-corrected:    p = {p_yates:.4f}")
print(f"chi-square 2x2, no correction:      p = {p_no_correction:.4f}")
print(f"chi-square 3 channels (core task):  p = {p_three_channels:.4f}")
# The permutation test makes no large-sample approximation: its null distribution is built from
# this data. Its p-value (about 0.018) sits between the uncorrected chi-square (0.010), which
# tends to understate p for small tables, and the Yates-corrected value (0.023), which is known
# to be conservative. All three agree on the conclusion at the 0.05 level: Online
# payments are declined more often than card-present payments.
