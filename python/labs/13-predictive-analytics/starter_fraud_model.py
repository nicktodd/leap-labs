"""Module 13 lab starter: fraud classification (Part A) and daily-spend forecasting (Part B).

Run from any folder:  python labs/13-predictive-analytics/starter_fraud_model.py
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
    """Return all 140 transactions with amount_gbp and the five FEATURES columns added."""
    df = pd.read_csv(SHARED / "transactions.csv", parse_dates=["txn_timestamp"])
    fx = pd.read_csv(SHARED / "fx_rates.csv")
    customers = pd.read_csv(SHARED / "customers.csv")
    # TODO 1: add amount_gbp (merge fx on currency; amount * rate_to_gbp).
    # TODO 1: add hour, is_online (channel == "Online") and is_foreign (0/1 columns).
    #         Decide how to define is_foreign: country != "GB", or country != the customer's
    #         home_country from customers.csv. If you use customers.csv, decide what to do
    #         about K012, who has no row there. Justify your choice in a comment.
    raise NotImplementedError


def split(df):
    """TODO 2: return X_train, X_test, y_train, y_test using
    train_test_split(test_size=0.3, random_state=42, stratify=y).
    Print how many fraud rows land in each half."""
    raise NotImplementedError


def part_a(df):
    # TODO 3: DummyClassifier(strategy="most_frequent"): accuracy, recall, precision
    #         (use zero_division=0).
    # TODO 4: Pipeline([("scale", StandardScaler()), ("model", LogisticRegression())]):
    #         the same three metrics plus confusion_matrix.
    # TODO 5: the same pipeline with LogisticRegression(class_weight="balanced").
    #         Print which test rows each model flags and which frauds it misses.
    # TODO 6: comments: why accuracy looks good for every model; the recall/precision
    #         trade-off; a paragraph for a fraud-operations manager citing your numbers.
    raise NotImplementedError


def part_b(df):
    # TODO 7: daily totals of APPROVED amount_gbp with resample("D") (expect 28 days).
    # TODO 8: hold out the final 7 days; build three forecasts for them:
    #         training mean, naive (shift(1)), seasonal naive (shift(7)).
    # TODO 9: print the MAE of each, and comment on which wins and why the payday week matters.
    raise NotImplementedError


if __name__ == "__main__":
    data = load_features()
    part_a(data)
    part_b(data)
