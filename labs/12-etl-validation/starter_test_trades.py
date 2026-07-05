import pytest
from starter_etl_pipeline import extract, transform

VALID_ASSET_CLASSES = {"Equity", "Bond", "ETF", "Crypto"}


@pytest.fixture
def clean_trades():
    return transform(extract())


# TODO: write tests for
# 1. no missing trade_id values
# 2. quantity is always positive
# 3. value is never negative
# 4. asset_class only contains VALID_ASSET_CLASSES
# 5. no duplicate trade_id values

# TODO (Part 3): add test_asset_class_valid_no_all, deliberately missing .all(),
# run it, interpret the error (with GenAI if needed), then fix it yourself with a
# comment explaining why .all() is required.
