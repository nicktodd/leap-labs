from pathlib import Path

import pandas as pd

SHARED = Path(__file__).resolve().parents[2] / "shared"

df = pd.read_csv(SHARED / "transactions.csv", parse_dates=["txn_timestamp"])

# The .dt accessor exposes datetime parts for a whole column at once. It only works
# because parse_dates made txn_timestamp a datetime64 column; on text it raises an error.
df["hour"] = df["txn_timestamp"].dt.hour
df["day_name"] = df["txn_timestamp"].dt.day_name()
print(df[["txn_id", "txn_timestamp", "hour", "day_name"]].head())

# value_counts() sorts by count, and sort_index() would sort alphabetically
# (Friday, Monday, ...). reindex() with an explicit list gives calendar order.
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
by_weekday = df["day_name"].value_counts().reindex(WEEKDAYS, fill_value=0)
print("\nTransactions by weekday (Monday-Sunday):")
print(by_weekday)

# Alternative: an ordered Categorical keeps the order through later groupby calls too.
df["day_name"] = pd.Categorical(df["day_name"], categories=WEEKDAYS, ordered=True)
print("\nSame counts via an ordered Categorical and groupby:")
print(df.groupby("day_name", observed=False)["txn_id"].count())

print(f"\nBusiest hour of the day: {df['hour'].value_counts().idxmax()}:00 "
      f"({df['hour'].value_counts().max()} transactions)")
