"""Extension 4: sweep the HIGH_VALUE threshold and count hits and misses at each value.

For each threshold, prints how many transactions are flagged, how many confirmed fraud
transactions are caught, how many flags are false alarms and how many fraud transactions
are missed. First for HIGH_VALUE on its own, then for all transaction rules together.

    python ext4_threshold_sweep.py
"""

from fraud_screen import (build_flags, build_parser, check_high_value, evaluate,
                          load_customers, load_rates, read_transactions)

THRESHOLDS = [250, 500, 750, 1000]


def print_table(title, results):
    print(f"\n{title}")
    print(f"{'threshold':>9} {'flagged':>8} {'caught':>7} {'false':>6} {'missed':>7}  missed ids")
    for threshold, e in results:
        print(f"{threshold:>9,} {e['flagged']:>8} {len(e['flagged_fraud']):>7} "
              f"{len(e['false_alarms']):>6} {len(e['missed_fraud']):>7}  "
              f"{', '.join(e['missed_fraud']) or '-'}")


def main(argv=None):
    args = build_parser().parse_args(argv)
    rates = load_rates(args.fx)
    customers = load_customers(args.customers)
    transactions, _ = read_transactions(args.input, rates)

    high_value_only = []
    all_rules = []
    for threshold in THRESHOLDS:
        # evaluate() only needs a dict keyed by txn_id, so the single-rule case can reuse it.
        flags = {t["txn_id"]: ["HIGH_VALUE"] for t in transactions
                 if check_high_value(t, threshold)}
        high_value_only.append((threshold, evaluate(transactions, flags)))
        all_rules.append((threshold,
                          evaluate(transactions, build_flags(transactions, customers, threshold))))

    print_table("HIGH_VALUE rule on its own", high_value_only)
    print_table("All transaction rules (HIGH_VALUE, FOREIGN/UNKNOWN_CUSTOMER, NIGHT_ONLINE)",
                all_rules)
    # caught / flagged is the share of flags that are fraud (precision);
    # caught / (caught + missed) is the share of fraud that is flagged (recall).
    # Module 13 names and computes these properly.


if __name__ == "__main__":
    main()
