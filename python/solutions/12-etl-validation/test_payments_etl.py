"""Module 12 lab solution: pytest suite for payments_etl.py.

Run from this folder:   python -m pytest -v
"""
import math

import pandas as pd
import pytest

from payments_etl import (
    clean_amount, extract, load, normalise_channel, normalise_country, parse_timestamps,
    read_fx, transform,
)

ALLOWED_CHANNELS = {"Online", "In-store", "Contactless"}
REQUIRED_COLUMNS = ["txn_id", "txn_timestamp", "customer_id", "merchant", "merchant_category",
                    "channel", "country", "currency", "amount", "status", "amount_gbp"]


# --- Unit tests: one transform step each, on tiny hand-made inputs ------------------------

@pytest.mark.parametrize("raw_value, expected", [
    ("Online", "Online"),
    ("online", "Online"),
    ("ONLINE", "Online"),
    ("Online ", "Online"),
    ("In-store", "In-store"),
    ("in-store", "In-store"),
    ("In Store", "In-store"),
    ("instore", "In-store"),
    ("Contactless", "Contactless"),
    ("contactless", "Contactless"),
    ("CONTACTLESS", "Contactless"),
    (" Contactless", "Contactless"),
])
def test_normalise_channel(raw_value, expected):
    assert normalise_channel(pd.Series([raw_value])).iloc[0] == expected


def test_normalise_channel_unknown_is_missing():
    # An unrecognised value must not be silently mapped to one of the valid channels.
    assert pd.isna(normalise_channel(pd.Series(["Telephone"])).iloc[0])


def test_normalise_country():
    result = normalise_country(pd.Series(["UK", "gb", " FR "]))
    assert result.tolist() == ["GB", "GB", "FR"]


def test_clean_amount():
    result = clean_amount(pd.Series(["£1,249.00", "€85.50", "$1,594.61", "TBC", ""]))
    assert result.iloc[0] == 1249.0
    assert result.iloc[1] == 85.5
    assert result.iloc[2] == 1594.61
    assert math.isnan(result.iloc[3])
    assert math.isnan(result.iloc[4])


def test_parse_timestamps_both_formats_and_invalid():
    result = parse_timestamps(pd.Series(["2026-02-03 14:22", "03-Feb-2026 14:22", "2026-02-29 09:35"]))
    assert result.iloc[0] == pd.Timestamp("2026-02-03 14:22")
    assert result.iloc[1] == pd.Timestamp("2026-02-03 14:22")
    assert pd.isna(result.iloc[2])  # 2026 is not a leap year


# --- Pipeline fixture: run extract + transform once for all the output tests --------------

@pytest.fixture(scope="module")
def pipeline():
    # scope="module": the pipeline runs once for this file, not once per test. The tests
    # only read the result, so sharing it is safe and keeps the suite fast.
    raw = extract()
    fx = read_fx()
    clean, rejects = transform(raw, fx)
    return {"raw": raw, "fx": fx, "clean": clean, "rejects": rejects}


# --- Output validation --------------------------------------------------------------------

def test_clean_row_count(pipeline):
    assert len(pipeline["clean"]) == 138


def test_required_columns_not_null(pipeline):
    clean = pipeline["clean"]
    assert clean[REQUIRED_COLUMNS].notna().all().all()
    assert (clean["merchant_category"] != "").all()


def test_channel_in_allowed_set(pipeline):
    assert pipeline["clean"]["channel"].isin(ALLOWED_CHANNELS).all()


def test_amount_positive(pipeline):
    assert (pipeline["clean"]["amount"] > 0).all()


def test_txn_id_unique(pipeline):
    assert pipeline["clean"]["txn_id"].is_unique


def test_currency_in_fx_table(pipeline):
    assert pipeline["clean"]["currency"].isin(pipeline["fx"]["currency"]).all()


def test_amount_gbp_matches_rate(pipeline):
    clean = pipeline["clean"]
    rates = clean["currency"].map(pipeline["fx"].set_index("currency")["rate_to_gbp"])
    expected = (clean["amount"] * rates).tolist()
    # amount_gbp is rounded to pence, so the difference can be up to half a penny. For
    # P0026, 6.30 * 0.85 is computed as 5.3549999999999995 and rounds to 5.36: slightly more than
    # 0.005 away, because of floating-point representation. A
    # tolerance of one penny states the rule "correct to the penny" without that edge case.
    assert clean["amount_gbp"].tolist() == pytest.approx(expected, abs=0.01)


def test_outlier_flagged_not_deleted(pipeline):
    flagged = pipeline["clean"].loc[pipeline["clean"]["needs_review"], "txn_id"].tolist()
    assert flagged == ["P0141"]


# --- Reconciliation: no row may disappear without a recorded reason -----------------------

def test_reconciliation(pipeline):
    assert len(pipeline["raw"]) == len(pipeline["clean"]) + len(pipeline["rejects"])


def test_reject_reasons(pipeline):
    reasons = dict(zip(pipeline["rejects"]["txn_id"], pipeline["rejects"]["reject_reason"]))
    assert reasons == {
        "P0095": "duplicate",
        "P0102": "duplicate",
        "P0057": "bad amount",
        "P0086": "bad amount",
        "P0131": "invalid timestamp",
    }


# --- Load: write to a temporary folder, never to the real output --------------------------

def test_load_writes_both_files(pipeline, tmp_path):
    clean_path, rejects_path = load(pipeline["clean"], pipeline["rejects"], tmp_path)
    assert clean_path.exists()
    assert rejects_path.exists()
    reloaded = pd.read_csv(clean_path)
    assert len(reloaded) == len(pipeline["clean"])
    assert list(reloaded.columns) == list(pipeline["clean"].columns)
    assert "reject_reason" in pd.read_csv(rejects_path).columns


# --- Part 3: exact float comparison, fixed ------------------------------------------------

def test_total_amount_gbp(pipeline):
    # Original version: assert clean["amount_gbp"].sum() == 19099.01
    # It failed with: assert np.float64(19099.010000000002) == 19099.01
    # Most decimal values (0.01, 0.85, ...) have no exact binary floating-point
    # representation, so each amount is stored as the nearest binary value and adding 138
    # of them accumulates tiny errors. == demands bit-for-bit equality, which float
    # arithmetic does not promise. pytest.approx compares within a relative tolerance
    # (1e-6 by default), which is the question the test means to ask.
    assert pipeline["clean"]["amount_gbp"].sum() == pytest.approx(19099.01)
