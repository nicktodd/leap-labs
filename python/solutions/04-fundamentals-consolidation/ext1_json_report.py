"""Extension 1: --format json writes the fraud report as JSON instead of text.

    python ext1_json_report.py --format json
"""

import json
from pathlib import Path

from fraud_screen import (build_flags, build_parser, build_report, evaluate, find_velocity,
                          load_customers, load_rates, read_transactions, write_report)


def build_report_dict(transactions, skipped, flags_by_txn, velocity, evaluation, args):
    """Return the report as a dict of JSON-compatible values.

    json.dump only handles str, int, float, bool, None, list and dict. datetime and date
    objects, tuples used as keys and Path objects must be converted first.
    """
    by_id = {t["txn_id"]: t for t in transactions}
    return {
        "input": Path(args.input).name,
        "rules": {"high_value_gbp": args.high_value, "velocity": args.velocity},
        "processed": len(transactions),
        "skipped": [{"txn_id": txn_id, "reason": reason} for txn_id, reason in skipped],
        "flagged": [
            {
                "txn_id": txn_id,
                "customer_id": by_id[txn_id]["customer_id"],
                "timestamp": by_id[txn_id]["ts"].isoformat(timespec="minutes"),
                "merchant": by_id[txn_id]["merchant"],
                "amount_gbp": round(by_id[txn_id]["amount_gbp"], 2),
                "flags": flags,
            }
            for txn_id, flags in flags_by_txn.items()
        ],
        # The velocity keys are (customer_id, date) tuples: JSON object keys must be
        # strings, so each customer-day becomes a small object in a list instead.
        "velocity": [
            {"customer_id": customer_id, "date": day.isoformat(), "count": count}
            for (customer_id, day), count in sorted(velocity.items())
        ],
        "evaluation": evaluation,
    }


def main(argv=None):
    parser = build_parser()
    parser.add_argument("--format", choices=["text", "json"], default="text",
                        help="report format (default: text)")
    args = parser.parse_args(argv)

    rates = load_rates(args.fx)
    customers = load_customers(args.customers)
    transactions, skipped = read_transactions(args.input, rates)
    flags_by_txn = build_flags(transactions, customers, args.high_value)
    velocity = find_velocity(transactions, args.velocity)
    evaluation = evaluate(transactions, flags_by_txn)

    if args.format == "text":
        write_report(args.report, build_report(transactions, skipped, flags_by_txn,
                                               velocity, evaluation, args))
        return

    report = build_report_dict(transactions, skipped, flags_by_txn, velocity, evaluation, args)
    path = Path(args.report).with_suffix(".json")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Processed {report['processed']}, flagged {len(report['flagged'])}, "
          f"velocity customer-days {len(report['velocity'])}")
    print(f"JSON report written to {path}")

    # Read it back to prove the file is valid JSON with the expected shape.
    with open(path, encoding="utf-8") as f:
        loaded = json.load(f)
    print(f"Round trip: {len(loaded['flagged'])} flagged, first {loaded['flagged'][0]}")


if __name__ == "__main__":
    main()
