# Demo: Module 13 — Predictive Analytics, Forecasting & Model Evaluation

**Duration:** 22 minutes
**Files:** `predictive_demo.py`
**Prerequisite:** `pip install scikit-learn`

## Part 1: Three problem types, conceptually (4 min)

Narration, one line each:

- **Regression** predicts a number (e.g. what will this trade's value be?)
- **Classification** predicts a category (e.g. is this trade a BUY or a SELL?)
- **Time series forecasting** predicts a future point along a timeline (e.g. what will next
  week's total value be?) — Module 9's weekly `resample()` totals are exactly the shape of input
  forecasting needs, though this dataset only has two weeks, nowhere near enough to forecast a
  third responsibly. Mention it conceptually; don't build it on two data points.

## Part 2: Train/test split, and why it matters (4 min)

Narration: if you evaluate a model on the same data it learned from, it can look artificially
good, it's memorised the answers, not learned the underlying pattern. `train_test_split` holds
back a portion of the data (here, 30%) that the model never sees during training, so the
evaluation reflects how it performs on data it hasn't memorised.

## Part 3: A regression model, evaluated honestly (7 min)

Build a `LinearRegression` predicting `value` from `quantity` alone. Compute MAE and RMSE on the
held-out test set. Then compute the same two metrics for a **naive baseline** that always
predicts the training mean, using `DummyRegressor`.

Run it and look at the actual numbers together: the trained model's MAE (≈15,363) barely beats
the naive baseline's MAE (≈15,630). Narration: this matches Module 8's finding directly — the
correlation between `quantity` and `value` was weak (r ≈ -0.21), so a model built on `quantity`
alone was never going to predict `value` well. **A model that barely beats a naive baseline is
an honest, useful result, not a failure of the exercise** — it tells you `quantity` alone isn't a
strong enough signal, which is worth knowing.

## Part 4: MAE vs. RMSE — what each actually measures (3 min)

Narration: MAE (Mean Absolute Error) is the average size of the error, in the original units —
easy to explain to a non-technical stakeholder ("on average, predictions are off by about
$15,363"). RMSE (Root Mean Squared Error) squares errors before averaging, so it penalises large
errors more heavily than small ones — useful when a few very wrong predictions matter more than
many slightly-wrong ones. RMSE is always >= MAE for the same predictions; here it's meaningfully
higher, meaning a handful of large errors are dragging it up.

## Part 5: A classification model — and a humbling result (4 min)

Build a `LogisticRegression` predicting `side` (BUY/SELL) from `quantity` and `value`. Compute
accuracy on the test set, and compare against a `DummyClassifier` that always predicts the
majority class.

Run it: the trained model's accuracy (0.5) is **worse** than the naive majority-class baseline
(≈0.67). Narration: this is exactly why accuracy alone, without a baseline comparison, can be
misleading — 50% sounds like "better than a coin flip is likely," but it isn't better than just
always guessing the more common class here. With only 20 rows total and a 6-row test set, this
result is also extremely noisy; don't over-interpret one small-sample run either way.

## Key message

A predictive model's evaluation metric is only meaningful next to a baseline. MAE and RMSE both
describe regression error, but in different ways; accuracy describes classification correctness,
but only tells you something once compared against the naive "always guess the common answer"
result.
