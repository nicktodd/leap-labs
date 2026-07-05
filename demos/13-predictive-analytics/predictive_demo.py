from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.dummy import DummyRegressor, DummyClassifier
from sklearn.metrics import mean_absolute_error, mean_squared_error, accuracy_score

DATA_PATH = Path(__file__).resolve().parents[2] / "shared" / "trades.csv"
df = pd.read_csv(DATA_PATH)

# --- Part 3: regression, evaluated honestly ---
X = df[["quantity"]]
y = df["value"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = LinearRegression().fit(X_train, y_train)
preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)
rmse = mean_squared_error(y_test, preds) ** 0.5

baseline = DummyRegressor(strategy="mean").fit(X_train, y_train)
base_preds = baseline.predict(X_test)
base_mae = mean_absolute_error(y_test, base_preds)
base_rmse = mean_squared_error(y_test, base_preds) ** 0.5

print("Regression: predicting value from quantity")
print(f"  Model    MAE: {mae:,.2f}  RMSE: {rmse:,.2f}")
print(f"  Baseline MAE: {base_mae:,.2f}  RMSE: {base_rmse:,.2f}  (always predicts the training mean)")
print(
    "  The model barely beats the baseline -- consistent with Module 8's weak "
    "quantity/value correlation. quantity alone isn't a strong predictor of value."
)

# --- Part 5: classification, a humbling result ---
Xc = df[["quantity", "value"]]
yc = (df["side"] == "BUY").astype(int)
Xc_train, Xc_test, yc_train, yc_test = train_test_split(
    Xc, yc, test_size=0.3, random_state=42, stratify=yc
)

clf = LogisticRegression().fit(Xc_train, yc_train)
clf_preds = clf.predict(Xc_test)
accuracy = accuracy_score(yc_test, clf_preds)

base_clf = DummyClassifier(strategy="most_frequent").fit(Xc_train, yc_train)
base_clf_preds = base_clf.predict(Xc_test)
base_accuracy = accuracy_score(yc_test, base_clf_preds)

print("\nClassification: predicting side (BUY/SELL) from quantity and value")
print(f"  Model    accuracy: {accuracy:.2f}")
print(f"  Baseline accuracy: {base_accuracy:.2f}  (always predicts the majority class)")
print(
    "  The model is WORSE than the naive baseline here -- accuracy alone, without a "
    "baseline comparison, would have made 0.50 sound reasonable. It isn't, in this case."
)
