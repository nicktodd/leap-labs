# Module 5 Lab - Pandas Fundamentals: DataFrames & Series

## Scenario

PaySprint's card-payments team has one month of card transactions (2 February to 1 March 2026)
in a CSV file. In Module 3 you summarised it per customer with `csv.DictReader` and dicts. The
team now wants the same analysis in pandas, plus ad-hoc lookups and filters that would each have
needed a new loop in plain Python.

## Objectives

By the end of this lab you will have:

- Loaded a CSV into a DataFrame with a proper datetime column, and inspected its structure
- Selected rows and columns by position (`.iloc`) and by label (`.loc`), and explained the
  difference in how their slices end
- Filtered rows with combined boolean conditions, `.isin()` and `.query()`
- Added a derived column with a vectorised lookup (`.map()`), with no row loops
- Ranked and sorted with `nlargest` and multi-key `sort_values`
- Reproduced Module 3's per-customer summary with `groupby` + `agg`, and checked it matches

## Setup

- `pip install pandas` (pandas 3.x)
- Data files in `shared/` (repo root): `transactions.csv` and `fx_rates.csv`
- Starter file: `labs/05-pandas-fundamentals/starter_pandas_payments.py`. Run it with
  `python starter_pandas_payments.py`; it builds paths from its own location, so it works from
  any working directory.

## The data

`shared/transactions.csv`: 140 card transactions, one row each. Columns used in this lab:
`txn_id` (P0001..P0140), `txn_timestamp`, `customer_id`, `customer_name`, `merchant`,
`merchant_category`, `channel` (`Online`, `In-store`, `Contactless`), `currency` (GBP, EUR,
USD; `amount` is in this currency), `amount`, `status` (`APPROVED` / `DECLINED`).

`shared/fx_rates.csv`: `currency, rate_to_gbp` (FX (foreign exchange) rates to pounds
sterling). `amount_gbp = amount * rate_to_gbp`.

## Task

1. **Load and inspect.** Read `transactions.csv` with `parse_dates=["txn_timestamp"]`. Print the
   shape, `df.dtypes`, and call `df.info()`. Confirm that `txn_timestamp` is a datetime dtype.
2. **Select by position with `.iloc`.** Print rows at positions 10 to 14 inclusive, the last 3
   rows, and (in a single `.iloc` call) the first 5 rows of the first 4 columns.
3. **Select by label with `.loc`.** Make `txn_id` the index with `set_index("txn_id")`. Print
   transaction `P0042`, then `.loc["P0010":"P0015", ["merchant", "amount"]]`. Print how many rows
   the label range returns and add a comment explaining why it differs from what `.iloc[10:15]`
   style slicing would suggest.
4. **Filter with more than one condition.**
   - Declined Online transactions: combine two conditions with `&`. Each condition needs its own
     parentheses.
   - Non-GBP transactions, using `.isin()`. Print the count per currency.
   - The declined Online filter again, written with `.query()`. Confirm (in code) that it returns
     the same rows as the boolean-mask version.
5. **Convert to GBP (pounds sterling) without a loop.** Read `fx_rates.csv`, turn it into a
   Series indexed by `currency`, and add an `amount_gbp` column using `df["currency"].map(...)`.
6. **Rank and sort.** Print the 5 largest transactions by `amount_gbp` with `nlargest`. Then sort
   the whole DataFrame by `customer_id` ascending and `amount_gbp` descending (two keys, two
   directions), and print the first 8 rows.
7. **Reproduce Module 3's summary.** Build one row per customer with `txn_count` (all rows) and
   `total_gbp` (APPROVED rows only) using `groupby` and `agg`. Compare it with the plain-Python
   numbers from Module 3: either implement the `module3_summary()` stub in the starter (plain
   `csv.DictReader` and dicts), or, if you have it, also read your Module 3
   `output/customer_summary.csv`. The script must still run if that file does not exist. Compare
   money with a tolerance (for example half a penny), not `==`, and print the number of
   mismatches.
8. **Connect the two approaches.** Write a comment block mapping each pandas operation you used
   to the Module 3 loop, `if` statement or dict accumulator it replaces.

## Acceptance criteria

- The script runs with `python starter_pandas_payments.py` with no errors or warnings.
- `df.shape` is `(140, 13)` after loading, and `txn_timestamp` shows a `datetime64` dtype.
- The label range `P0010`-`P0015` returns 6 rows (label slices include the end label), and the
  comment says so.
- 11 declined Online transactions; 28 non-GBP transactions (20 EUR, 8 USD); the `.query()`
  version is confirmed identical to the mask version.
- `amount_gbp` is created without `for`, `iterrows()` or `apply()`. The largest transaction is
  P0094 at 2,145.31 GBP.
- The per-customer summary has 12 rows. K002 and K004 have the most transactions (19 each) and
  K006 has the highest approved total (2,632.04 GBP). There are 0 mismatches against the
  plain-Python calculation.
- The comment block in step 8 names the specific Module 3 pattern each pandas call replaces
  (for example `counts[cid] = counts.get(cid, 0) + 1`), not only "it is shorter".

## Extension exercises

1. **Dates with the `.dt` accessor.** Add `hour` and `day_name` columns from `txn_timestamp`.
   Print the transaction count per weekday in calendar order (Monday to Sunday), not alphabetical
   or count order. Done when Monday prints first and Sunday last, and you can explain why
   `value_counts()` alone does not give that order.
2. **Text with the `.str` accessor.** Find all coffee-shop transactions with a single
   case-insensitive `.str.contains()` call matching "coffee" or "pret". Then apply
   `.str.title()` to the distinct merchant names and print every name it changes. Done when you
   have shown `Sainsbury's` becoming `Sainsbury'S` (and found the other names it damages), and
   written one sentence on why automatic case normalisation is risky on data that is already
   clean.
3. **Vectorised versus loop performance.** Compute `amount_gbp` twice: once with an
   `iterrows()` loop and once vectorised. Time each with `time.perf_counter()`, on the 140 rows
   and on a copy scaled up 100 times with `pd.concat`. Assert both methods give the same answer.
   Done when you print both timings at both sizes and explain in a comment where the loop's
   time goes.
4. **Chained assignment under copy-on-write.** Add a `review` column set to `False`, then run
   `df[df["status"] == "DECLINED"]["review"] = True`. Show that `df` is unchanged and capture the
   warning pandas 3 emits (use `warnings.catch_warnings(record=True)`). Fix it with a single
   `.loc` assignment. Done when you print the count of flagged rows before (0) and after (13) the
   fix, with a comment explaining why the first version cannot work.
