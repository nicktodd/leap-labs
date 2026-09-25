"""Extension 4: Module 4's hand-written fraud rules, scored as a classifier.

Rules (as in the Module 4 lab):
  HIGH_VALUE   amount_gbp > 500
  FOREIGN      country differs from the customer's home_country in customers.csv
  NIGHT_ONLINE channel is Online and the time is 00:00-04:59
A transaction is predicted as fraud if ANY rule fires.
"""
import pandas as pd
from sklearn.metrics import confusion_matrix, precision_score, recall_score

from fraud_model import fraud_pipeline, load_features, split

df = load_features()
X_train, X_test, y_train, y_test = split(df)

# load_features() already computes is_foreign against home_country, with K012 assumed GB.
rules = pd.DataFrame({
    "HIGH_VALUE": df["amount_gbp"] > 500,
    "FOREIGN": df["is_foreign"] == 1,
    "NIGHT_ONLINE": (df["channel"] == "Online") & (df["hour"] < 5),
})
df["any_rule"] = rules.any(axis=1).astype(int)


def score(name, y_true, preds):
    tn, fp, fn, tp = confusion_matrix(y_true, preds, labels=[0, 1]).ravel()
    print(f"  {name:<20} recall {recall_score(y_true, preds, zero_division=0):.2f}  "
          f"precision {precision_score(y_true, preds, zero_division=0):.2f}  "
          f"TP {tp}  FP {fp}  FN {fn}  TN {tn}")


logit = fraud_pipeline(class_weight="balanced").fit(X_train, y_train)
print("Same 42 test rows (4 fraud):")
score("Any rule fires", y_test, df.loc[X_test.index, "any_rule"])
score("Logistic, balanced", y_test, logit.predict(X_test))

test = df.loc[X_test.index].join(rules)
flagged = test[(test["any_rule"] == 1) | (test["is_fraud"] == 1)]
print("\nTest rows that are fraud or flagged by a rule:")
print(flagged[["txn_id", "customer_id", "amount_gbp", "hour", "channel", "country", "home_country",
               "HIGH_VALUE", "FOREIGN", "NIGHT_ONLINE", "is_fraud"]].round(2).to_string(index=False))

# The rules need no training, so they can also be scored on all 140 rows.
print("\nAll 140 rows:")
score("Any rule fires", df["is_fraud"], df["any_rule"])

# On the test rows the rules catch all 4 frauds (recall 1.00) but raise 5 false alarms
# (precision 0.44): K004's holiday spending in Spain three times, and K007's US trip twice.
# The balanced model catches 2 of 4 with 1 false alarm. On all 140 rows the rules catch all 12
# frauds with 11 false alarms. The rules win on recall because a human wrote them with the
# known fraud patterns in mind, including a HIGH_VALUE rule that catches K011's GBP 780 cloned
# card; the model never saw a daytime in-store fraud in training. The rules lose on precision
# because FOREIGN cannot tell a holiday from a stolen card. A practical design combines them:
# rules as a safety net, the model's probability to rank the alerts for an analyst.
