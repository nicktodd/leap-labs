# Module 13 Lab - Model Answer Notes

See `fraud_model.py` (core, Parts A and B). The extension files import `load_features()` and
`split()` from it. Verified results against `shared/transactions.csv`:

## Part A - fraud classification

- `is_foreign` is defined as `country != home_country`, using a left merge with `customers.csv`.
  K003 (home FR) and K008 (home IE) would otherwise have every purchase marked foreign. K012's 10
  rows have no home country; all are in GB about 20 km from home, so GB is assumed and flagged in a
  `home_country_assumed` column. On this split both definitions give the same dummy and plain
  model results; the home-country version gives the balanced model one fewer false alarm (with
  `country != "GB"` it also flags P0025, a GBP 32.68 purchase by K008 in her home country IE).
- Stratified split: 98 training rows (8 fraud), 42 test rows (4 fraud: P0045, P0088, P0136,
  P0043). Each test fraud is worth 0.25 of recall.

| Model | Accuracy | Recall | Precision | TP | FP | FN | TN |
|---|---|---|---|---|---|---|---|
| Dummy (most frequent) | 0.905 | 0.00 | 0.00 | 0 | 0 | 4 | 38 |
| Logistic regression | 0.905 | 0.25 | 0.50 | 1 | 1 | 3 | 37 |
| Logistic, `class_weight="balanced"` | 0.929 | 0.50 | 0.67 | 2 | 1 | 2 | 37 |

- Both logistic models flag P0045 (GBP 1,012.76 Apple Store, US, 02:10) and falsely flag P0100
  (K007's legitimate GBP 1,202.97 British Airways booking from the US at 07:34). The balanced
  model also catches P0043 (K009's GBP 1.50 card-testing charge at 01:33).
- Both miss P0088 (GBP 857.47 Currys, FR, 23:04) and P0136 (K011's GBP 780.00 cloned card,
  in-store, GB, 14:19).
- Balanced model coefficients on standardised features: hour -2.50, is_online 0.80, amount_gbp
  0.73, is_foreign 0.72, distance_from_home_km -0.28. Hour dominates. Distance is weakly negative,
  most likely because it overlaps heavily with is_foreign and the legitimate far-from-home trips
  pull against it; with 8 training frauds, individual coefficients should not be over-read.
- On this split class weighting improves recall AND precision. The classic trade-off (more
  recall, lower precision) is visible in Extension 1, not in the core comparison. Delegates should
  report what they observe rather than the textbook expectation.

## Part B - forecasting

- 28 daily totals of approved `amount_gbp`. Held-out week Mon 23 Feb to Sun 1 Mar: actual average
  GBP 568.41 a day, training mean GBP 356.79 a day.
- MAE: training mean GBP 384.86, naive GBP 529.63, seasonal naive GBP 512.08. The mean wins.
- Weekly approved totals: GBP 1,448.98 (27 transactions), GBP 2,323.38 (34), GBP 3,720.32 (30),
  GBP 3,978.87 (36). Excluding the 5 approved confirmed-fraud rows: GBP 1,448.98, GBP 1,908.34,
  GBP 1,575.01, GBP 3,198.87.
- Why the mean wins: daily totals are dominated by one-off large purchases. Sun 22 Feb's GBP
  2,730.79 includes the GBP 2,145.31 fraudulent flight (P0094). Naive copies it onto Mon 23 Feb and
  seasonal naive copies it onto Sun 1 Mar, which produces their largest errors.
- Why payday matters: the held-out week is the payday week, the busiest of the month (36
  transactions; highest genuine spend). Training data contains no payday, so every method
  under-forecasts the week on average. A monthly cycle cannot be learned from one month.

Key points to check in a delegate's solution:

- **Accuracy is not the headline.** A delegate who reports "the model is 90% accurate" without
  noting the dummy's identical 0.905 has missed the main point of the lab.
- **`zero_division=0` is used**, so the dummy's precision prints as 0.00 rather than raising a
  warning.
- **The scaler is inside the Pipeline**, fitted on training rows only. Scaling the full dataset
  before splitting leaks test information.
- **The small test set is stated explicitly**: 4 frauds, 0.25 of recall per row.
- **The missed frauds are named and explained** (a 23:04 fraud that a linear `hour` feature treats
  as evening; a cloned card that looks normal on every feature), not only counted.
- **The manager paragraph uses money and people**, not metric names: GBP 780.00 lost on P0136 as
  a false negative; a Business customer's GBP 1,202.97 flight blocked as a false positive.
- **The `is_foreign` choice is justified**, and K012 is handled by a visible assumption, not an
  inner join that silently drops 10 rows.
- **Part B's comment is honest**: the simplest method wins, and the reason is in the data (spikes,
  payday), not a claim that naive methods are always bad.

## Extension notes

**E1 - Threshold tuning** (`ext1_threshold_tuning.py`). From 0.3 to 0.7 the balanced model flags
the same 3 rows (precision 0.67, recall 0.50). At 0.2 it flags 4 (precision 0.50); at 0.1 it
flags 8 with no extra fraud caught (precision 0.25, recall 0.50). At 0.8 and 0.9 it loses P0043
(probability 0.768) and recall falls to 0.25. P0136 (0.0136) and P0088 (0.0121) sit far below
every threshold. Good answers conclude that thresholds only trade between rows the features
already separate. A common pitfall is using `predict_proba(X_test)[:, 0]`, the probability of
the legitimate class, which inverts the table.

**E2 - Cross-validation** (`ext2_cross_validation.py`). Folds contain 2, 2, 2, 3 and 3 frauds.
Plain model: recall per fold 0.5, 1.0, 0.5, 0.33, 0.67 (mean 0.60, sample standard deviation
0.25); precision mean 0.83 (standard deviation 0.24). Balanced model: recall 1.0, 1.0, 0.5, 0.67,
1.0 (mean 0.83, standard deviation 0.24); precision mean 0.88 (standard deviation 0.16). The
core split's recall of 0.50 is the lowest fold value, which shows how much a single split depends
on which frauds land in the test set. Pitfalls: forgetting `shuffle=True` (then `random_state`
has no effect), and quoting means without the spread.

**E3 - Decision tree** (`ext3_decision_tree.py`). The tree has a single split, `hour <= 5.00`,
despite `max_depth=3`: all 8 training frauds happened before 05:00 and no legitimate training
transaction did, so one split separates the training data perfectly. On test it flags P0045 and
P0043 only: precision 1.00, recall 0.50 (it avoids P0100, which the logistic model flags). Good
answers inspect the training rows to explain why the tree stopped, and note that it would miss
any daytime fraud. Pitfall: calling the tree "better" because precision is 1.00 on 2 flags.

**E4 - Rules vs models** (`ext4_rules_vs_models.py`). On the 42 test rows "any rule fires" has
recall 1.00 and precision 0.44 (TP 4, FP 5). The 5 false alarms are all FOREIGN: K004's Spanish
holiday (P0064, P0079, P0082) and K007's US trip (P0100, P0109). P0136 is caught only by
HIGH_VALUE, and P0043 only by NIGHT_ONLINE. On all 140 rows the rules catch all 12 frauds with 11
false alarms (precision 0.52). Good answers recognise that the rules were written with knowledge
of the fraud patterns, so their recall is not an independent test, and propose combining rules
and model scores. Pitfall: using `country != "GB"` for FOREIGN, which marks K003's and K008's home-country purchases as
foreign: false alarms rise from 5 to 10 on the test rows and from 11 to 19 on all 140 rows.
