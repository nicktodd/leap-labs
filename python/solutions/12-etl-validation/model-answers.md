# Module 12 Lab - Model Answer Notes

See `payments_etl.py` (the pipeline) and `test_payments_etl.py` (the test suite) for the core
solution, and `ext1_test_schema.py` to `ext4_test_coverage_gaps.py` for the extensions. Run the
tests from inside `solutions/12-etl-validation/`. The extension files do not match pytest's
`test_*.py` pattern, so run each by name, for example `python -m pytest -v ext1_test_schema.py`.

## Verified results

Output of `python payments_etl.py`:

- 143 raw rows -> 138 clean rows + 5 rejected rows.
- Rejected: P0095 and P0102 `duplicate`, P0057 (blank amount) and P0086 (`TBC`) `bad amount`,
  P0131 (`2026-02-29 09:35`) `invalid timestamp`. The rejects file keeps the raw values, so
  `TBC` and the blank amount appear as they arrived.
- Flagged for review, kept in the clean output: P0141, Pret A Manger, Contactless,
  `amount_gbp` 1850.0. It is the only flagged row.
- Channels: Online 69, Contactless 46, In-store 23. Countries: GB 111, US 8, ES 6, FR 5, IE 4,
  NL 2, DE 2.
- Total `amount_gbp`: `np.float64(19099.010000000002)`.
- Writes `output/clean_transactions.csv` and `output/rejected_transactions.csv`.

`python -m pytest -v` (collects `test_payments_etl.py` only): 28 passed. That is 16 unit tests
(12 parametrised channel variants, the unknown-channel test, country, amount and timestamps) and
12 tests on the pipeline output, reconciliation, load and the Part 3 total.

Part 3: with `assert clean["amount_gbp"].sum() == 19099.01` the test fails with
`assert np.float64(19099.010000000002) == 19099.01`. The fix is
`== pytest.approx(19099.01)`.

## Key points to check in a delegate's solution

- **`extract` reads with `dtype=str, keep_default_na=False`.** With defaults, pandas turns the
  blank amount into NaN before any rule sees it, and `TBC` forces `amount` to text anyway. The
  docstring should say that type conversion belongs in transform, where it is tested, and that
  keeping raw strings lets rejected rows be written out as they arrived.
- **Duplicates are removed after text normalisation.** If `drop_duplicates()` runs on the raw
  rows, only P0095 is found; P0102's second copy (` Amazon`, `ONLINE`) survives and the clean
  count is 139, which `test_txn_id_unique` then catches. `subset=["txn_id"]` also works, but the
  delegate should say which copy is kept and why.
- **Rejects carry raw values and a reason**, and the reconciliation test (143 == 138 + 5) is
  present. A pipeline that drops rows with `dropna()` and no record passes the row-count test
  but cannot explain itself to an auditor.
- **`normalise_channel` returns NaN for an unknown value** rather than falling back to a default,
  and there is a test for it.
- **The channel test is parametrised over every raw variant**, not a loop inside one test. With
  `parametrize`, a failure names the exact input; with a loop, the first failure hides the rest.
- **The fixture has `scope="module"`** and the comment says why that is safe (the tests only
  read the result). A function-scoped fixture works but reruns the pipeline for every test.
- **The load test uses `tmp_path`.** A test that writes into `output/` can overwrite a real
  result and leaves files behind.
- **Part 3 is explained, not only fixed.** The comment should say that most decimal values
  (0.85, 0.01) have no exact binary floating-point representation, so a sum of 138 rounded
  amounts carries a tiny error, and that `pytest.approx` compares within a tolerance (relative
  1e-6 by default). Rounding the sum to 2 decimal places before `==` also passes, and is
  acceptable if the delegate can explain it; comparing the `repr` string is not.
- **`test_amount_gbp_matches_rate` needs a tolerance too.** P0026 is EUR 6.30; `6.30 * 0.85` is
  `5.3549999999999995` and pandas rounds it to 5.36, which is slightly more than 0.005 from the unrounded
  product. The model answer uses `pytest.approx(expected, abs=0.01)`. A delegate who uses
  `abs=0.005` sees this test fail on P0026, which is a second example of the Part 3 lesson.

## Extension notes

**E1 - Schema test.** `ext1_test_schema.py`: 2 passed. In pandas 3 text columns have dtype
`str` and the parsed timestamp is `datetime64[us]`; delegates who expect `object` or
`datetime64[ns]` (pandas 2) will see the difference in the failure message. Comparing two dicts
makes pytest print only the differing keys: removing the `is_fraud` conversion from `transform()`
gives `{'is_fraud': 'str'} != {'is_fraud': 'int64'}`. Check that column order is also asserted,
since it is part of what CSV consumers read.

**E2 - Idempotency.** `ext2_test_idempotency.py`: 3 passed (one hash test per output file, one
same-folder rerun test). `tmp_path` is function-scoped, so the module-scoped fixture needs
`tmp_path_factory`; delegates who try `tmp_path` in a module fixture get a `ScopeMismatch`
error. Hashing the bytes catches formatting changes (float representation, column order, line
endings) that a DataFrame comparison would ignore. Common ways to break idempotency, worth
discussing: appending with `mode="a"`, adding a run timestamp column, or iterating over a `set`
to order rows.

**E3 - Hand-crafted bad input.** `ext3_test_bad_input.py`: 5 passed. `transform_strict()` checks
the raw rows first (currency in the FX table, amount not negative), then passes the rest to the
unchanged `transform()`. X0001 (JPY) is rejected as `unknown currency`, X0002 (`-25.00`) and
X0003 (`-£12.50`) as `negative amount`; P0001-P0003 survive and reconciliation holds. On the real
file the strict version still gives 138 clean rows and only the three original reasons. Pitfalls:
`clean_amount(...) < 0 & mask` without parentheses (`&` binds more tightly than `<`), and
rejecting a row twice when it breaks both rules, which breaks reconciliation.

**E4 - Coverage.** `pytest-cov` 7.1.0 is used. On `test_payments_etl.py` alone the report is 84%
for `payments_etl.py`, missing lines 149-152 (`run_pipeline`) and 156-165 (the `__main__`
block). `ext4_test_coverage_gaps.py` adds an end-to-end `run_pipeline(out_dir=tmp_path)` test;
with it the report is 88% and only the `__main__` block is missing (29 passed, 1 xfailed). The
second point is the more important one: `transform()` shows as covered, yet no test feeds it a
channel that cannot be mapped. With P0001's channel set to `Telephone`, the pipeline still
returns 138 clean rows and 5 rejects, and P0001 keeps a NaN channel. The extension records this
as a `strict=True` `xfail` test. Look for a delegate who can explain that coverage counts lines
executed, and vectorised pandas code has no branches for different data values.
