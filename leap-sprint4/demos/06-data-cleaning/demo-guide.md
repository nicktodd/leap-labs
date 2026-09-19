# Demo: Module 6 — Data Cleaning & Preparation

**Duration:** 20 minutes
**Files:** `clean_trades_demo.py`
**Data:** `shared/messy-trades-raw.csv` — the same trades as `trades.csv`, deliberately dirtied

## Part 1: Seeing the damage (4 min)

Load the messy file and run `df.info()` and `df.isna().sum()`. Narration: before fixing
anything, always quantify what's actually wrong — three missing values (`quantity`, `value`,
`client_name`, one each), and `df.info()` alone won't show the duplicate row, the inconsistent
date format, or the outlier. Cleaning starts with inspection, not assumption.

## Part 2: Missing values — three different decisions, on purpose (6 min)

Walk through all three missing values, narrating that **the right fix depends on what's
missing, not a single blanket rule**:

- **`quantity` missing (T0005)** — there's no way to safely reconstruct a trade's quantity from
  the other columns. **Decision: drop the row.** Fabricating a number here would silently corrupt
  every downstream total.
- **`value` missing (T0004)** — `value` is derivable: `quantity * price`. **Decision: recompute
  it**, don't drop the row.
- **`client_name` missing (T0010)** — `client_id` (`C007`) appears on another row (`T0020`) that
  *does* have a name. **Decision: backfill from the other row with the same `client_id`**, using
  `groupby("client_id")["client_name"].transform("first")`.

Key message: "fill it in," "drop it," and "recompute it" are all valid — the data itself tells
you which, you don't get to pick whichever is easiest.

## Part 3: Data types, including dates (4 min)

Show `trade_date` parsed with `pd.to_datetime()`. Point out the deliberately ambiguous row:
`05/01/2026` could be 5 January or 1 May, depending on the format assumed. Narration: resolve
ambiguity using context, not assumption — this trade's `trade_id` (`T0002`) places it between
`T0001` (`2026-01-05`) and `T0003` (`2026-01-06`), so it must be `2026-01-05`, meaning the source
format is day-first, not month-first. **Never silently guess a date format**; when genuinely
unsure, go back to the source system or the person who produced the file.

Also normalise `asset_class`'s casing (`"equity"` vs. `"Equity"`). Try `.str.capitalize()` first
and let the room notice it turns `"ETF"` into `"Etf"` — it doesn't know `ETF` is an acronym, it
just upper-cases the first letter and lower-cases the rest. Fix it with a small canonical mapping
(`{"equity": "Equity", "etf": "ETF", ...}`) instead. Narration: a generic string-cleaning
function can introduce a *new* inconsistency while fixing an old one — always check its output
against every distinct value, not just the ones you were originally worried about.

## Part 4: Duplicates and outliers (6 min)

- **Duplicate row (T0006 appears twice, identically)** — `df.duplicated()` finds it,
  `drop_duplicates()` removes it. Straightforward because it's an *exact* duplicate; a near-
  duplicate (same trade, slightly different values) would need a judgement call instead.
- **Outlier (T0021, quantity 99,999)** — flag it, don't blindly delete it. Compare it to other
  Equity quantities (all under 200): this could be a genuine institutional block trade, or a
  fat-finger error (perhaps a missing decimal point: `999.99`?). Narration: an outlier is a
  question, not an automatic deletion — the lab requires delegates to document their reasoning,
  not just apply a rule.

## Key message

Cleaning isn't one technique applied uniformly, it's a series of individual decisions, each
justified by what's actually knowable about that specific problem. Documenting *why* you chose
drop vs. recompute vs. backfill vs. flag matters as much as the code that does it.
