from pathlib import Path
import pandas as pd

SHARED = Path(__file__).resolve().parents[2] / "shared"

txns = pd.read_csv(SHARED / "transactions.csv")
fx = pd.read_csv(SHARED / "fx_rates.csv")
txns = txns.merge(fx, on="currency", how="left", validate="many_to_one")
txns["amount_gbp"] = (txns["amount"] * txns["rate_to_gbp"]).round(2)
spend = txns[txns["status"] == "APPROVED"]

pivot = spend.pivot_table(index="merchant_category", columns="channel", values="amount_gbp",
                          aggfunc="sum", fill_value=0)  # no margins: they are not data

# melt turns the wide table back into one row per (category, channel) pair.
long = (pivot.reset_index()
        .melt(id_vars="merchant_category", var_name="channel", value_name="amount_gbp"))
print(f"long form: {len(long)} rows ({pivot.shape[0]} categories x {pivot.shape[1]} channels)")
print(long.head(6))

# fill_value=0 created rows for combinations that never occurred. Drop them so that the long
# form describes the data rather than the shape of the pivot.
long_nonzero = long[long["amount_gbp"] != 0]
print(f"non-zero combinations: {len(long_nonzero)}")

# Verify: the long-form totals match the source data, overall and per channel.
direct = spend.groupby("channel")["amount_gbp"].sum()
from_long = long.groupby("channel")["amount_gbp"].sum()
check = pd.DataFrame({"from_source": direct, "from_melt": from_long}).round(2)
print(check)
print(f"overall: source {spend['amount_gbp'].sum():,.2f}, melted {long['amount_gbp'].sum():,.2f}")
assert (check["from_source"] - check["from_melt"]).abs().max() < 0.005

# The same check with margins=True left on shows why margins must be dropped before melting.
with_margins = spend.pivot_table(index="merchant_category", columns="channel",
                                 values="amount_gbp", aggfunc="sum", fill_value=0,
                                 margins=True, margins_name="Total")
bad_long = with_margins.reset_index().melt(id_vars="merchant_category", value_name="amount_gbp")
print(f"melted WITH margins: {bad_long['amount_gbp'].sum():,.2f} (4x the true total)")
