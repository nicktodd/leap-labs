"""Module 13 lab solution: fraud classification on an imbalanced target, plus a simple
daily-spend forecasting comparison.

Part A predicts is_fraud (12 of 140 rows) and judges the models with recall, precision and a
confusion matrix, because accuracy is misleading when one class is rare.
Part B compares three baseline forecasts of daily approved spend by MAE (mean absolute error).

The extension files import load_features() and split() from here, so the core feature
engineering and the train/test split are defined once.
"""
from pathlib import Path

import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    mean_absolute_error,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

SHARED = Path(__file__).resolve().parents[2] / "shared"

FEATURES = ["amount_gbp", "distance_from_home_km", "hour", "is_online", "is_foreign"]


def load_features():
    """Return the 140 transactions with amount_gbp and the five model features added."""
    df = pd.read_csv(SHARED / "transactions.csv", parse_dates=["txn_timestamp"])
    fx = pd.read_csv(SHARED / "fx_rates.csv")
    customers = pd.read_csv(SHARED / "customers.csv")

    df = df.merge(fx, on="currency", how="left", validate="many_to_one")
    df["amount_gbp"] = df["amount"] * df["rate_to_gbp"]

    # is_foreign is judged against the customer's HOME country, not against GB. K003 (home FR)
    # and K008 (home IE) live abroad, so a simple country != "GB" test would mark every one of
    # their ordinary purchases as foreign. K012 has no customers.csv row (reference data lag):
    # a left merge keeps her rows, and every one of her 10 transactions is in GB about 20 km
    # from home, so GB is the sensible assumed home country. The assumption is flagged in a
    # column so it stays visible rather than hidden inside fillna.
    df = df.merge(customers[["customer_id", "home_country"]], on="customer_id", how="left")
    df["home_country_assumed"] = df["home_country"].isna()
    df["home_country"] = df["home_country"].fillna("GB")

    df["hour"] = df["txn_timestamp"].dt.hour
    df["is_online"] = (df["channel"] == "Online").astype(int)
    df["is_foreign"] = (df["country"] != df["home_country"]).astype(int)
    return df


def split(df):
    """The one train/test split every part of the lab uses."""
    X = df[FEATURES]
    y = df["is_fraud"]
    # stratify=y keeps the fraud share the same in both halves. With only 12 positives, an
    # unstratified split could put 1 or 7 of them in the test set by chance, and a test set
    # with 1 fraud can only score recall 0.0 or 1.0.
    return train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)


def fraud_pipeline(class_weight=None):
    # Scaling inside the Pipeline means the scaler learns its mean/standard deviation from
    # the training rows only, so no information leaks from the test set.
    return Pipeline([
        ("scale", StandardScaler()),
        ("model", LogisticRegression(class_weight=class_weight)),
    ])


def report(name, y_test, preds):
    acc = accuracy_score(y_test, preds)
    rec = recall_score(y_test, preds, zero_division=0)
    prec = precision_score(y_test, preds, zero_division=0)
    tn, fp, fn, tp = confusion_matrix(y_test, preds, labels=[0, 1]).ravel()
    print(f"  {name:<22} accuracy {acc:.3f}  recall {rec:.2f}  precision {prec:.2f}  "
          f"TP {tp}  FP {fp}  FN {fn}  TN {tn}")
    return {"accuracy": acc, "recall": rec, "precision": prec, "tp": tp, "fp": fp, "fn": fn, "tn": tn}


def part_a(df):
    print("=== Part A: fraud classification ===")
    print(f"Rows: {len(df)}, fraud rows: {df['is_fraud'].sum()} "
          f"({df['is_fraud'].mean():.1%} of all transactions)")
    print(f"Rows with an assumed home country (no customers.csv record): "
          f"{df['home_country_assumed'].sum()} ({', '.join(df.loc[df['home_country_assumed'], 'customer_id'].unique())})")

    X_train, X_test, y_train, y_test = split(df)
    print(f"Train: {len(y_train)} rows, {y_train.sum()} fraud.  "
          f"Test: {len(y_test)} rows, {y_test.sum()} fraud.")
    print(f"Test fraud rows: {', '.join(df.loc[y_test[y_test == 1].index, 'txn_id'])}")
    print("  With only 4 fraud rows in the test set, each one moves recall by 0.25.\n")

    dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
    report("Dummy (most frequent)", y_test, dummy.predict(X_test))

    plain = fraud_pipeline().fit(X_train, y_train)
    plain_preds = plain.predict(X_test)
    report("Logistic regression", y_test, plain_preds)

    balanced = fraud_pipeline(class_weight="balanced").fit(X_train, y_train)
    bal_preds = balanced.predict(X_test)
    report("Logistic, balanced", y_test, bal_preds)

    print("\nConfusion matrix, balanced model (rows = actual 0/1, columns = predicted 0/1):")
    print(confusion_matrix(y_test, bal_preds, labels=[0, 1]))

    # Show exactly which rows each model got right and wrong: with 4 positives this is more
    # informative than any summary number.
    test_rows = df.loc[X_test.index, ["txn_id", "customer_id", "amount_gbp", "hour", "channel",
                                      "country", "is_fraud"]].copy()
    test_rows["plain_pred"] = plain_preds
    test_rows["balanced_pred"] = bal_preds
    interesting = test_rows[(test_rows["is_fraud"] == 1) | (test_rows["plain_pred"] == 1)
                            | (test_rows["balanced_pred"] == 1)]
    print("\nTest rows that are fraud or were flagged by either model:")
    print(interesting.round(2).to_string(index=False))

    coefs = pd.Series(balanced.named_steps["model"].coef_[0], index=FEATURES).round(2)
    print("\nBalanced model coefficients (on standardised features):")
    print(coefs.to_string())


# Why accuracy looks good for every model: 38 of the 42 test rows are legitimate, so a model
# that never flags anything (the dummy) already scores 38/42 = 0.905. The plain logistic
# regression also scores 0.905, because it swaps one missed fraud for one false alarm. The
# balanced model scores 0.929. Accuracy is dominated by the easy majority class and barely moves.
# Recall shows the difference: 0.00 (dummy), 0.25 (plain), 0.50 (balanced).
#
# class_weight="balanced" weights each fraud row by about 98 / (2 * 8) = 6.1 during training,
# so missing a fraud costs the model more. Here recall doubles from 0.25 to 0.50 (it now
# catches K009's GBP 1.50 card-testing charge, P0043) and precision rises from 0.50 to 0.67,
# because the one false alarm (P0100, K007's legitimate GBP 1,203 flight booked from the US) is
# shared by both models. On this split the balanced model is better on both measures; the
# usual trade-off (more recall bought with more false alarms) appears in Extension 1 when the
# threshold is lowered to 0.1. With 4 test positives, one row either way changes recall by 0.25,
# so do not read too much into one split (Extension 2 addresses this).
#
# The two frauds both models miss are the subtle ones: P0088 happened at 23:04, and "hour" is
# a linear feature, so 23 looks like late evening rather than "night"; P0136 is K011's cloned
# card used in-store in GB in the afternoon, which looks like ordinary spending on every feature.
#
# For a fraud-operations manager: on the 42 transactions held back for testing, the balanced
# model flagged 3, and 2 of those were fraud (P0045, a GBP 1,013 Apple Store attempt from the
# US, and P0043, a GBP 1.50 test charge). It missed 2 of the 4 frauds. A missed fraud (false
# negative) is money lost: P0136 alone is GBP 780.00 that went through on a cloned card, plus
# a customer who discovers it on their statement. A false alarm (false positive) costs an
# analyst's time and an irritated genuine customer: P0100 was K007's own GBP 1,203 flight
# booking during a business trip, and blocking it would have stranded a Business customer.
# On these numbers the model is a helpful first filter for night-time, overseas, online
# attempts, but it cannot be the only control, because the frauds that look normal get through.


def part_b(df):
    print("\n=== Part B: forecasting daily approved spend ===")
    approved = df[df["status"] == "APPROVED"]
    daily = approved.set_index("txn_timestamp")["amount_gbp"].resample("D").sum()
    print(f"Daily series: {len(daily)} days, {daily.index.min():%a %d %b} to {daily.index.max():%a %d %b}")

    train, test = daily.iloc[:-7], daily.iloc[-7:]
    forecasts = pd.DataFrame({
        "actual": test,
        # 1. Always predict the average training day.
        "train_mean": train.mean(),
        # 2. Naive: tomorrow looks like today. shift(1) moves each value one day later.
        "naive": daily.shift(1).loc[test.index],
        # 3. Seasonal naive: same weekday one week earlier. shift(7) keeps Monday with Monday.
        "seasonal_naive": daily.shift(7).loc[test.index],
    })
    forecasts.index = forecasts.index.strftime("%a %d %b")
    print(forecasts.round(2).to_string())

    print(f"\nHeld-out week: actual average GBP {test.mean():,.2f} a day, "
          f"training mean GBP {train.mean():,.2f} a day")
    print("MAE (mean absolute error) over the 7 held-out days, GBP:")
    for name in ["train_mean", "naive", "seasonal_naive"]:
        mae = mean_absolute_error(forecasts["actual"], forecasts[name])
        print(f"  {name:<15} {mae:,.2f}")

    weekly = daily.resample("W-SUN").sum().to_frame("sum")
    weekly["transactions"] = approved.set_index("txn_timestamp").resample("W-SUN").size()
    print("\nApproved spend by week (weeks end on Sunday):")
    for week_end, row in weekly.iterrows():
        print(f"  week ending {week_end:%d %b}: GBP {row['sum']:,.2f} from {int(row['transactions'])} transactions")

    genuine = approved[approved["is_fraud"] == 0]
    genuine_weekly = genuine.set_index("txn_timestamp")["amount_gbp"].resample("W-SUN").sum()
    print("Same, excluding the 5 approved confirmed-fraud rows: "
          + ", ".join(f"GBP {v:,.2f}" for v in genuine_weekly))

# Which forecast wins: the plain training mean (MAE GBP 384.86) beats both the naive forecast
# (GBP 529.63) and the seasonal naive forecast (GBP 512.08). Daily totals here are driven by a
# few one-off large purchases (flights, electronics, and the GBP 2,145 fraudulent flight on Sun
# 22 Feb). Naive and seasonal naive copy those spikes forward onto days where they do not
# repeat: naive predicts GBP 2,730.79 for Mon 23 Feb, and seasonal naive predicts the same
# GBP 2,730.79 for Sun 1 Mar. The mean spreads the spikes thinly and is never wildly wrong.
#
# Why the payday week matters: the held-out week (23 Feb to 1 Mar) contains payday (Fri 27 Feb)
# and has the most approved transactions of any week (36, against 27, 34 and 30). Excluding
# confirmed fraud, it is also the highest-spend week by a wide margin (GBP 3,198.87 against
# GBP 1,448.98 to GBP 1,908.34). A forecast trained only on the three pre-payday weeks has never
# seen a payday: the training mean predicts GBP 356.79 a day, against an actual held-out average
# of GBP 568.41 a day (GBP 3,978.87 / 7), so even the winning method under-forecasts the week.
# Payday is a monthly cycle:
# with one month of data it cannot be learned, and seasonal naive only captures the weekly
# cycle. Several months of history would be needed before a monthly pattern could be modelled.


if __name__ == "__main__":
    data = load_features()
    part_a(data)
    part_b(data)
