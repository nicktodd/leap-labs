from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

DATA_PATH = Path(__file__).resolve().parents[2] / "shared" / "trades.csv"
df = pd.read_csv(DATA_PATH)

X = df[["quantity", "price"]]
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

print(f"Model    MAE: {mae:,.2f}  RMSE: {rmse:,.2f}")
print(f"Baseline MAE: {base_mae:,.2f}  RMSE: {base_rmse:,.2f}")
# The model does NOT clearly beat the baseline here (MAE ~16,513 vs. ~15,630) — a
# surprising result, since value looks like a simple function of quantity and price.

# Investigate: compare quantity * price to the actual value, per row
df["calc_value"] = df["quantity"] * df["price"]
df["disagrees"] = (df["calc_value"] - df["value"]).abs() > 0.01
print("\nRows where quantity * price != value:")
print(df.loc[df["disagrees"], ["trade_id", "asset_class", "quantity", "price", "value", "calc_value"]])

# The pattern: every disagreeing row is a Bond trade. Bonds are quoted per 100 of face
# value (a standard bond-market convention) -- so for Bonds, value = quantity * price / 100,
# not quantity * price directly, the way every other asset class in this dataset works.
# A plain LinearRegression on raw quantity and price can't learn this "divide by 100, but
# only for Bonds" rule -- it's a categorical interaction, not something a linear
# combination of quantity and price alone can represent.

# Plain-English explanation: on average, this model's predictions are off by about
# $16,513 (the MAE) -- and that's not meaningfully better than just always guessing the
# training set's average value (~$15,630 MAE), so this model isn't actually useful yet.
# The root cause is a hidden asset-class-specific rule (the Bond pricing convention) that
# quantity and price alone don't capture. The fix isn't a fancier model -- it's better
# feature engineering: compute value correctly per asset class first (or add asset_class
# as a feature the model can condition on), rather than expecting quantity and price
# alone to encode a rule that depends on which market convention applies.
