import argparse
import csv
from pathlib import Path

DEFAULT_INPUT = Path(__file__).resolve().parents[2] / "shared" / "trades.csv"


def read_trades(path):
    """Read a trades CSV, returning (trades, skipped_count).

    Skips any row where quantity or value can't be converted to a number,
    printing a warning naming the trade_id, and continues with the rest.
    """
    trades = []
    skipped = 0
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row["quantity"] = float(row["quantity"])
                row["value"] = float(row["value"])
            except (TypeError, ValueError):
                print(f"Skipping malformed trade {row.get('trade_id', '?')}: "
                      f"bad quantity/value")
                skipped += 1
                continue
            trades.append(row)
    return trades, skipped


def check_large(trade, threshold):
    return trade["value"] > threshold


def check_high_volume(trade, threshold):
    return (
        trade["asset_class"] == "Equity"
        and trade["side"] == "BUY"
        and trade["quantity"] > threshold
    )


def count_by_client(trades):
    counts = {}
    for trade in trades:
        client = trade["client_name"]
        counts[client] = counts.get(client, 0) + 1
    return counts


def build_flags(trades, large_threshold, high_volume_threshold):
    flags_by_trade = {}
    for trade in trades:
        flags = []
        if check_large(trade, large_threshold):
            flags.append("LARGE")
        if check_high_volume(trade, high_volume_threshold):
            flags.append("HIGH_VOLUME")
        if flags:
            flags_by_trade[trade["trade_id"]] = flags
    return flags_by_trade


def find_frequent_clients(trades, frequency_threshold):
    counts = count_by_client(trades)
    return {name: n for name, n in counts.items() if n >= frequency_threshold}


def write_report(path, trades, skipped_count, flags_by_trade, frequent_clients):
    lines = []
    lines.append(f"Trades processed: {len(trades)}")
    lines.append(f"Trades skipped (malformed): {skipped_count}")
    lines.append("")
    lines.append("Flagged trades:")
    if flags_by_trade:
        for trade_id, flags in flags_by_trade.items():
            lines.append(f"  {trade_id}: {', '.join(flags)}")
    else:
        lines.append("  (none)")
    lines.append("")
    lines.append("High-frequency clients:")
    if frequent_clients:
        for client, count in frequent_clients.items():
            lines.append(f"  {client}: {count} trades")
    else:
        lines.append("  (none)")

    report_text = "\n".join(lines)
    with open(path, "w", encoding="utf-8") as f:
        f.write(report_text + "\n")

    print(report_text)


def main():
    parser = argparse.ArgumentParser(description="Trade compliance checker")
    parser.add_argument("--input", default=DEFAULT_INPUT)
    parser.add_argument("--report", default="report.txt")
    parser.add_argument("--large-threshold", type=float, default=20000)
    parser.add_argument("--high-volume-threshold", type=float, default=150)
    parser.add_argument("--frequency-threshold", type=int, default=3)
    args = parser.parse_args()

    trades, skipped_count = read_trades(args.input)
    flags_by_trade = build_flags(trades, args.large_threshold, args.high_volume_threshold)
    frequent_clients = find_frequent_clients(trades, args.frequency_threshold)
    write_report(args.report, trades, skipped_count, flags_by_trade, frequent_clients)


if __name__ == "__main__":
    main()
