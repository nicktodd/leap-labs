"""Module 14 Extension 4: a one-month "statement" for the top 3 customers by spend.

Spend uses the same definition as the dashboard: approved, not confirmed fraud, not held for
review. Credit limits come from shared/customers.csv. K012 has transactions but no customer
record, so the join must keep K012 and say that the limit is unknown, not crash or drop them.
"""
import pandas as pd

from payments_dashboard import OUT, SHARED, extract, run

TOP_N = 3


def customer_summary(df, customers):
    spend = df[(df["status"] == "APPROVED") & (df["is_fraud"] == 0) & ~df["held_for_review"]]
    per_customer = (spend.groupby(["customer_id", "customer_name"])
                    .agg(spend_gbp=("amount_gbp", "sum"), transactions=("txn_id", "size"),
                         largest_gbp=("amount_gbp", "max"))
                    .reset_index())
    top_category = (spend.groupby(["customer_id", "merchant_category"])["amount_gbp"].sum()
                    .reset_index().sort_values("amount_gbp", ascending=False)
                    .drop_duplicates("customer_id").set_index("customer_id")["merchant_category"])
    per_customer["top_category"] = per_customer["customer_id"].map(top_category)

    # Left join: every customer with spend stays, whether or not reference data exists.
    summary = per_customer.merge(customers[["customer_id", "segment", "credit_limit_gbp"]],
                                 on="customer_id", how="left", validate="one_to_one")
    summary["share_of_limit"] = summary["spend_gbp"] / summary["credit_limit_gbp"]  # NaN for K012
    summary["share_of_total"] = summary["spend_gbp"] / summary["spend_gbp"].sum()
    return summary.sort_values("spend_gbp", ascending=False).reset_index(drop=True)


def statement(row):
    if pd.isna(row["credit_limit_gbp"]):
        limit_line = "Credit limit: not on file (no customer record); share of limit not available"
        segment = "unknown"
    else:
        limit_line = (f"Credit limit: GBP {row['credit_limit_gbp']:,.0f}; "
                      f"February spend used {row['share_of_limit']:.1%} of it")
        segment = row["segment"]
    return "\n".join([
        f"--- {row['customer_name']} ({row['customer_id']}, {segment}) ---",
        f"Spend: GBP {row['spend_gbp']:,.2f} over {row['transactions']} transactions "
        f"({row['share_of_total']:.1%} of all customer spend)",
        f"Largest transaction: GBP {row['largest_gbp']:,.2f}; top category: {row['top_category']}",
        limit_line,
    ])


if __name__ == "__main__":
    raw_rows, rates = extract()
    clean_df, _ = run(raw_rows, rates)
    customers = pd.read_csv(SHARED / "customers.csv")
    summary = customer_summary(clean_df, customers)

    print(f"=== Top {TOP_N} customers by spend, February 2026 ===\n")
    for _, row in summary.head(TOP_N).iterrows():
        print(statement(row) + "\n")

    top_share = summary.head(TOP_N)["spend_gbp"].sum() / summary["spend_gbp"].sum()
    print(f"The top {TOP_N} of {len(summary)} customers account for {top_share:.1%} of customer spend.")

    no_record = summary[summary["credit_limit_gbp"].isna()]
    for _, row in no_record.iterrows():
        rank = row.name + 1
        print(f"No customer record: {row['customer_id']} {row['customer_name']} "
              f"(rank {rank}, GBP {row['spend_gbp']:,.2f}); raise with the reference-data team.")

    summary.round(4).to_csv(OUT / "customer_statements.csv", index=False)
    print("Wrote customer_statements.csv")
