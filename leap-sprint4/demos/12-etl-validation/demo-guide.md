# Demo: Module 12 — ETL Concepts & Data Validation

**Duration:** 20 minutes
**Files:** `etl_pipeline_demo.py`, `test_trades_demo.py`
**Prerequisite:** `pip install pandas pytest`. GitHub Copilot Chat available.

## Part 1: ETL, conceptually (5 min)

Narration: **Extract** — get the raw data from its source (a file, an API, a database).
**Transform** — clean and reshape it into the form your analysis needs (Module 6's cleaning
steps, structured as reusable functions). **Load** — write the result somewhere downstream
analysis can rely on, without redoing the cleaning every time.

Show `etl_pipeline_demo.py`: `extract()` reads `shared/messy-trades-raw.csv`, `transform()`
reuses Module 6's cleaning logic as a single function, `load()` writes the clean result to
`clean_trades_loaded.csv`. Narration: this is exactly Module 6's lab, restructured as three named
stages instead of one long script — the same logic, but now each stage can be tested, reused, and
scheduled independently.

## Part 2: API vs. pipeline, revisited (3 min)

Recall Module 11's API-vs-extract judgement call. Narration: an ETL pipeline is usually what
*consumes* a batch extract (or periodically calls an API) and turns it into something ready for
analysis — the two modules are two ends of the same journey: Module 11 is how data arrives,
Module 12 is what happens to it once it does.

## Part 3: Validating with pytest, before analysis touches it (6 min)

Show `test_trades_demo.py` running against the **transformed** (already-cleaned) data:

```python
def test_no_missing_trade_ids(clean_trades):
    assert clean_trades["trade_id"].notna().all()

def test_quantity_is_positive(clean_trades):
    assert (clean_trades["quantity"] > 0).all()

def test_asset_class_is_valid(clean_trades):
    valid = {"Equity", "Bond", "ETF", "Crypto"}
    assert clean_trades["asset_class"].isin(valid).all()
```

Narration: these tests run *before* any analysis code touches the data — catching a schema or
range problem here, with a clear pytest failure message naming the exact assertion, is far
cheaper than discovering it three modules later as a mysteriously wrong chart or model result.

## Part 4: An unfamiliar failing-test error, interpreted with GenAI (6 min)

Run `test_asset_class_is_valid_broken`, a deliberately buggy version:

```python
def test_asset_class_is_valid_broken(clean_trades):
    valid = {"Equity", "Bond", "ETF", "Crypto"}
    assert clean_trades["asset_class"].isin(valid)  # missing .all()
```

Run it and read the error out loud: `ValueError: The truth value of a Series is ambiguous. Use
a.empty, a.bool(), a.item(), a.any() or a.all().` Ask the room: has anyone seen this exact error
before? For those who haven't, paste it into Copilot Chat and ask it to explain what's actually
going wrong.

Narration: `.isin(valid)` returns a whole boolean *Series* (one True/False per row), not a single
True/False — `assert` needs one boolean, and Python doesn't know how to collapse a multi-row
Series into "true" or "false" on its own, hence the ambiguity error. The fix, `.isin(valid).all()`,
collapses it into "were all rows valid?" Emphasise: GenAI can explain what an unfamiliar error
message means quickly, but you still write and understand the actual fix yourself — that's the
difference between using it as a learning aid and outsourcing the debugging entirely.

## Key message

Validating data with pytest, before it reaches analysis code, turns a silent bad-data problem
into a loud, specific, fixable test failure. Reading pytest's own error messages carefully (with
GenAI as a translator when the wording is unfamiliar) is a normal, efficient part of that
workflow, not a shortcut around understanding it.
