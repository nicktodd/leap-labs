from pathlib import Path

import pandas as pd

from ext2_pipe_functions import RAW_PATH, clean, normalise

OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)

raw = pd.read_csv(RAW_PATH)
norm = normalise(raw)  # same index as raw, no rows removed

# One reason per rejected row, assigned in pipeline order: a row rejected for its amount
# is not also counted as a duplicate.
reason = pd.Series(pd.NA, index=raw.index, dtype="str")
reason[raw["amount"].isna()] = "blank amount"
reason[reason.isna() & norm["amount"].isna()] = "non-numeric amount (" + raw["amount"] + ")"
reason[reason.isna() & norm["txn_timestamp"].isna()] = "invalid date (" + raw["txn_timestamp"] + ")"
survivors = reason.isna()
dup = norm["txn_id"].where(survivors).duplicated() & survivors
reason[dup] = "duplicate of an earlier row with the same txn_id"

# Quarantine keeps the ORIGINAL raw values, so the source team sees exactly what arrived.
rejected = raw[reason.notna()].assign(reject_reason=reason[reason.notna()])
rejected.to_csv(OUT / "rejected_rows.csv", index=False)
print(rejected[["txn_id", "merchant", "amount", "txn_timestamp", "reject_reason"]].to_string(index=False))

clean_df = clean(raw)
print(f"\nReconciliation: raw {len(raw)} = clean {len(clean_df)} + rejected {len(rejected)}")
assert len(raw) == len(clean_df) + len(rejected)
# Every raw row index is in exactly one of the two sets.
assert set(clean_df.index).isdisjoint(rejected.index)
assert set(clean_df.index) | set(rejected.index) == set(raw.index)
print(rejected["reject_reason"].str.split(" \\(").str[0].value_counts().to_string())
print(f"\nWrote {OUT / 'rejected_rows.csv'}")
