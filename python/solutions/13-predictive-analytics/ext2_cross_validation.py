"""Extension 2: stratified 5-fold cross-validation of recall and precision.

One 70/30 split leaves 4 fraud rows in the test set, so each one moves recall by 0.25.
Cross-validation tests on every row exactly once and shows how much the score varies.
"""
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_validate

from fraud_model import FEATURES, fraud_pipeline, load_features

df = load_features()
X, y = df[FEATURES], df["is_fraud"]

# StratifiedKFold keeps 2 or 3 fraud rows in every fold (12 / 5). shuffle=True with a fixed
# random_state gives the same folds on every run.
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for label, weight in [("plain", None), ("balanced", "balanced")]:
    scores = cross_validate(fraud_pipeline(class_weight=weight), X, y, cv=cv,
                            scoring=["recall", "precision"])
    recall = pd.Series(scores["test_recall"])
    precision = pd.Series(scores["test_precision"])
    print(f"Logistic regression, {label}:")
    print(f"  recall per fold    {recall.round(2).tolist()}")
    print(f"  precision per fold {precision.round(2).tolist()}")
    # pandas .std() is the sample standard deviation (ddof=1).
    print(f"  recall    mean {recall.mean():.2f}  standard deviation {recall.std():.2f}")
    print(f"  precision mean {precision.mean():.2f}  standard deviation {precision.std():.2f}\n")

print("Fraud rows per test fold:", [int(y.iloc[test].sum()) for _, test in cv.split(X, y)])

# Across the five folds the balanced model's recall ranges from 0.50 to 1.00, and the plain
# model's from 0.33 to 1.00. The single split in the core task (recall 0.50 for the balanced
# model) happens to sit at the bottom of that range. With 2 or 3 positives per fold, one fraud
# row decides the score, so one split is closer to an anecdote than a measurement. The mean
# and standard deviation across folds are the figures to quote, and even they rest on 12 frauds.
