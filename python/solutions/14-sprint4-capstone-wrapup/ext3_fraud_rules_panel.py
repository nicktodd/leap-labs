"""Module 14 Extension 3: a fraud-rules panel for the dashboard.

Module 4's screening rules, rewritten with pandas over the cleaned dashboard data, and scored
against is_fraud (the fraud team's confirmed outcome). For each rule: how many transactions it
flags, how many of those are confirmed fraud (caught), and how many are not (false alarms).
"""
import pandas as pd

from payments_dashboard import OUT, SHARED, extract, run

HIGH_VALUE_GBP = 500
VELOCITY_PER_DAY = 3  # transactions by one customer on one calendar day
NIGHT_HOURS = range(0, 5)  # 00:00 to 04:59


def apply_rules(df, customers):
    # how="left" keeps K012, who has transactions but no customer record; indicator=True
    # tells us which rows found no match, so they get UNKNOWN_CUSTOMER instead of FOREIGN.
    df = df.merge(customers[["customer_id", "home_country"]], on="customer_id",
                  how="left", validate="many_to_one", indicator=True)
    known = df["_merge"] == "both"
    day_count = df.groupby(["customer_id", df["txn_timestamp"].dt.date])["txn_id"].transform("size")

    rules = pd.DataFrame({
        "HIGH_VALUE": df["amount_gbp"] > HIGH_VALUE_GBP,
        "FOREIGN": known & (df["country"] != df["home_country"]),
        "UNKNOWN_CUSTOMER": ~known,
        "NIGHT_ONLINE": (df["channel"] == "Online") & df["txn_timestamp"].dt.hour.isin(NIGHT_HOURS),
        "VELOCITY": day_count >= VELOCITY_PER_DAY,
    }, index=df.index)
    return df.drop(columns="_merge"), rules


def score(rules, is_fraud):
    fraud = is_fraud == 1
    rows = {}
    for name in rules.columns:
        hit = rules[name]
        rows[name] = {"flagged": int(hit.sum()), "fraud caught": int((hit & fraud).sum()),
                      "false alarms": int((hit & ~fraud).sum())}
    any_flag = rules.any(axis=1)
    rows["ANY RULE"] = {"flagged": int(any_flag.sum()), "fraud caught": int((any_flag & fraud).sum()),
                        "false alarms": int((any_flag & ~fraud).sum())}
    return pd.DataFrame(rows).T


if __name__ == "__main__":
    raw_rows, rates = extract()
    clean_df, _ = run(raw_rows, rates)
    customers = pd.read_csv(SHARED / "customers.csv")
    df, rules = apply_rules(clean_df, customers)

    panel = score(rules, df["is_fraud"])
    fraud_total = int((df["is_fraud"] == 1).sum())
    print(f"=== Fraud-rules panel ({len(df)} transactions, {fraud_total} confirmed fraud) ===")
    print(f"Rules: HIGH_VALUE > GBP {HIGH_VALUE_GBP}; FOREIGN = country differs from home country; "
          f"NIGHT_ONLINE = Online 00:00-04:59; VELOCITY = {VELOCITY_PER_DAY}+ transactions per customer-day")
    print(panel.to_string())

    fraud = df["is_fraud"] == 1
    any_flag = rules.any(axis=1)
    missed = df[fraud & ~any_flag]
    print(f"\nFraud missed by every rule ({len(missed)}):")
    print(missed[["txn_id", "customer_id", "merchant", "channel", "country", "amount_gbp", "status"]]
          .to_string(index=False) if len(missed) else "  none")

    # False alarms from the FOREIGN rule, by customer: shows who the rule inconveniences.
    foreign_fp = df[rules["FOREIGN"] & ~fraud]
    print("\nFOREIGN false alarms by customer:")
    print(foreign_fp.groupby(["customer_id", "country"]).size().rename("transactions").to_string())

    flagged = df.loc[any_flag, ["txn_id", "customer_id", "amount_gbp", "is_fraud"]].copy()
    flagged["flags"] = rules[any_flag].apply(lambda r: ",".join(r.index[r]), axis=1)
    flagged.to_csv(OUT / "fraud_rules_flagged.csv", index=False)
    print(f"\nPrecision of ANY RULE: {panel.loc['ANY RULE', 'fraud caught'] / panel.loc['ANY RULE', 'flagged']:.1%}; "
          f"recall: {panel.loc['ANY RULE', 'fraud caught'] / fraud_total:.1%}")
    print("Wrote fraud_rules_flagged.csv")
