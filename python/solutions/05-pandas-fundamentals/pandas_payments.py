import csv
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SHARED = ROOT / "shared"
TXN_PATH = SHARED / "transactions.csv"
FX_PATH = SHARED / "fx_rates.csv"
# Module 3 writes its plain-Python summary to output/customer_summary.csv (lab or solution
# folder). The comparison below uses it only if it exists.
MODULE3_SUMMARY_CANDIDATES = [
    ROOT / folder / "03-data-structures-file-io" / "output" / "customer_summary.csv"
    for folder in ("labs", "solutions")
]

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 20)

# --- 1. Load with a real datetime column, and inspect ---
# parse_dates converts txn_timestamp at load time, so it is datetime64 rather than text.
df = pd.read_csv(TXN_PATH, parse_dates=["txn_timestamp"])
print(f"Shape: {df.shape}")
print("\nColumn dtypes:")
print(df.dtypes)
print("\ninfo():")
df.info()

# --- 2. Positional selection with .iloc ---
# .iloc works on positions, like list slicing: the end position is excluded.
print("\nRows at positions 10-14 (.iloc[10:15]):")
print(df.iloc[10:15][["txn_id", "merchant", "amount"]])
print("\nLast 3 rows (.iloc[-3:]):")
print(df.iloc[-3:][["txn_id", "merchant", "amount"]])
print("\nFirst 5 rows, columns 0-3 (.iloc[:5, 0:4]):")
print(df.iloc[:5, 0:4])

# --- 3. Label selection with .loc on a txn_id index ---
by_id = df.set_index("txn_id")
print("\nSingle transaction by label (.loc['P0042']):")
print(by_id.loc["P0042"])
# Label slices INCLUDE the end label, unlike .iloc position slices: this returns 6 rows.
label_range = by_id.loc["P0010":"P0015", ["merchant", "amount"]]
print(f"\n.loc['P0010':'P0015', ['merchant', 'amount']] returns {len(label_range)} rows:")
print(label_range)

# --- 4. Boolean filters with more than one condition ---
# & (not `and`) combines Series element by element; each condition needs parentheses
# because & binds more tightly than ==.
declined_online = df[(df["status"] == "DECLINED") & (df["channel"] == "Online")]
print(f"\nDeclined Online transactions (boolean mask): {len(declined_online)}")
print(declined_online[["txn_id", "customer_id", "merchant", "currency", "amount"]])

non_gbp = df[df["currency"].isin(["EUR", "USD"])]
print(f"\nNon-GBP transactions (isin): {len(non_gbp)}")
print(non_gbp["currency"].value_counts())

declined_online_q = df.query("status == 'DECLINED' and channel == 'Online'")
print(f"\nSame filter via .query(): {len(declined_online_q)} rows, "
      f"identical to the mask version: {declined_online_q.equals(declined_online)}")

# --- 5. Convert to GBP with a vectorised lookup ---
# fx_rates.csv becomes a Series indexed by currency; .map() looks up every row's
# currency in one operation, then the multiplication runs on whole columns.
rates = pd.read_csv(FX_PATH).set_index("currency")["rate_to_gbp"]
# The column is not rounded per row: rounding happens once, on the totals, so that
# pandas and the plain-Python loop below agree (Series.round and Python's round()
# can disagree on values such as 6.30 * 0.85 = 5.3549999...).
df["amount_gbp"] = df["amount"] * df["currency"].map(rates)
print("\nSample of amount_gbp:")
print(df.loc[df["currency"] != "GBP", ["txn_id", "currency", "amount", "amount_gbp"]].head().round(2))

# --- 6. Ranking and sorting ---
print("\nTop 5 transactions by amount_gbp (nlargest):")
top5 = df.nlargest(5, "amount_gbp")[["txn_id", "customer_name", "merchant", "currency", "amount", "amount_gbp"]]
print(top5.round(2))

# Two sort keys: customer ascending, then amount_gbp descending within each customer.
sorted_df = df.sort_values(["customer_id", "amount_gbp"], ascending=[True, False])
print("\nSorted by customer_id then amount_gbp descending (first 8 rows):")
print(sorted_df[["customer_id", "txn_id", "merchant", "amount_gbp"]].head(8).round(2))

# --- 7. Module 3's per-customer summary, in pandas ---
summary = (
    df.groupby(["customer_id", "customer_name"])
    .agg(txn_count=("txn_id", "count"))
    .join(
        df[df["status"] == "APPROVED"]
        .groupby(["customer_id", "customer_name"])
        .agg(total_gbp=("amount_gbp", "sum"))
    )
    .reset_index()
)
summary["total_gbp"] = summary["total_gbp"].round(2)
print("\nPer-customer summary (pandas):")
print(summary.to_string(index=False))


def module3_summary():
    """Recompute Module 3's numbers in plain Python (csv + dicts), for comparison."""
    with open(FX_PATH, newline="") as f:
        fx = {row["currency"]: float(row["rate_to_gbp"]) for row in csv.DictReader(f)}
    counts = {}
    totals = {}
    with open(TXN_PATH, newline="") as f:
        for row in csv.DictReader(f):
            cid = row["customer_id"]
            counts[cid] = counts.get(cid, 0) + 1
            if row["status"] == "APPROVED":
                gbp = float(row["amount"]) * fx[row["currency"]]
                totals[cid] = totals.get(cid, 0.0) + gbp
    return {cid: (counts[cid], round(totals.get(cid, 0.0), 2)) for cid in counts}


plain = module3_summary()
# Compare money with a tolerance of half a penny rather than ==, because floating-point
# sums can differ in the last bits depending on the order of addition.
mismatches = [
    r.customer_id
    for r in summary.itertuples()
    if plain[r.customer_id][0] != r.txn_count or abs(plain[r.customer_id][1] - r.total_gbp) >= 0.005
]
print(f"\nCompared with the plain-Python (Module 3) calculation: {len(plain)} customers, "
      f"{len(mismatches)} mismatches")

# If Module 3's output file is present, compare against it too (optional).
for path in MODULE3_SUMMARY_CANDIDATES:
    if path.exists():
        m3 = pd.read_csv(path)
        merged = summary.merge(m3, on="customer_id", suffixes=("", "_m3"))
        # A few pence of tolerance: a Module 3 solution may have rounded each row to
        # 2 dp before summing, which shifts totals slightly.
        same = (
            (merged["txn_count"] == merged["txn_count_m3"])
            & ((merged["total_gbp"] - merged["total_gbp_m3"]).abs() < 0.05)
        )
        print(f"Compared with {path.name} from Module 3: {int(same.sum())} of {len(m3)} customers match")
        break
else:
    print("Module 3's output/customer_summary.csv not found; skipped the file comparison.")

# --- 8. What each pandas operation replaces from Module 3 ---
# - pd.read_csv(...)                 -> with open(...) + csv.DictReader + list(...), plus
#                                       float(row["amount"]) on every row (dtypes are inferred)
# - df[mask] / df.query(...)         -> for row in rows: if row["status"] == "DECLINED" and ...
# - df["currency"].map(rates)        -> fx[row["currency"]] inside the loop, one row at a time
# - groupby(...).agg(count)          -> counts[cid] = counts.get(cid, 0) + 1
# - filter then groupby(...).sum()   -> if approved: totals[cid] = totals.get(cid, 0.0) + gbp
# - nlargest / sort_values           -> sorted(rows, key=lambda r: ..., reverse=True)[:5]
# groupby partitions the rows by key (the dict keys in Module 3) and applies the
# aggregation to each partition (the running accumulator in Module 3), in compiled code.
