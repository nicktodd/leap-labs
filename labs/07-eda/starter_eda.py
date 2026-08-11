"""Lab 07: Exploratory Data Analysis on the mission dataset."""

from pathlib import Path
import pandas as pd

DATA_PATH = Path(r"C:\Users\zackt\Documents\leap-sprint4\shared\trades.csv")
df = pd.read_csv(DATA_PATH)

# 1. Shape and describe
print("Shape:", df.shape)
print("\nDescribe (numeric columns):")
print(df.describe())

# 2. Segment by currency
print("\n--- Currency segmentation ---")
currency_group = df.groupby("currency")["value"].agg(count="count", mean_value="mean")
print(currency_group)
# ANOMALY NOTE (addressed in step 5): USD and GBP values are summed in the same column
# but are not directly comparable without FX conversion — combining them would produce
# a meaningless aggregate.

# 3. Segment by client_name
print("\n--- Client segmentation ---")
client_total = df.groupby("client_name")["value"].sum().sort_values(ascending=False)
client_count = df.groupby("client_name")["value"].count().sort_values(ascending=False)
print("Highest total value:", client_total.index[0], f"${client_total.iloc[0]:,.2f}")
print("Most individual trades:", client_count.index[0], f"({client_count.iloc[0]} trades)")

# 4. Equity instruments only — highest total value
print("\n--- Equity instrument segmentation ---")
equity_df = df[df["asset_class"] == "Equity"]
equity_instrument = equity_df.groupby("instrument")["value"].sum().sort_values(ascending=False)
print("Highest-value equity instrument:", equity_instrument.index[0], f"${equity_instrument.iloc[0]:,.2f}")
print(equity_instrument)

# 5. Pattern, anomaly, hypothesis
# PATTERN: J. Okafor is the advisor for the three clients with the highest individual trade
#          values (Alice Chen $38,092, Jamal Ferris $37,510, Ben Whitfield $35,191), suggesting
#          the Growth team consistently handles larger accounts than Income or the other Growth advisor.
#
# ANOMALY: Trades denominated in GBP (Elliot Park's VUSA trades) and USD are stored in the same
#          'value' column without a currency conversion factor, so any aggregate across all clients
#          silently mixes currencies and overstates or understates the true total depending on the
#          GBP/USD exchange rate on each trade date.
#
# HYPOTHESIS (checkable with Module 8 t-test): Clients advised by J. Okafor have a statistically
#             significantly higher mean trade value than clients advised by R. Alvarez or S. Rahman,
#             which can be confirmed or rejected with a two-sample t-test on the 'value' column
#             segmented by advisor.

print("\n--- Advisory team mean trade value ---")
print(df.groupby("advisor")["value"].mean().sort_values(ascending=False))
