"""Extension 3: hand-crafted bad input. Run:  python -m pytest -v ext3_test_bad_input.py

The core transform() has no rule for an unsupported currency (amount_gbp would be NaN) or a
negative amount (it would pass straight through). transform_strict() adds both rules as a
validation step on the raw rows, then hands the remaining rows to the unchanged transform().
"""
import pandas as pd
import pytest

from payments_etl import RAW_PATH, clean_amount, extract, read_fx, transform


def transform_strict(raw, fx):
    """transform() plus two rules: currency must be in the FX table, amount must not be
    negative. Rejected rows keep their raw values, as in transform()."""
    currency = raw["currency"].str.strip().str.upper()
    unknown_currency = ~currency.isin(fx["currency"])
    # A refund would be a separate transaction type; a card payment with a negative amount
    # is a keying or feed error. Blank and 'TBC' give NaN here, and NaN < 0 is False, so
    # they are left for transform() to reject as "bad amount".
    # The parentheses matter: & binds more tightly than <. A row with both problems is
    # reported once, as an unknown currency.
    negative_amount = (clean_amount(raw["amount"]) < 0) & ~unknown_currency

    rejects = pd.concat([
        raw[unknown_currency].assign(reject_reason="unknown currency"),
        raw[negative_amount].assign(reject_reason="negative amount"),
    ])
    clean, core_rejects = transform(raw[~unknown_currency & ~negative_amount], fx)
    rejects = pd.concat([rejects, core_rejects], ignore_index=True)
    return clean, rejects


@pytest.fixture
def bad_input(tmp_path):
    # Start from three genuine raw rows, then add one row per new rule. Copying real rows
    # keeps every other column valid, so each bad row fails for exactly one reason.
    good = extract()[lambda df: df["txn_id"].isin(["P0001", "P0002", "P0003"])]
    unknown = good.iloc[[0]].assign(txn_id="X0001", currency="JPY", amount="4500")
    negative = good.iloc[[1]].assign(txn_id="X0002", amount="-25.00")
    negative_symbol = good.iloc[[2]].assign(txn_id="X0003", amount="-£12.50")
    path = tmp_path / "bad_transactions.csv"
    pd.concat([good, unknown, negative, negative_symbol]).to_csv(path, index=False)
    return path


@pytest.fixture
def result(bad_input):
    raw = extract(bad_input)
    clean, rejects = transform_strict(raw, read_fx())
    return raw, clean, rejects


def test_bad_rows_rejected_with_reason(result):
    _, _, rejects = result
    reasons = dict(zip(rejects["txn_id"], rejects["reject_reason"]))
    assert reasons == {
        "X0001": "unknown currency",
        "X0002": "negative amount",
        "X0003": "negative amount",
    }


def test_good_rows_survive(result):
    _, clean, _ = result
    assert clean["txn_id"].tolist() == ["P0001", "P0002", "P0003"]
    assert clean["amount_gbp"].notna().all()


def test_reconciliation(result):
    raw, clean, rejects = result
    assert len(raw) == len(clean) + len(rejects)


def test_rejects_keep_raw_values(result):
    _, _, rejects = result
    # The rejects file is for a person to investigate, so it shows what arrived, not a
    # half-cleaned version.
    assert rejects.loc[rejects["txn_id"] == "X0003", "amount"].iloc[0] == "-£12.50"


def test_real_file_unchanged():
    # The new rules must not reject anything in the real extract.
    clean, rejects = transform_strict(extract(RAW_PATH), read_fx())
    assert len(clean) == 138
    assert set(rejects["reject_reason"]) == {"duplicate", "bad amount", "invalid timestamp"}
