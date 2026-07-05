from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

DATA_PATH = Path(__file__).resolve().parents[2] / "shared" / "trades.csv"
df = pd.read_csv(DATA_PATH)

# TODO:
# 1. LinearRegression predicting value from quantity and price.
# 2. train_test_split(test_size=0.3, random_state=42).
# 3. Evaluate with MAE and RMSE on the test set.
# 4. DummyRegressor(strategy="mean") baseline, evaluated the same way, and compared.
# 5. Investigate: compute quantity * price per row, compare to actual value, find the
#    asset_class where they disagree.
# 6. Comment: what's actually different about how value is calculated for that class?
# 7. Comment: plain-English explanation of the MAE, why the model underperformed, and
#    what feature engineering would fix it.
