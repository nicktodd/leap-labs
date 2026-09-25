"""Extension 1: schema test. Run:  python -m pytest -v ext1_test_schema.py"""
import pytest

from payments_etl import extract, read_fx, transform

# The contract downstream code relies on. If a transform change turns amount back into
# text, or leaves txn_timestamp unparsed, this test names the column that changed.
EXPECTED_DTYPES = {
    "txn_id": "str",
    "txn_timestamp": "datetime64[us]",
    "customer_id": "str",
    "customer_name": "str",
    "merchant": "str",
    "merchant_category": "str",
    "channel": "str",
    "country": "str",
    "currency": "str",
    "amount": "float64",
    "status": "str",
    "distance_from_home_km": "float64",
    "is_fraud": "int64",
    "amount_gbp": "float64",
    "needs_review": "bool",
}


@pytest.fixture(scope="module")
def clean():
    return transform(extract(), read_fx())[0]


def test_columns_match_schema(clean):
    # Order matters too: the CSV column order is part of what consumers read.
    assert list(clean.columns) == list(EXPECTED_DTYPES)


def test_dtypes_match_schema(clean):
    actual = clean.dtypes.astype(str).to_dict()
    # Comparing two dicts makes pytest print only the keys that differ.
    assert actual == EXPECTED_DTYPES
