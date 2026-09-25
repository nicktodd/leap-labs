# Module 3 Lab - Model Answer Notes

See `customer_activity.py` for the core solution and `ext1_set_operations.py` to
`ext4_round_trip.py` for the extensions. Every script runs from any folder; output files are
written to `output/` next to the script.

## Verified results

Output of `python customer_activity.py`:

- `FX rates: {'GBP': 1.0, 'EUR': 0.85, 'USD': 0.79}`
- `Read 140 transactions`, `Customers with transactions: 12`
- `All 18 merchants map to exactly one category`, `Distinct (merchant, category) pairs: 18`
- `A list cannot be a set member: unhashable type: 'list'`
- Summary table, sorted by approved GBP total:

| id | customer | txns | total_gbp | largest | cats |
|---|---|---:|---:|---:|---:|
| K006 | Farah Siddiqui | 11 | 2,632.04 | 2,145.31 | 5 |
| K004 | Daniel Price | 19 | 2,002.88 | 652.38 | 7 |
| K011 | Kofi Asante | 13 | 1,865.67 | 780.00 | 8 |
| K007 | George Mensah | 10 | 1,830.64 | 1,202.97 | 6 |
| K002 | Ben Carter | 19 | 714.21 | 157.14 | 6 |
| K009 | Ibrahim Yusuf | 16 | 693.55 | 293.81 | 7 |
| K010 | Julia Novak | 12 | 435.13 | 100.86 | 7 |
| K008 | Hannah Kelly | 4 | 342.23 | 151.57 | 2 |
| K001 | Amara Okoye | 12 | 295.64 | 88.25 | 6 |
| K012 | Lena Fischer | 10 | 267.02 | 61.64 | 4 |
| K003 | Chloe Dubois | 4 | 227.56 | 122.33 | 2 |
| K005 | Eilidh Murray | 10 | 164.98 | 81.22 | 6 |

- `output/customer_summary.csv`: header plus 12 rows, e.g. `K006,Farah Siddiqui,11,2632.04,2145.31,5`.
  The 12 totals add up to GBP 11,471.55 (checked in Extension 4).
- `output/declined.json`: 13 objects, P0016, P0029, P0037, P0045, P0076, P0088, P0092, P0106,
  P0110, P0114, P0118, P0120, P0122. The first is P0016 (Apple Store, USD 1,594.61,
  `amount_gbp` 1259.74).

## Key points to check in a delegate's solution

- **`rate_to_gbp` and `amount` are converted with `float()`.** `csv.DictReader` returns strings.
  A `rates` dict that prints `{'GBP': '1.00', ...}` leads to
  `TypeError: can't multiply sequence by non-int of type 'str'` on the first conversion.
- **`setdefault` returns the stored value.** `d.setdefault(k, []).append(t)` works because the
  call returns the list that is already in the dict (or the new one it has inserted). A delegate
  who writes `d[k] = d.get(k, []).append(t)` stores `None`, because `append` returns `None`.
- **The consistency check uses a set per merchant, not a list.** With a list, a merchant with 16
  transactions would hold 16 copies of its category and `len(...) != 1` would flag every
  merchant.
- **Why a tuple can be a set member.** Set membership depends on a hash, and a hash must not
  change while the value is in the set. A tuple is immutable, so its hash is stable; a list can
  change, so Python refuses to hash it (`unhashable type: 'list'`). The same rule applies to
  dict keys.
- **`total_gbp` and `largest_txn_gbp` use approved transactions only.** Including declines makes
  K002 Ben Carter's total and largest value much larger (his declined P0016 is GBP 1,259.74),
  and he moves up the table. A delegate whose table does not match should check the filter first.
- **`max()` compares by the GBP amount.** `max(approved, key=lambda t: t["amount"])` compares
  strings, so `"99.00"` beats `"1202.97"`; `key=lambda t: float(t["amount"])` compares numbers but
  ranks a USD amount against a GBP amount as if they were the same unit.
- **Rounding happens at the end.** `amount_gbp` keeps full precision in memory and is rounded
  only in the summary row and the JSON output, so totals are not built from rounded pieces.
- **`newline=""` on the CSV write.** Without it, Windows writes a blank line between rows,
  because the `csv` module writes its own `\r\n` line endings.
- **The JSON keeps the CSV's strings.** In `declined.json`, `amount` is `"1594.61"` (a string)
  while `amount_gbp` is a number, because only `amount_gbp` was computed. That is acceptable for
  this task; a delegate who converts the other numeric fields before `json.dump` has gone beyond
  it, and should be asked to say which fields they converted.
- **`with` for every file**, reading and writing. `json.dump(data, open(path, "w"))` without a
  `with` is a common miss.

## Extension notes

**E1 - Set operations.** Customers who used both Online and In-store: 10 (K001, K002, K004,
K005, K006, K007, K009, K010, K011, K012); K003 and K008 never used In-store. Customers with a
decline: K001, K002, K005, K009, K010, K011, K012, so 5 customers have none (K003, K004, K006,
K007, K008). Merchants used by exactly one customer: `{'Airbnb': {'K004'}}`. Look for `sorted()`
around every printed set: set order is not guaranteed, and unsorted output makes comparisons with
a partner confusing.

**E2 - `defaultdict` and `Counter`.** The `defaultdict(list)` grouping equals the `setdefault`
dict (`True`). Reading `by_customer['K999']` returns `[]` and grows the dict from 12 keys to 13:
the missing-key default is inserted on read, not only on write. That is the case where the plain
dict is safer: code that looks up IDs from another source (such as a customer list) can silently
create empty entries, which then appear in reports as customers with zero transactions. Top 3
merchants: Uber 16, TfL 15, Tesco 14, and the manual `dict` plus `sorted` gives the same result.
The solution also shows that `Counter` returns 0 for an unseen key (`Dining`, which has no
declines).

**E3 - Join to reference data.** 11 customers in `customers.csv`. Highest use of credit limit:
K011 Kofi Asante 62.2% (GBP 1,865.67 of 3,000), then K009 Ibrahim Yusuf 46.2% (GBP 693.55 of
1,500); lowest K001 Amara Okoye 3.7%. K012 is reported as a warning: approved spend GBP 267.02,
no row in `customers.csv`. The ranking differs from the core table: K006 has the highest spend
but uses 17.5% of a GBP 15,000 limit. A delegate who uses `customers[customer_id]` gets
`KeyError: 'K012'`, which is the point of the exercise. Dropping K012 silently (with a
`continue` and no message) is a weaker answer: the missing reference data is itself a finding.

**E4 - Round trip.** Reading the file back gives 12 rows, grand total GBP 11,471.55 from both the
file and memory, and no per-customer mismatches. Comparing with `==` works here because both
sides hold the same values rounded to 2 decimal places and `float()` of the written text returns
the same float; comparing the file against unrounded in-memory sums would need
`math.isclose`. The formatted file holds `'2,632.04'`, and `float()` raises
`ValueError: could not convert string to float: '2,632.04'`. Formatting belongs to the display
layer; a file that another program reads should hold values that parse without knowing how they
were displayed (thousands separators also differ by locale: `2.632,04` in much of Europe). The
solution uses `runpy.run_path` to run the core script and reuse its `summary_rows`; a delegate who
recomputes the totals in the extension script is also correct.
