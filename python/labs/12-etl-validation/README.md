# Module 12 Lab - ETL Concepts & Data Validation

## Scenario

PaySprint receives a raw card-transactions extract every month, and the Module 6 cleaning script
is now run by hand each time. The payments team wants it turned into an ETL (extract, transform,
load) pipeline that can be scheduled: small cleaning functions that can each be tested, a clean
output file, and a rejects file that explains every row that did not make it through. A pytest
suite must prove that no row is lost without a recorded reason.

## Objectives

By the end of this lab you will have:

- Structured a pipeline as extract, transform and load stages, with an extract stage that does
  not interpret types
- Split the transform stage into small functions and unit-tested each one on hand-made input
- Used `@pytest.mark.parametrize` to test many input variants with one test function
- Used a `scope="module"` fixture so the pipeline runs once for the whole test file
- Written a reconciliation test and a load test that uses pytest's `tmp_path` fixture
- Used GenAI to interpret an unfamiliar failing-test message, then written the fix yourself

## Setup

- `pip install pandas pytest` (pandas 3.x)
- Data files in `shared/` (repo root): `messy-transactions-raw.csv` and `fx_rates.csv`
- Starter files in `labs/12-etl-validation/`: `starter_payments_etl.py` (the pipeline, with
  function stubs) and `starter_test_payments_etl.py` (the test file, with TODO comments)
- Run the pipeline with `python starter_payments_etl.py`. Run the tests from inside
  `labs/12-etl-validation/` with `python -m pytest -v starter_test_payments_etl.py`
  (the test file imports the pipeline module from the same folder).
- GitHub Copilot Chat available for Part 3

## The data

`shared/messy-transactions-raw.csv` is the 143-row raw extract you cleaned in Module 6. It has
the columns `txn_id`, `txn_timestamp`, `customer_id`, `customer_name`, `merchant`,
`merchant_category`, `channel`, `country`, `currency`, `amount`, `status`,
`distance_from_home_km` and `is_fraud`, and the same problems: currency symbols and thousands
separators in `amount`, two unrecoverable amounts, channel spelling variants, `UK` instead of the
ISO (International Organization for Standardization) code `GB`, stray whitespace, missing
categories, two timestamp formats, an impossible date and duplicate rows.

`shared/fx_rates.csv` gives `rate_to_gbp` for GBP (pounds sterling), EUR and USD. FX (foreign
exchange) conversion: `amount_gbp = amount * rate_to_gbp`.

## Task

The demo wrapped Module 6's cleaning in one `transform()` function and tested only the final
output. This lab goes further: each cleaning rule becomes its own function with its own tests,
rejected rows are kept and explained, and the tests check that nothing disappears.

### Part 1: Build the pipeline

Complete the functions in `starter_payments_etl.py`.

1. **Extract.** `extract(path)` reads the raw file with `dtype=str` and
   `keep_default_na=False`, so every value arrives as the text that was in the file. In the
   docstring, explain why the extract stage should not interpret types. Print the distinct raw
   `channel` values with `repr()`: you will need them for the tests.
2. **Small transform functions.** Each takes a Series (or DataFrame) and returns a new one:
   - `clean_amount(series)`: remove `£`, `€`, `$` and thousands separators, then
     `pd.to_numeric(..., errors="coerce")`.
   - `normalise_channel(series)`: map every variant to `Online`, `In-store` or `Contactless`.
     An unrecognised value becomes NaN; it is never guessed.
   - `normalise_country(series)`: upper-case codes, `UK` -> `GB`.
   - `parse_timestamps(series)`: parse `YYYY-MM-DD HH:MM` and `DD-Mon-YYYY HH:MM` explicitly;
     anything else (including `2026-02-29`) becomes NaT.
   - `fill_categories(df)`: fill a blank `merchant_category` from the category the same merchant
     has on other rows.
   - `add_amount_gbp(df, fx)`: add `amount_gbp`, rounded to 2 decimal places.
3. **Transform.** `transform(raw, fx)` returns a tuple `(clean, rejects)`. It calls the small
   functions, and every row it removes goes into `rejects` with its **raw** values and a
   `reject_reason`: `"duplicate"`, `"bad amount"` or `"invalid timestamp"`. Choose the order of
   the steps so that P0102's reformatted second copy is detected as a duplicate (Module 6 showed
   why the order matters). Convert `distance_from_home_km` to float and `is_fraud` to int. Add a
   boolean `needs_review` column for Contactless payments above GBP 100 (the UK contactless
   limit): flag them, do not delete them.
4. **Load.** `load(clean, rejects, out_dir)` creates `out_dir` if needed, writes
   `clean_transactions.csv` and `rejected_transactions.csv` into it and returns both paths. The
   default `out_dir` is the `output/` folder next to the script.
5. Run the script. Print the counts (raw, clean, rejected), the rejected rows with their
   reasons, the rows flagged for review, the channel counts and the total `amount_gbp`.

### Part 2: Validate with pytest

Complete `starter_test_payments_etl.py`. Group the tests into three kinds:

1. **Unit tests** on tiny hand-made inputs, with no files involved:
   - one `@pytest.mark.parametrize` test for `normalise_channel` covering every raw variant you
     printed in step 1 (and the three canonical values), plus a test that an unknown value
     such as `"Telephone"` becomes NaN;
   - `normalise_country`, `clean_amount` (including `"TBC"` and `""`) and `parse_timestamps`
     (both formats give the same `Timestamp`, and `2026-02-29 09:35` gives NaT).
2. **Output validation** using a fixture with `scope="module"` that runs `extract()` and
   `transform()` once and returns the raw, clean and rejected data. Test: the clean row count;
   no nulls in the required columns; `channel` only takes the three allowed values;
   `amount > 0`; `txn_id` is unique; every currency is in the FX table; the outlier is flagged
   in `needs_review` and still present.
3. **Reconciliation and load:**
   - a reconciliation test: raw rows == clean rows + rejected rows;
   - a test that the reject reasons per `txn_id` are the ones you expect (compare a dict);
   - a load test that writes into pytest's built-in `tmp_path` fixture (a fresh temporary folder
     per test), reads both files back and checks the row count and columns. A test must never
     write into your real `output/` folder.

Run `python -m pytest -v starter_test_payments_etl.py` until every test passes.

### Part 3: Interpret an unfamiliar failing test, then fix it yourself

Print the total of `amount_gbp` in the clean data, rounded to 2 decimal places. Then add this
test, using that rounded value:

```python
def test_total_amount_gbp(pipeline):
    assert pipeline["clean"]["amount_gbp"].sum() == <your rounded total>
```

Run it and read the failure message carefully: the two numbers pytest prints look almost the
same. If you do not recognise the cause, paste the message into Copilot Chat and ask what is
going wrong. Then, **without copying a suggested fix verbatim**, rewrite the assertion with
`pytest.approx` and add a comment that explains why `==` failed and what `pytest.approx`
compares instead. Keep the original assertion as a comment above the fix, with the failure
message pytest printed.

## Acceptance criteria

- `extract`, the six small transform functions, `transform` and `load` are separate functions;
  `extract` returns only strings and its docstring explains why.
- The pipeline reports 143 raw rows, 138 clean rows and 5 rejected rows: P0095 and P0102
  (`duplicate`), P0057 and P0086 (`bad amount`), P0131 (`invalid timestamp`).
- The clean data has channel counts Online 69, Contactless 46, In-store 23, and `GB` 111 rows.
- P0141 (Pret A Manger, Contactless, GBP 1,850.00) is in the clean output with
  `needs_review` True, and it is the only flagged row.
- `output/clean_transactions.csv` and `output/rejected_transactions.csv` are written; the
  rejects file shows the raw values (for example `TBC` in `amount`) and a `reject_reason`.
- The `normalise_channel` test is parametrised and covers every raw variant.
- The fixture has `scope="module"`; the load test uses `tmp_path`.
- The reconciliation test passes: 143 == 138 + 5.
- Part 3: the exact-equality failure message is recorded in a comment, and the fix uses
  `pytest.approx` with your own explanation.
- All tests pass with `python -m pytest -v starter_test_payments_etl.py` (or your renamed test
  file).

## Extension exercises

Save extension tests as separate files and run each one by name, for example
`python -m pytest -v ext1_test_schema.py` (pytest only discovers `test_*.py` files
automatically).

1. **Schema test.** Write a test that compares the clean DataFrame's columns (in order) and
   dtypes against a dict `EXPECTED_DTYPES` of column name -> dtype string. Done when the test
   passes, and when you remove the `is_fraud` conversion from `transform()` the failure
   message names `is_fraud` and both dtypes.
2. **Idempotency.** Run the pipeline twice into two different temporary folders (use
   `tmp_path_factory` in a module-scoped fixture) and assert that each output file has the same
   SHA-256 hash (`hashlib`) both times. Add a second test that runs twice into the same folder
   and checks the files are replaced, not appended to. Done when both tests pass and a docstring
   explains why a scheduled pipeline must produce identical output when it is re-run.
3. **Hand-crafted bad input.** In a fixture, build a small CSV in `tmp_path` from three genuine
   raw rows plus rows with an unsupported currency (`JPY`) and a negative amount (`-25.00`, and
   one with a currency symbol, `-£12.50`). Add rules so these rows are rejected with the reasons
   `"unknown currency"` and `"negative amount"`. Done when tests assert the exact reason for each
   bad row, that the three good rows survive, that reconciliation still holds, and that the real
   file still gives 138 clean rows.
4. **Coverage.** `pip install pytest-cov`, then run
   `python -m pytest --cov=<your pipeline module> --cov-branch --cov-report=term-missing` on
   your test file. Identify a function or block that no test executes, write a test that covers
   it, and rerun to show the missing lines have gone. Done when you can also name one data case
   that your tests never try even though the coverage report shows the code as covered, and
   explain why line coverage cannot see it.
