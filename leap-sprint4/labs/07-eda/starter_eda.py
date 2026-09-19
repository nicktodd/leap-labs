from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[2] / "shared" / "trades.csv"
df = pd.read_csv(DATA_PATH)

# TODO:
# 1. Print df.shape and describe() on the numeric columns.
# 2. Segment by currency: count and mean value per currency. Note the mixing anomaly.
# 3. Segment by client_name: highest total value, and highest trade count (may differ).
# 4. Segment by instrument, within asset_class == "Equity" only: highest total value.
# 5. Write one pattern, one anomaly, and one specific, checkable hypothesis as comments.
