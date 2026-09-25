from pathlib import Path
import pandas as pd

SHARED = Path(__file__).resolve().parents[2] / "shared"

txns = pd.read_csv(SHARED / "transactions.csv")
customers = pd.read_csv(SHARED / "customers.csv")

# A left merge keeps every transaction, including those whose customer has no reference row.
# indicator=True adds a _merge column that shows which rows found a match.
merged = txns.merge(
    customers[["customer_id", "home_country"]],
    on="customer_id", how="left", validate="many_to_one", indicator=True,
)
print("merge result:")
print(merged["_merge"].value_counts().to_string())
unmatched = merged[merged["_merge"] == "left_only"]
print(f"transactions with no customers.csv row: {len(unmatched)} "
      f"(customers: {', '.join(unmatched['customer_id'].unique())})")

# Without a home_country, "foreign" cannot be decided. Comparing country != NaN would be True
# for every K012 row and silently count them all as foreign, so label them separately.
merged["location"] = "Domestic"
merged.loc[merged["country"] != merged["home_country"], "location"] = "Foreign"
merged.loc[merged["home_country"].isna(), "location"] = "Unknown home"

summary = merged.groupby("location").agg(
    txn_count=("txn_id", "count"), fraud=("is_fraud", "sum"), fraud_rate=("is_fraud", "mean")
)
print("\nFraud rate by location relative to the customer's home country:")
print(summary.round(3).to_string())

foreign_legit = merged[(merged["location"] == "Foreign") & (merged["is_fraud"] == 0)]
print("\nForeign transactions that are not fraud, by customer and country:")
print(foreign_legit.groupby(["customer_id", "country"]).size().to_string())

# K003 (home FR) and K008 (home IE) spend in their home countries in EUR. Using
# "country != 'GB'" as the foreign test would count those as foreign; comparing with each
# customer's home_country does not.
naive_foreign = (merged["country"] != "GB").sum()
print(f"\nrows with country != 'GB': {naive_foreign}; "
      f"rows foreign to the customer's home: {(merged['location'] == 'Foreign').sum()}")
