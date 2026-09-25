import pandas as pd

from ext2_pipe_functions import FX_PATH, RAW_PATH, clean

pd.set_option("display.width", 120)

df = clean(pd.read_csv(RAW_PATH))
rates = pd.read_csv(FX_PATH).set_index("currency")["rate_to_gbp"]
df["amount_gbp"] = (df["amount"] * df["currency"].map(rates)).round(2)


def iqr_upper_fence(s):
    q1, q3 = s.quantile([0.25, 0.75])
    return q3 + 1.5 * (q3 - q1)


# Global rule: one fence for every transaction, whatever was bought.
global_fence = iqr_upper_fence(df["amount_gbp"])
df["global_flag"] = df["amount_gbp"] > global_fence

# Segment rule: one fence per merchant_category, computed within that category.
category_fence = df.groupby("merchant_category")["amount_gbp"].transform(iqr_upper_fence)
df["category_flag"] = df["amount_gbp"] > category_fence

print(f"Global upper fence: {global_fence:.2f} GBP")
print("Per-category upper fences (GBP):")
print(df.groupby("merchant_category")["amount_gbp"].apply(iqr_upper_fence).round(2).to_string())

summary = df.groupby("merchant_category")[["global_flag", "category_flag"]].sum()
summary.loc["TOTAL"] = summary.sum()
print("\nRows flagged per category:")
print(summary.to_string())

legit_big = df[df["global_flag"] & df["merchant_category"].isin(["Travel", "Electronics"]) & (df["is_fraud"] == 0)]
print(f"\nLegitimate (is_fraud == 0) Travel/Electronics rows flagged by the global rule: {len(legit_big)}")
print(legit_big[["txn_id", "customer_id", "merchant", "amount_gbp", "category_flag"]].to_string(index=False))

print("\nP0141 under each rule:")
print(df.loc[df["txn_id"] == "P0141", ["txn_id", "merchant", "amount_gbp", "global_flag", "category_flag"]]
      .to_string(index=False))

# Conclusion: the global fence (about 200 GBP) treats every flight, laptop or phone as
# suspicious, because the month is dominated by small coffee, transport and grocery spend.
# A per-category fence compares a purchase with what is normal for that kind of purchase,
# so it stops flagging legitimate Travel and Electronics spend. It is still only as good
# as the segment: Dining and Transport mix cheap and expensive merchants (coffee vs
# restaurants, TfL vs Trainline), so their fences are low and flag normal meals and fares.
# Segment-aware thresholds reduce false positives; they do not replace a business rule
# (the contactless limit) or human review.
