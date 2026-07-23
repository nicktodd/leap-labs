"""Lab 12: pytest validation suite for the ETL pipeline output."""

import pytest
from starter_etl_pipeline import extract, transform

VALID_ASSET_CLASSES = {"Equity", "Bond", "ETF", "Crypto"}


@pytest.fixture
def clean_trades():
    return transform(extract())


def test_no_missing_trade_id(clean_trades):
    """Every row must have a trade_id — a missing id makes audit trails impossible."""
    assert clean_trades["trade_id"].isna().sum() == 0


def test_quantity_always_positive(clean_trades):
    """Quantity must be strictly positive — a zero or negative quantity is not a valid trade."""
    assert (clean_trades["quantity"] > 0).all()


def test_value_never_negative(clean_trades):
    """Value must be non-negative — a negative value would indicate a data-entry error."""
    assert (clean_trades["value"] >= 0).all()


def test_asset_class_valid(clean_trades):
    """asset_class must only contain the four canonical values after normalisation."""
    assert clean_trades["asset_class"].isin(VALID_ASSET_CLASSES).all()


def test_no_duplicate_trade_ids(clean_trades):
    """Each trade_id must appear exactly once — duplicates would double-count trades."""
    assert not clean_trades["trade_id"].duplicated().any()


# Part 3: deliberately broken test — missing .all()
# Running this as-is produces:
#   ValueError: The truth value of a Series is ambiguous. Use .any() or .all().
# because clean_trades["asset_class"].isin(valid) returns a boolean *Series*, not a single
# bool. Python's `assert` tries to evaluate the Series as a boolean scalar, which pandas
# refuses to do, raising the error. Fix: add .all() so the entire Series is collapsed to one
# True/False before the assert checks it.
def test_asset_class_valid_no_all(clean_trades):
    valid = {"Equity", "Bond", "ETF", "Crypto"}
    # Original broken version (kept for reference, commented out):
    # assert clean_trades["asset_class"].isin(valid)
    #
    # Fix: .isin() returns a boolean Series; .all() collapses it to a single bool.
    assert clean_trades["asset_class"].isin(valid).all()
