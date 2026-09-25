# Module 13 Lab - Predictive Analytics, Forecasting & Model Evaluation

## Scenario

PaySprint's fraud-operations team reviews suspicious card transactions by hand and wants to know
whether a simple model could help them prioritise. Only 12 of the month's 140 transactions are
confirmed fraud, so the usual "percentage correct" score will mislead you. The finance team also
wants a first forecast of daily card spend, and needs to know which simple method to trust.

## Objectives

By the end of this lab you will have:

- Engineered model features from raw transaction columns and reference data
- Split an imbalanced dataset with stratification, and explained why it matters with few positives
- Evaluated classifiers with recall, precision and a confusion matrix against a naive baseline,
  and explained why accuracy alone is misleading
- Used class weighting to change the balance between missed fraud and false alarms
- Compared three baseline forecasts of a daily time series on a held-out week
- Explained model results in plain English to a non-technical manager

## Setup

- `pip install pandas scikit-learn`
- Data files in `shared/` (repo root): `transactions.csv`, `fx_rates.csv`, `customers.csv`
- Starter file: `starter_fraud_model.py`, in `labs/13-predictive-analytics/`. Run it with
  `python labs/13-predictive-analytics/starter_fraud_model.py` from any folder.

## The data

`transactions.csv`: one row per card transaction, 2 Feb to 1 Mar 2026. The columns this lab uses:
`txn_timestamp`, `customer_id`, `channel` (`Online`, `In-store`, `Contactless`), `country` (ISO
code, where the card was used), `currency`, `amount` (in `currency`), `status` (`APPROVED` /
`DECLINED`), `distance_from_home_km`, and `is_fraud` (1 = confirmed fraud by the fraud team).

`fx_rates.csv` gives `rate_to_gbp` per currency (FX, foreign exchange): `amount_gbp = amount *
rate_to_gbp`. `customers.csv` gives each customer's `home_country`. Customer K012 has
transactions but no row in `customers.csv`.

### Terms used throughout this lab

For a fraud classifier, "positive" means "predicted fraud".

- **TP (true positive)**: a fraud the model flagged.
- **FP (false positive)**: a legitimate transaction the model flagged (a false alarm).
- **FN (false negative)**: a fraud the model did not flag (a missed fraud).
- **TN (true negative)**: a legitimate transaction the model left alone.
- **Precision** = TP / (TP + FP): of the transactions flagged, the share that were fraud.
- **Recall** = TP / (TP + FN): of the frauds, the share the model flagged.
- **Accuracy** = (TP + TN) / all rows: the share of all predictions that were correct.
- **MAE (mean absolute error)**: the average size of a forecast's error, in GBP.

`confusion_matrix(y_true, y_pred)` returns `[[TN, FP], [FN, TP]]` for 0/1 labels.

## Task

### Part A - fraud classification

1. In `load_features()`, build these features: `amount_gbp`, `distance_from_home_km`, `hour`
   (from `txn_timestamp`), `is_online` (1 if `channel == "Online"`), and `is_foreign`. Choose how
   to define `is_foreign`: either `country != "GB"`, or `country` differs from the customer's
   `home_country` in `customers.csv`. Look at customers K003 and K008 before you decide. If you
   use `customers.csv`, handle K012 deliberately (a left merge, then a documented assumption)
   rather than silently dropping her rows. Justify the choice in a comment. The target is
   `is_fraud`.
2. Split with `train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)`. Print how many
   fraud rows are in the training and test sets, and which `txn_id`s the test frauds are. In a
   comment, explain what `stratify` does and why it matters when there are only 12 positives.
3. Fit a `DummyClassifier(strategy="most_frequent")` and print its accuracy, recall and precision
   on the test set. Use `zero_division=0` in `precision_score` and `recall_score`.
4. Fit a `Pipeline` of `StandardScaler` then `LogisticRegression`. Print the same three metrics
   and the `confusion_matrix`. Print the test rows that are fraud or were flagged, so you can see
   which frauds were caught and which were missed. In a comment, explain why accuracy looks good
   for both the dummy and this model.
5. Repeat step 4 with `LogisticRegression(class_weight="balanced")`. Compare recall and precision
   with step 4, and discuss the trade-off between them. If the test set contains very few fraud
   rows, say how many, and what one row more or less does to recall.
6. Write a plain-English paragraph (as a comment) for a fraud-operations manager: what a false
   negative costs PaySprint here, what a false positive costs, and what your model would mean for
   their team. Cite specific transactions and numbers from your output. Report what the model
   produces: if a result is disappointing, say so.

### Part B - forecasting daily spend

7. Keep only `APPROVED` transactions and resample `amount_gbp` to daily totals with
   `resample("D")`. You should have 28 days, Mon 2 Feb to Sun 1 Mar.
8. Hold out the final 7 days as the test period. Forecast each of those days three ways:
   - the mean of the 21 training days
   - naive: the previous day's actual value (`shift(1)`)
   - seasonal naive: the actual value on the same weekday one week earlier (`shift(7)`)
9. Print a table of actual vs each forecast, and the MAE of each forecast. In a comment, say which
   method wins and why, with reference to the large one-off transactions in the series. Print the
   weekly totals and explain why it matters that payday (Fri 27 Feb) falls in the held-out week.

## Acceptance criteria

- The script runs with no errors or warnings from any folder.
- `is_foreign` has a stated definition and justification; K012's 10 rows are kept.
- The stratified split puts 8 fraud rows in the 98-row training set and 4 in the 42-row test set.
- The dummy classifier scores accuracy 0.905 with recall 0.00: every model's accuracy is at least
  0.905, and your comment explains why that number says little.
- Recall, precision and the confusion matrix are printed for the dummy, the plain model and the
  balanced model, and the comparison names the specific frauds each model misses.
- The manager paragraph describes a false negative and a false positive in business terms (money,
  analyst time, customer experience), with specific numbers from your output.
- Part B has 28 daily values; the three MAEs are printed; with approved `amount_gbp`, the
  training-mean forecast's MAE is GBP 384.86.

## Extension exercises

1. **Threshold tuning.** `predict()` uses a 0.5 threshold on the predicted probability. Use
   `predict_proba(X_test)[:, 1]` from the balanced model and, for thresholds 0.1, 0.2, ..., 0.9,
   print the number flagged, precision and recall. Done: a table plus a comment on which
   threshold you would recommend and whether any threshold catches the frauds the model missed.
2. **Cross-validation.** Use `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` with
   `cross_validate` to score recall and precision for the plain and balanced pipelines. Print each
   fold's scores, the mean and the standard deviation. Done: a comment explaining why a single
   train/test split is unreliable with 12 positives, using the spread you observed.
3. **Decision tree.** Fit `DecisionTreeClassifier(max_depth=3, random_state=42)` on the same
   training rows and print its rules with `export_text`. Done: the rules printed, test-set recall
   and precision compared with the balanced logistic model, and a comment on why the tree looks
   the way it does (inspect the training rows it splits on).
4. **Rules vs models.** Score Module 4's hand-written rules as a classifier on the same 42 test
   rows: HIGH_VALUE (`amount_gbp` > GBP 500), FOREIGN (country differs from `home_country` in
   `customers.csv`, with K012 handled as in step 1), NIGHT_ONLINE (Online, 00:00-04:59). Predict
   fraud if any rule fires. Done: recall and precision for the rules next to the models, the
   false alarms listed by customer, and a comment on when you would use each approach.
