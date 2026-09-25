"""Extension 3: a shallow decision tree, and the rules it learned."""
import pandas as pd
from sklearn.metrics import confusion_matrix, precision_score, recall_score
from sklearn.tree import DecisionTreeClassifier, export_text

from fraud_model import FEATURES, fraud_pipeline, load_features, split

df = load_features()
X_train, X_test, y_train, y_test = split(df)

# Trees split on thresholds, so they do not need scaled features.
tree = DecisionTreeClassifier(max_depth=3, random_state=42).fit(X_train, y_train)
print("Rules learned by the tree (max_depth=3):")
print(export_text(tree, feature_names=FEATURES))

train_rows = df.loc[X_train.index]
print("Training rows with hour <= 5:")
print(train_rows[train_rows["hour"] <= 5]["is_fraud"].value_counts().rename({0: "legitimate", 1: "fraud"}).to_string())

logit = fraud_pipeline(class_weight="balanced").fit(X_train, y_train)
for name, model in [("Decision tree", tree), ("Logistic, balanced", logit)]:
    preds = model.predict(X_test)
    tn, fp, fn, tp = confusion_matrix(y_test, preds, labels=[0, 1]).ravel()
    print(f"{name:<20} recall {recall_score(y_test, preds, zero_division=0):.2f}  "
          f"precision {precision_score(y_test, preds, zero_division=0):.2f}  "
          f"TP {tp}  FP {fp}  FN {fn}")
    flagged = df.loc[X_test.index[preds == 1], "txn_id"].tolist()
    print(f"  flagged: {flagged}")

# The tree needed only one split: every training fraud happened between 00:00 and 05:00, and
# no legitimate training transaction did, so "hour <= 5" separates the training data
# perfectly and the tree stops growing. On the test rows it flags P0045 and P0043 (both fraud)
# and nothing else: precision 1.00, recall 0.50. It avoids the logistic model's false alarm on
# P0100 (07:34) but misses the same two frauds, P0088 (23:04) and P0136 (14:19). The tree is
# easier to explain to a fraud team ("flag anything before 06:00") but it has learned one fact
# about 8 training frauds; any fraud outside those hours will pass.
