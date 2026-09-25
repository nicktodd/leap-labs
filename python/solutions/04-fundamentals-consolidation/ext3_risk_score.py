"""Extension 3: a risk score per transaction, a --min-score filter and ranked output.

The score is the number of flags on the transaction, plus 1 for VELOCITY when the
transaction falls on a flagged customer-day.

    python ext3_risk_score.py --min-score 2
"""

from fraud_screen import (OUT, build_flags, build_parser, find_velocity, load_customers,
                          load_rates, read_transactions, write_report)


def score_transactions(transactions, flags_by_txn, velocity):
    """Return a list of (score, txn, flags) for every transaction, including score 0."""
    scored = []
    for txn in transactions:
        flags = list(flags_by_txn.get(txn["txn_id"], []))   # copy: do not change the input
        if (txn["customer_id"], txn["ts"].date()) in velocity:
            flags.append("VELOCITY")
        scored.append((len(flags), txn, flags))
    return scored


def main(argv=None):
    parser = build_parser()
    parser.add_argument("--min-score", type=int, default=2,
                        help="only list transactions with at least this score (default: 2)")
    parser.set_defaults(report=OUT / "risk_report.txt")
    args = parser.parse_args(argv)

    rates = load_rates(args.fx)
    customers = load_customers(args.customers)
    transactions, skipped = read_transactions(args.input, rates)
    flags_by_txn = build_flags(transactions, customers, args.high_value)
    velocity = find_velocity(transactions, args.velocity)
    scored = score_transactions(transactions, flags_by_txn, velocity)

    # Highest score first; within a score, the largest GBP amount first. A tuple key sorts
    # on the first item, then the second. Negating both gives descending order for each.
    ranked = sorted((s for s in scored if s[0] >= args.min_score),
                    key=lambda s: (-s[0], -s[1]["amount_gbp"]))

    lines = [f"Transactions with risk score >= {args.min_score}: {len(ranked)} "
             f"of {len(transactions)} processed ({len(skipped)} skipped)", ""]
    lines.append(f"{'score':>5}  {'txn_id':<6} {'cust':<4} {'amount_gbp':>10}  fraud  flags")
    for score, txn, flags in ranked:
        lines.append(f"{score:>5}  {txn['txn_id']:<6} {txn['customer_id']:<4} "
                     f"{txn['amount_gbp']:>10,.2f}  {txn['is_fraud']:>5}  {', '.join(flags)}")

    # How well does the score separate fraud from the rest?
    lines += ["", "Score distribution (all processed transactions):",
              f"{'score':>5} {'txns':>5} {'fraud':>6}"]
    by_score = {}
    for score, txn, _ in scored:
        counts = by_score.setdefault(score, [0, 0])
        counts[0] += 1
        counts[1] += txn["is_fraud"] == "1"   # True adds 1, False adds 0
    for score in sorted(by_score, reverse=True):
        lines.append(f"{score:>5} {by_score[score][0]:>5} {by_score[score][1]:>6}")

    write_report(args.report, lines)


if __name__ == "__main__":
    main()
