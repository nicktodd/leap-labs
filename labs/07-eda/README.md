# Module 7 Lab — Exploratory Data Analysis (EDA)

## Objectives

By the end of this lab you will have:

- Used `describe()`, `value_counts()`, and `groupby` to summarise and segment the mission dataset
- Identified at least one pattern and one anomaly worth investigating further
- Written down a specific, checkable hypothesis about the data — not a vague observation

## Setup

- `pip install pandas`
- `shared/trades.csv` (repo root) — the clean mission dataset

## Task

Starter file: `starter_eda.py`, in `labs/07-eda/`.

1. Print the shape of the dataset and `describe()` on the numeric columns.
2. Segment the data by `currency`: how many trades are in USD vs. GBP, and what's the mean
   `value` for each? (Careful: don't sum values across currencies without noting they're not
   directly comparable — that's the anomaly this step is designed to surface.)
3. Segment by `client_name`: which client has the highest total trade value, and which has the
   most individual trades? (These are not necessarily the same client — check both.)
4. Segment by `instrument` within `asset_class == "Equity"` only: which equity instrument has the
   highest total value traded?
5. Write down **one pattern**, **one anomaly**, and **one specific hypothesis** as comments in
   your script, each in a single clear sentence. A hypothesis must be checkable (e.g. "clients
   served by J. Okafor trade larger average values than clients served by other advisors"), not
   vague (e.g. "some advisors seem busier").

## Acceptance criteria

- The script runs with `python starter_eda.py` and produces no errors.
- All four segmentations (currency, client, equity instrument, and whichever grouping you choose
  for the pattern/anomaly/hypothesis) are present.
- The GBP/USD currency-mixing anomaly is explicitly called out in a comment, not silently ignored.
- Your hypothesis is phrased so that it could, in principle, be confirmed or rejected with
  Module 8's statistical tools — not just a feeling about the data.
