"""Extension 1: threshold tuning with predict_proba.

model.predict() uses a fixed threshold of 0.5 on the predicted fraud probability. A fraud team
can choose a different threshold: lower means more alerts (higher recall, lower precision),
higher means fewer, surer alerts.
"""
import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score

from fraud_model import fraud_pipeline, load_features, split

df = load_features()
X_train, X_test, y_train, y_test = split(df)
model = fraud_pipeline(class_weight="balanced").fit(X_train, y_train)

# Column 1 of predict_proba is the probability of class 1 (fraud).
proba = model.predict_proba(X_test)[:, 1]

rows = []
for threshold in np.round(np.arange(0.1, 1.0, 0.1), 1):
    preds = (proba >= threshold).astype(int)
    rows.append({
        "threshold": threshold,
        "flagged": preds.sum(),
        "frauds_caught": int(((preds == 1) & (y_test == 1)).sum()),
        "precision": precision_score(y_test, preds, zero_division=0),
        "recall": recall_score(y_test, preds, zero_division=0),
    })
print("Balanced logistic regression, 42 test rows (4 fraud):")
print(pd.DataFrame(rows).round(2).to_string(index=False))

scores = df.loc[X_test.index, ["txn_id", "customer_id", "amount_gbp", "hour", "channel", "is_fraud"]].copy()
scores["fraud_probability"] = proba
print("\nHighest-scoring test rows, plus every fraud row:")
top = scores.sort_values("fraud_probability", ascending=False)
print(pd.concat([top.head(6), top[top["is_fraud"] == 1]]).drop_duplicates()
      .round({"amount_gbp": 2, "fraud_probability": 4}).to_string(index=False))

# Reading the table: from 0.3 to 0.7 the model flags the same 3 rows (precision 0.67, recall
# 0.50). Lowering the threshold to 0.1 doubles the alerts to 8 but catches no extra fraud, so
# precision falls to 0.25 while recall stays at 0.50. Raising it to 0.8 drops P0043 (probability
# about 0.77) and recall falls to 0.25. The two missed frauds, P0088 and P0136, have
# probabilities far below 0.1: no threshold in this range recovers them. Threshold tuning can
# only trade between rows the features already separate; it cannot fix missing signal.
