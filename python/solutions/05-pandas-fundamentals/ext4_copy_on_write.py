import warnings
from pathlib import Path

import pandas as pd

SHARED = Path(__file__).resolve().parents[2] / "shared"

df = pd.read_csv(SHARED / "transactions.csv")
df["review"] = False

# Chained assignment: df[mask] creates a new object, and ["review"] = True is applied
# to that intermediate object. Under pandas 3 copy-on-write the intermediate always
# behaves as a copy, so df is never modified. pandas emits ChainedAssignmentError
# (a warning, not an exception); it is recorded here so it can be printed.
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    df[df["status"] == "DECLINED"]["review"] = True

for w in caught:
    print(f"{w.category.__name__}: {str(w.message).splitlines()[0]}")
print(f"Rows flagged for review after chained assignment: {df['review'].sum()}")

# Fix: one .loc call selects rows and column together and assigns in a single step.
df.loc[df["status"] == "DECLINED", "review"] = True
print(f"Rows flagged for review after .loc assignment:    {df['review'].sum()}")

# A second common form of the same mistake: taking a filtered subset, then modifying it.
# Under copy-on-write the subset is independent, so df is again unchanged; call .copy()
# to make the intention explicit if the subset is meant to be modified separately.
declined = df[df["status"] == "DECLINED"].copy()
declined["review"] = "escalated"
print(f"df['review'] after editing the subset: {df['review'].value_counts().to_dict()}")
