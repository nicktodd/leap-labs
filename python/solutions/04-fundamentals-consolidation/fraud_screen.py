"""fraud_screen.py - screen card transactions against simple fraud rules.

Usage (from any folder):
    python fraud_screen.py
    python fraud_screen.py --input ../../shared/messy-transactions-raw.csv --high-value 750

Standard library only. Importing this module defines functions and prints nothing; the
extension scripts import from it.
"""

import argparse
import csv
from datetime import datetime
from pathlib import Path

SHARED = Path(__file__).resolve().parents[2] / "shared"
OUT = Path(__file__).resolve().parent / "output"

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M"
NIGHT_START_HOUR = 0   # NIGHT_ONLINE covers 00:00 to 04:59 inclusive
NIGHT_END_HOUR = 5     # exclusive upper bound, so 05:00 is not night


# --- Reading ----------------------------------------------------------------------------

def load_rates(path):
    """Return a dict of currency -> rate to GBP, read from an fx_rates CSV file."""
    with open(path, newline="", encoding="utf-8") as f:
        return {row["currency"]: float(row["rate_to_gbp"]) for row in csv.DictReader(f)}


def load_customers(path):
    """Return a dict of customer_id -> customer row, read from a customers CSV file."""
    with open(path, newline="", encoding="utf-8") as f:
        return {row["customer_id"]: row for row in csv.DictReader(f)}


def parse_row(row, rates):
    """Return a copy of a raw CSV row with amount_gbp (float) and ts (datetime) added.

    Raises ValueError with a short reason if the amount, timestamp or currency is unusable.
    """
    try:
        amount = float(row["amount"])
    except ValueError:
        raise ValueError(f"bad amount {row['amount']!r}") from None
    try:
        ts = datetime.strptime(row["txn_timestamp"], TIMESTAMP_FORMAT)
    except ValueError:
        # Covers both the wrong format and an impossible date such as 2026-02-29.
        raise ValueError(f"bad timestamp {row['txn_timestamp']!r}") from None
    if row["currency"] not in rates:
        raise ValueError(f"unsupported currency {row['currency']!r}")
    # {**row, ...} builds a new dict, so the caller's row is left unchanged.
    return {**row, "amount_gbp": amount * rates[row["currency"]], "ts": ts}


def read_transactions(path, rates):
    """Read a transactions CSV and return (transactions, skipped).

    skipped is a list of (txn_id, reason) tuples. A malformed row is reported with a warning
    and skipped; it never stops the run.
    """
    transactions = []
    skipped = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                transactions.append(parse_row(row, rates))
            except ValueError as e:
                print(f"WARNING: skipping {row.get('txn_id', '?')}: {e}")
                skipped.append((row.get("txn_id", "?"), str(e)))
    return transactions, skipped


# --- Rules ------------------------------------------------------------------------------

def check_high_value(txn, threshold):
    """HIGH_VALUE: the GBP amount is above the threshold."""
    return txn["amount_gbp"] > threshold


def check_foreign(txn, customers):
    """Return "FOREIGN", "UNKNOWN_CUSTOMER" or None for one transaction.

    FOREIGN compares the transaction country with the customer's home_country, not with GB:
    a customer who lives in France is not abroad when they pay in France.
    """
    customer = customers.get(txn["customer_id"])
    if customer is None:
        return "UNKNOWN_CUSTOMER"
    if txn["country"] != customer["home_country"]:
        return "FOREIGN"
    return None


def check_night_online(txn):
    """NIGHT_ONLINE: an Online transaction between 00:00 and 04:59."""
    return txn["channel"] == "Online" and NIGHT_START_HOUR <= txn["ts"].hour < NIGHT_END_HOUR


def build_flags(transactions, customers, high_value):
    """Return a dict of txn_id -> list of flags, for transactions with at least one flag."""
    flags_by_txn = {}
    for txn in transactions:
        flags = []
        if check_high_value(txn, high_value):
            flags.append("HIGH_VALUE")
        foreign = check_foreign(txn, customers)
        if foreign:
            flags.append(foreign)
        if check_night_online(txn):
            flags.append("NIGHT_ONLINE")
        if flags:
            flags_by_txn[txn["txn_id"]] = flags
    return flags_by_txn


def find_velocity(transactions, threshold):
    """VELOCITY: return {(customer_id, date): count} for customer-days with count >= threshold.

    The key is a tuple, so each customer-day appears once however many transactions it has.
    """
    counts = {}
    for txn in transactions:
        key = (txn["customer_id"], txn["ts"].date())
        counts[key] = counts.get(key, 0) + 1
    return {key: n for key, n in counts.items() if n >= threshold}


def evaluate(transactions, flags_by_txn):
    """Compare the flags with the confirmed outcome in is_fraud."""
    fraud_ids = {t["txn_id"] for t in transactions if t["is_fraud"] == "1"}
    flagged_ids = set(flags_by_txn)
    return {
        "flagged": len(flagged_ids),
        "flagged_fraud": sorted(flagged_ids & fraud_ids),
        "false_alarms": sorted(flagged_ids - fraud_ids),
        "fraud_total": len(fraud_ids),
        "missed_fraud": sorted(fraud_ids - flagged_ids),
    }


# --- Report -----------------------------------------------------------------------------

def build_report(transactions, skipped, flags_by_txn, velocity, evaluation, args):
    """Return the report as a list of lines."""
    by_id = {t["txn_id"]: t for t in transactions}
    lines = [
        "PaySprint fraud screen",
        f"Input: {Path(args.input).name}",
        f"Rules: HIGH_VALUE > GBP {args.high_value:,.2f}; FOREIGN; NIGHT_ONLINE 00:00-04:59; "
        f"VELOCITY >= {args.velocity} per customer-day",
        "",
        f"Transactions processed: {len(transactions)}",
        f"Rows skipped (malformed): {len(skipped)}",
    ]
    for txn_id, reason in skipped:
        lines.append(f"  {txn_id}: {reason}")

    lines += ["", f"Flagged transactions: {len(flags_by_txn)}"]
    for txn_id, flags in flags_by_txn.items():
        t = by_id[txn_id]
        lines.append(f"  {txn_id} {t['customer_id']} {t['ts']:%Y-%m-%d %H:%M} "
                     f"{t['merchant']:<16} GBP {t['amount_gbp']:>9,.2f}  {', '.join(flags)}")

    lines += ["", f"Velocity customer-days: {len(velocity)}"]
    for (customer_id, day), count in sorted(velocity.items()):
        lines.append(f"  {customer_id} {day}: {count} transactions")

    e = evaluation
    lines += [
        "",
        "Rule evaluation against is_fraud (transaction flags only):",
        f"  Flagged transactions that are fraud: {len(e['flagged_fraud'])} of {e['flagged']}",
        f"  False alarms: {len(e['false_alarms'])}",
        f"  Fraud transactions with no flag: {len(e['missed_fraud'])} of {e['fraud_total']}"
        + (f" ({', '.join(e['missed_fraud'])})" if e["missed_fraud"] else ""),
    ]
    return lines


def write_report(path, lines):
    """Write the report to path and print the same text, so the two cannot differ."""
    text = "\n".join(lines)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    print(text)
    print(f"\nReport written to {path}")


# --- Command line -----------------------------------------------------------------------

def build_parser():
    """Return the argument parser. A separate function so extensions can add options."""
    parser = argparse.ArgumentParser(description="Screen card transactions against fraud rules")
    parser.add_argument("--input", default=SHARED / "transactions.csv", type=Path,
                        help="transactions CSV (default: shared/transactions.csv)")
    parser.add_argument("--customers", default=SHARED / "customers.csv", type=Path,
                        help="customers CSV (default: shared/customers.csv)")
    parser.add_argument("--fx", default=SHARED / "fx_rates.csv", type=Path,
                        help="FX rates CSV (default: shared/fx_rates.csv)")
    parser.add_argument("--report", default=OUT / "fraud_report.txt", type=Path,
                        help="report file (default: output/fraud_report.txt)")
    parser.add_argument("--high-value", default=500.0, type=float,
                        help="HIGH_VALUE threshold in GBP (default: 500)")
    parser.add_argument("--velocity", default=3, type=int,
                        help="VELOCITY: transactions per customer per day (default: 3)")
    return parser


def main(argv=None):
    # argv=None makes argparse read sys.argv; passing a list lets other code call main().
    args = build_parser().parse_args(argv)
    rates = load_rates(args.fx)
    customers = load_customers(args.customers)
    transactions, skipped = read_transactions(args.input, rates)
    flags_by_txn = build_flags(transactions, customers, args.high_value)
    velocity = find_velocity(transactions, args.velocity)
    evaluation = evaluate(transactions, flags_by_txn)
    lines = build_report(transactions, skipped, flags_by_txn, velocity, evaluation, args)
    write_report(args.report, lines)


if __name__ == "__main__":
    main()
