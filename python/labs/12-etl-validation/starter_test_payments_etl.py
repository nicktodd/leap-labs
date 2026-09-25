"""Module 12 lab starter: pytest suite for starter_payments_etl.py.

Run from this folder:   python -m pytest -v starter_test_payments_etl.py
"""
import pandas as pd
import pytest

from starter_payments_etl import (
    clean_amount, extract, load, normalise_channel, normalise_country, parse_timestamps,
    read_fx, transform,
)

ALLOWED_CHANNELS = {"Online", "In-store", "Contactless"}


# --- Unit tests: one transform function each, on tiny hand-made inputs --------------------

# TODO: list every raw channel variant in the file (Part 1, step 1 prints them) with its
# expected canonical value. One parametrised test then checks all of them.
@pytest.mark.parametrize("raw_value, expected", [
    ("online", "Online"),
    # TODO: the other variants
])
def test_normalise_channel(raw_value, expected):
    assert normalise_channel(pd.Series([raw_value])).iloc[0] == expected


# TODO: test_normalise_channel_unknown_is_missing - an unrecognised channel becomes NaN.

# TODO: test_normalise_country - "UK", "gb" and " FR " give "GB", "GB", "FR".

# TODO: test_clean_amount - a Series such as ["£1,249.00", "€85.50", "TBC", ""]. Check the two
# numbers and that the last two are NaN (NaN != NaN, so use math.isnan or pd.isna).

# TODO: test_parse_timestamps - both formats give the same Timestamp; "2026-02-29 09:35" is NaT.


# --- Pipeline fixture ---------------------------------------------------------------------

# TODO: a fixture with scope="module" that runs extract() and transform() once and returns
# raw, fx, clean and rejects (a dict is convenient). Comment on why scope="module" is safe here.


# --- Output validation, reconciliation and load -------------------------------------------

# TODO: the clean output has 138 rows.
# TODO: no nulls in the required columns; channel only takes ALLOWED_CHANNELS values.
# TODO: amount > 0; txn_id unique; every currency is in the FX table.
# TODO: the contactless outlier is flagged in needs_review and still present.
# TODO: reconciliation - raw rows == clean rows + rejected rows.
# TODO: the reject reasons per txn_id are the ones you expect.
# TODO: load() writes both files into pytest's tmp_path fixture, and they read back correctly.


# --- Part 3 -------------------------------------------------------------------------------

# TODO: test_total_amount_gbp - assert the exact total of amount_gbp with ==, as described in
# the README. Run it, read the failure, then fix it and explain the fix in a comment.
