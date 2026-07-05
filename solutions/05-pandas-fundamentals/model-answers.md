# Module 5 Lab — Model Answer Notes

See `pandas_intro.py`. Verified: the `groupby("client_name")["value"].sum()` totals match
Module 3's manual-loop solution exactly, for every client.

Key points to check:

- **`.loc[condition, [columns]]`, not manual iteration**, for the SELL-only selection. A
  delegate who writes `for i, row in df.iterrows(): if row["side"] == "SELL": ...` has missed
  the point of the module — `iterrows()` works, but defeats the reason pandas exists.
- **`df["advisor"].unique()` returns a NumPy array, not a Python `set`** — both express "distinct
  values," but delegates should notice the type difference if they check `type(...)`.
- **The comment explaining `groupby` should reference Module 3's actual pattern**
  (`dict.get(key, 0.0) + value`), not just say "it's a shortcut" — the point of the comparison is
  connecting the two, not just noting pandas is shorter.
