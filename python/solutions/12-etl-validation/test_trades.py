import pytest
from etl_pipeline import extract, transform

VALID_ASSET_CLASSES = {"Equity", "Bond", "ETF", "Crypto"}


@pytest.fixture
def clean_trades():
    return transform(extract())


def test_no_missing_trade_ids(clean_trades):
    assert clean_trades["trade_id"].notna().all()


def test_quantity_is_positive(clean_trades):
    assert (clean_trades["quantity"] > 0).all()


def test_value_is_non_negative(clean_trades):
    assert (clean_trades["value"] >= 0).all()


def test_asset_class_is_valid(clean_trades):
    assert clean_trades["asset_class"].isin(VALID_ASSET_CLASSES).all()


def test_no_duplicate_trade_ids(clean_trades):
    assert clean_trades["trade_id"].is_unique


def test_asset_class_valid_no_all(clean_trades):
    # isin(...) returns one True/False per row (a Series), not a single True/False,
    # so `assert` alone can't collapse it into a pass/fail verdict — Python doesn't
    # know how to interpret "is this whole Series true?" without being told how.
    # .all() answers the actual question this test is asking: "were ALL rows valid?"
    assert clean_trades["asset_class"].isin(VALID_ASSET_CLASSES).all()
