"""fraud_screen.py - screen card transactions against simple fraud rules.

Standard library only. Complete each function, then wire them together in main().
The suggested breakdown below is a guide: you may add helper functions, but keep each
function small enough to explain to your partner.
"""

import argparse
import csv
from datetime import datetime
from pathlib import Path

SHARED = Path(__file__).resolve().parents[2] / "shared"
OUT = Path(__file__).resolve().parent / "output"

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M"


# --- Reading ----------------------------------------------------------------------------

def load_rates(path):
    """Return a dict of currency -> rate to GBP (float), read from an fx_rates CSV file."""
    raise NotImplementedError


def load_customers(path):
    """Return a dict of customer_id -> customer row, read from a customers CSV file."""
    raise NotImplementedError


def parse_row(row, rates):
    """Return a copy of a raw CSV row with amount_gbp (float) and ts (datetime) added.

    TODO: raise ValueError with a short reason (naming the bad value) if the amount cannot
    be converted with float(), the timestamp does not match TIMESTAMP_FORMAT
    (datetime.strptime), or the currency has no rate.
    """
    raise NotImplementedError


def read_transactions(path, rates):
    """Read a transactions CSV and return (transactions, skipped).

    TODO: call parse_row for each row. For a malformed row, print a warning naming the
    txn_id and the reason, record it in `skipped` (e.g. a list of (txn_id, reason)
    tuples) and carry on. The tool must never crash on bad input.
    """
    raise NotImplementedError


# --- Rules ------------------------------------------------------------------------------

def check_high_value(txn, threshold):
    """TODO: HIGH_VALUE - return True if txn["amount_gbp"] > threshold."""
    raise NotImplementedError


def check_foreign(txn, customers):
    """TODO: return "FOREIGN" if the transaction country differs from the customer's
    home_country, "UNKNOWN_CUSTOMER" if the customer is not in `customers`, else None."""
    raise NotImplementedError


def check_night_online(txn):
    """TODO: NIGHT_ONLINE - return True for an Online transaction between 00:00 and 04:59."""
    raise NotImplementedError


def build_flags(transactions, customers, high_value):
    """TODO: return a dict of txn_id -> list of flags, for transactions with at least one
    flag, e.g. {"P0016": ["HIGH_VALUE", "FOREIGN", "NIGHT_ONLINE"]}."""
    raise NotImplementedError


def find_velocity(transactions, threshold):
    """TODO: VELOCITY - count transactions per (customer_id, calendar date) and return the
    customer-days whose count is >= threshold, e.g. {("K009", date(2026, 2, 12)): 4}."""
    raise NotImplementedError


def evaluate(transactions, flags_by_txn):
    """TODO: compare the flags with is_fraud. Return how many flagged transactions are
    fraud, how many are false alarms, and which fraud transactions have no flag."""
    raise NotImplementedError


# --- Report -----------------------------------------------------------------------------

def build_report(transactions, skipped, flags_by_txn, velocity, evaluation, args):
    """TODO: return the report as a list of lines (see the README for the contents)."""
    raise NotImplementedError


def write_report(path, lines):
    """TODO: write the lines to `path` (create its folder if needed) and print the same
    text to the console, so the file and the console output cannot differ."""
    raise NotImplementedError


# --- Command line -----------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(description="Screen card transactions against fraud rules")
    parser.add_argument("--input", default=SHARED / "transactions.csv", type=Path,
                        help="transactions CSV (default: shared/transactions.csv)")
    # TODO: add --customers, --fx, --report, --high-value and --velocity with the defaults
    #       listed in the README. Use type=float or type=int for the thresholds.
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    # TODO: load the rates and customers, read the transactions, build the flags, find the
    #       velocity customer-days, evaluate, then build and write the report.
    raise NotImplementedError("main() is not written yet")


if __name__ == "__main__":
    main()
