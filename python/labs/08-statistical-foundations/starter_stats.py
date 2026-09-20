from pathlib import Path
import pandas as pd
from scipy import stats

DATA_PATH = Path(__file__).resolve().parents[2] / "shared" / "trades.csv"
df = pd.read_csv(DATA_PATH)

# TODO:
# 1. Calculate skew of quantity and value; comment on what each tells you about shape.
# 2. Calculate pearsonr(quantity, value); comment on r and p together.
# 3. Discuss and comment: would a strong correlation here prove causation?
# 4. ttest_ind comparing BUY vs SELL value; interpret against 0.05, with a small-sample caveat.
