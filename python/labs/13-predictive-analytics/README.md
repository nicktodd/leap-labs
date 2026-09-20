# Module 13 Lab - Predictive Analytics, Forecasting & Model Evaluation

## Objectives

By the end of this lab you will have:

- Built a first simple regression model on the mission dataset
- Split data into train and test sets, and explained why that matters
- Evaluated the model with an appropriate metric, compared against a naive baseline
- Investigated a surprising result rather than accepting it at face value

## Setup

- `pip install pandas scikit-learn`
- `shared/trades.csv` (repo root)

## Two acronyms used throughout this lab

- **MAE - Mean Absolute Error**: the average size of the prediction error, in the original units
  (e.g. dollars). Easy to explain to a non-technical stakeholder: "predictions are off by about
  $X, on average."
- **RMSE - Root Mean Squared Error**: like MAE, but errors are squared before averaging (then
  square-rooted back to the original units), so a few large errors count for more than many small
  ones. RMSE is always >= MAE for the same set of predictions.

## Task

Starter file: `starter_predictive.py`, in `labs/13-predictive-analytics/`.

1. Build a `LinearRegression` model predicting `value` from **both** `quantity` and `price`.
2. Split the data with `train_test_split(test_size=0.3, random_state=42)`.
3. Evaluate the model on the test set with both MAE and RMSE (defined above).
4. Build a `DummyRegressor(strategy="mean")` baseline, evaluate it the same way, and compare.

You should find the model **does not clearly beat the baseline** - which is surprising, since
`value` looks like it should be a simple function of `quantity` and `price`. Don't stop there.

5. Investigate: for each row, compute `quantity * price` and compare it to the actual `value`.
   Find which rows disagree, and which `asset_class` they belong to.
6. Once you've found the pattern, write a comment explaining it: what's actually different about
   how `value` is calculated for that asset class, compared to every other trade in the dataset?
7. Write a plain-English paragraph, as a comment, explaining what the MAE actually means to a
   non-technical stakeholder, why the model underperformed, and what you'd change about the
   features before trying again (hint: what if you calculated `value` per-asset-class-correctly
   as an engineered feature, rather than relying on the model to infer it?).

## Acceptance criteria

- The script runs with `python starter_predictive.py` and produces no errors.
- `train_test_split` is used with `test_size=0.3, random_state=42` (for a fair comparison with
  the reference solution's exact numbers).
- Both MAE and RMSE are printed for the model and the baseline.
- The investigation correctly identifies which asset class breaks the simple
  `value = quantity * price` assumption, and states the actual relationship for that class.
- Your plain-English explanation cites specific numbers from your own output and correctly
  explains *why* the model underperformed, not just *that* it did.
