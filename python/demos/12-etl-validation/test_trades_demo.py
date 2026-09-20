import pytest
from etl_pipeline_demo import extract, transform

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


# Deliberately broken: missing .all() on a boolean Series. Run this one on its own to
# see the "truth value of a Series is ambiguous" error, and practice interpreting it
# with GenAI before fixing it (see demo-guide.md, Part 4).
def test_asset_class_is_valid_broken(clean_trades):
    assert clean_trades["asset_class"].isin(VALID_ASSET_CLASSES)
