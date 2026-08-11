"""Lab 13: Predictive analytics — linear regression on trade value."""

import numpy as np
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

DATA_PATH = Path(r"C:\Users\zackt\Documents\leap-sprint4\shared\trades.csv")
df = pd.read_csv(DATA_PATH)

# Features and target
X = df[["quantity", "price"]]
y = df["value"]

# 2. Split with test_size=0.3, random_state=42 for reproducibility
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 1. Linear regression model
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# 3. Evaluate with MAE and RMSE
model_mae = mean_absolute_error(y_test, y_pred)
model_rmse = mean_squared_error(y_test, y_pred) ** 0.5
print(f"LinearRegression — MAE: ${model_mae:,.2f}   RMSE: ${model_rmse:,.2f}")

# 4. DummyRegressor (mean) baseline
dummy = DummyRegressor(strategy="mean")
dummy.fit(X_train, y_train)
y_dummy = dummy.predict(X_test)
dummy_mae = mean_absolute_error(y_test, y_dummy)
dummy_rmse = mean_squared_error(y_test, y_dummy) ** 0.5
print(f"DummyRegressor    — MAE: ${dummy_mae:,.2f}   RMSE: ${dummy_rmse:,.2f}")

print(f"\nModel vs baseline MAE improvement: ${dummy_mae - model_mae:,.2f}")

# 5. Investigate: compare quantity * price to actual value
df["computed_value"] = df["quantity"] * df["price"]
df["value_diff"] = (df["value"] - df["computed_value"]).abs()
disagreements = df[df["value_diff"] > 0.01][["trade_id", "asset_class", "instrument",
                                              "quantity", "price", "value", "computed_value"]]
print("\nRows where value != quantity * price:")
print(disagreements.to_string(index=False))

# 6. Pattern explanation:
# Bond trades (US10Y) have value = quantity * (price / 100), not quantity * price directly.
# Bond prices are quoted as a percentage of face value (par), so US10Y at 98.75 means
# 98.75% of $100 face value per unit. The model cannot infer this pricing convention from
# quantity and price alone — it's a domain rule, not something a generic linear regression
# will discover from 20 rows.

# 7. Plain-English stakeholder explanation:
# The MAE tells us that, on average, this model's predictions are off by roughly the amount
# shown above compared to the actual trade values. The model failed to clearly beat a naive
# "always predict the mean" baseline because bond trades follow a different pricing rule:
# their value is quantity × (price ÷ 100), not quantity × price like equities and ETFs.
# Without knowing this, the model learns contradictory patterns from the same two features.
# To fix it before trying again, we would engineer a new feature — "correctly computed value
# per asset class" — where bonds use the percentage-of-par formula and everything else uses
# the direct product. With that feature, or with a separate model per asset class, the
# regression would almost certainly achieve near-zero error.
