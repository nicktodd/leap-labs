# Module 5 Lab - Model Answer Notes

See `pandas_payments.py`. Verified results against `shared/transactions.csv`:

- Shape `(140, 13)`; `txn_timestamp` is `datetime64[us]`, text columns show the pandas 3 `str`
  dtype, `amount` and `distance_from_home_km` are `float64`, `is_fraud` is `int64`.
- `.iloc[10:15]` returns P0011-P0015 (5 rows, end position excluded).
  `.loc["P0010":"P0015", ["merchant", "amount"]]` returns 6 rows (end label included).
- 11 declined Online transactions (P0016, P0029, P0045, P0076, P0088, P0092, P0106, P0110,
  P0118, P0120, P0122). The `.query()` version is identical (`.equals()` is `True`).
- 28 non-GBP transactions: 20 EUR, 8 USD.
- Top 5 by `amount_gbp`: P0094 2,145.31, P0076 1,326.74, P0016 1,259.74, P0100 1,202.97,
  P0045 1,012.76 (all USD).
- Per-customer summary (12 customers; `txn_count` all rows, `total_gbp` approved only):

  | customer | txn_count | total_gbp |
  | --- | --- | --- |
  | K001 Amara Okoye | 12 | 295.64 |
  | K002 Ben Carter | 19 | 714.21 |
  | K003 Chloe Dubois | 4 | 227.56 |
  | K004 Daniel Price | 19 | 2002.88 |
  | K005 Eilidh Murray | 10 | 164.98 |
  | K006 Farah Siddiqui | 11 | 2632.04 |
  | K007 George Mensah | 10 | 1830.64 |
  | K008 Hannah Kelly | 4 | 342.23 |
  | K009 Ibrahim Yusuf | 16 | 693.55 |
  | K010 Julia Novak | 12 | 435.13 |
  | K011 Kofi Asante | 13 | 1865.67 |
  | K012 Lena Fischer | 10 | 267.02 |

  0 mismatches against the plain-Python recomputation. The solution also compares against
  Module 3's `output/customer_summary.csv` if that file exists (with a tolerance of a few pence,
  because a Module 3 solution may have rounded each row before summing), and skips the
  comparison otherwise.

Key points to check in a delegate's solution:

- **The label-slice comment.** A delegate should state that `.loc` label slices include the end
  label and `.iloc` position slices exclude it. This is the most common off-by-one error when
  moving between the two.
- **`&` with parentheses, not `and`.** `df[df["status"] == "DECLINED" and ...]` raises
  "The truth value of a Series is ambiguous". Without parentheses, `&` binds before `==` and
  the expression fails or means something else.
- **`amount_gbp` must be vectorised.** `.map()` of a Series or dict on `currency`, then a column
  multiplication. `apply(lambda row: ..., axis=1)` or `iterrows()` works but misses the point
  of the step (Extension 3 measures why).
- **`total_gbp` counts approved rows only, `txn_count` counts all rows.** A delegate who filters
  to APPROVED before both aggregations gets a lower `txn_count` for customers with declines
  (for example K005, K009). The solution uses two groupbys joined on the customer key.
- **Rounding pitfall.** Rounding `amount_gbp` per row with `Series.round(2)` and rounding per row
  with Python's `round()` can disagree: `6.30 * 0.85` is stored as `5.3549999...`; Python's
  `round()` gives 5.35 and `Series.round(2)` gives 5.36. That single row makes K003 differ by a
  penny (227.56 vs 227.55) when the two methods are compared. Round totals once, at the end,
  and compare money with a tolerance.
- **The Module 3 mapping comment should name the loop patterns** (`counts.get(cid, 0) + 1`,
  `if row["status"] == "APPROVED"`, `fx[row["currency"]]`), not only say pandas is shorter.

## Extension notes

**E1 `.dt` accessor** (`ext1_datetime_accessor.py`). Weekday counts, Monday to Sunday: 20, 20,
18, 19, 19, 21, 23. `value_counts()` orders by count and `sort_index()` orders alphabetically
(Friday first), so a good answer uses `reindex()` with an explicit weekday list or an ordered
`Categorical`. The busiest hour is 18:00 with 19 transactions. Pitfall: calling `.dt` on a column
read without `parse_dates` raises `AttributeError: Can only use .dt accessor with datetimelike
values`.

**E2 `.str` accessor** (`ext2_string_accessor.py`). `str.contains("coffee|pret", case=False)`
finds 20 transactions (Costa Coffee 13, Pret A Manger 7). `.str.title()` changes three merchant
names: `ASOS` -> `Asos`, `Sainsbury's` -> `Sainsbury'S`, `TfL` -> `Tfl`. `string.capwords` fixes
the apostrophe but still breaks the two acronyms. The point: a generic casing function applied
to clean data introduces errors; check every distinct output value, and prefer an explicit
mapping when normalisation is needed (Module 6 builds on this).

**E3 performance** (`ext3_vectorised_vs_loop.py`). On the reference machine: 140 rows, iterrows
about 1.4-1.8 ms against 0.14-0.22 ms vectorised (about 8-9x); 14,000 rows, about 116-124 ms
against 0.35-0.40 ms (about 300-330x). Numbers vary per run and machine; the pattern (the gap
grows with row count) is what matters. A good explanation mentions that `iterrows()` builds a
Series per row and runs Python code per row, while the vectorised version runs a few operations
over whole arrays in compiled code. Pitfall: timing only the 140-row case and concluding the
difference is irrelevant.

**E4 chained assignment** (`ext4_copy_on_write.py`). The chained version emits
`ChainedAssignmentError` ("A value is being set on a copy of a DataFrame or Series through
chained assignment") and leaves 0 rows flagged. `df.loc[df["status"] == "DECLINED", "review"] =
True` flags 13 rows. Under pandas 3 copy-on-write, `df[mask]` always behaves as a new object, so
the second `[...] =` modifies that temporary object only. Delegates who learned pandas 2 may
expect it to work "sometimes"; under pandas 3 it never modifies the original.
