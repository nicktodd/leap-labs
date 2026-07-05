from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[2] / "shared" / "messy-trades-raw.csv"

df = pd.read_csv(DATA_PATH)

# TODO, each with a one-line comment explaining your reasoning:
# 1. Drop the row with missing quantity (can't be safely reconstructed).
# 2. Recompute the missing value as quantity * price.
# 3. Backfill the missing client_name from another row with the same client_id.
# 4. Parse trade_date correctly, resolving the ambiguous DD/MM/YYYY row using the
#    surrounding trade_id sequence, not an assumption.
# 5. Normalise asset_class casing without turning "ETF" into "Etf" (use a canonical mapping).
# 6. Drop the exact duplicate row.
# 7. Flag (don't drop) the quantity outlier, with a one-sentence investigation note.

print(f"Final row count: {len(df)}")
