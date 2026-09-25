"""Extension 2: accept a second timestamp format and currency-symbol amounts.

Reuses parse_amount from Module 2 (a copy of payment_utils.py sits in this folder) and
compares the skipped rows with the core parser on shared/messy-transactions-raw.csv.

    python ext2_flexible_parsing.py
"""

import csv
from datetime import datetime

from fraud_screen import (OUT, SHARED, build_flags, build_parser, build_report, evaluate,
                          find_velocity, load_customers, load_rates, read_transactions,
                          write_report)
from payment_utils import PaymentError, parse_amount

# Tried in order; the first format that parses wins. The two formats cannot both match the
# same text, so the order does not change any result.
TIMESTAMP_FORMATS = ["%Y-%m-%d %H:%M", "%d-%b-%Y %H:%M"]


def parse_timestamp(text):
    """Return a datetime for text in any of TIMESTAMP_FORMATS, or raise ValueError."""
    for fmt in TIMESTAMP_FORMATS:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    raise ValueError(f"bad timestamp {text!r}")


def parse_row_flexible(row, rates):
    """Same contract as fraud_screen.parse_row, with the more tolerant parsers."""
    try:
        amount = parse_amount(row["amount"])
    except (TypeError, ValueError, PaymentError):
        # parse_amount raises ValueError for text such as 'TBC' or '', and
        # InvalidAmountError (a PaymentError) for zero or negative amounts.
        raise ValueError(f"bad amount {row['amount']!r}") from None
    ts = parse_timestamp(row["txn_timestamp"])   # 2026-02-29 still fails: no such date
    if row["currency"] not in rates:
        raise ValueError(f"unsupported currency {row['currency']!r}")
    return {**row, "amount_gbp": amount * rates[row["currency"]], "ts": ts}


def read_transactions_flexible(path, rates):
    """Same as fraud_screen.read_transactions, using parse_row_flexible."""
    transactions = []
    skipped = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                transactions.append(parse_row_flexible(row, rates))
            except ValueError as e:
                print(f"WARNING: skipping {row.get('txn_id', '?')}: {e}")
                skipped.append((row.get("txn_id", "?"), str(e)))
    return transactions, skipped


def main(argv=None):
    parser = build_parser()
    parser.set_defaults(input=SHARED / "messy-transactions-raw.csv",
                        report=OUT / "fraud_report_flexible.txt")
    args = parser.parse_args(argv)
    rates = load_rates(args.fx)
    customers = load_customers(args.customers)

    print("--- Core parser ---")
    _, core_skipped = read_transactions(args.input, rates)
    print("\n--- Flexible parser ---")
    transactions, skipped = read_transactions_flexible(args.input, rates)
    print(f"\nRows skipped: core {len(core_skipped)}, flexible {len(skipped)} "
          f"({len(core_skipped) - len(skipped)} fewer)\n")

    flags_by_txn = build_flags(transactions, customers, args.high_value)
    velocity = find_velocity(transactions, args.velocity)
    evaluation = evaluate(transactions, flags_by_txn)
    write_report(args.report, build_report(transactions, skipped, flags_by_txn, velocity,
                                           evaluation, args))


if __name__ == "__main__":
    main()
