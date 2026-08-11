"""Trade compliance checker — flags LARGE, HIGH_VOLUME, and HIGH_FREQUENCY trades."""

import argparse
import csv


def read_trades(path: str) -> tuple[list[dict], int]:
    """Read a trades CSV, returning (trades, skipped_count).

    Skips any row where quantity or value can't be converted to a number,
    printing a warning naming the trade_id, and continues with the rest.
    """
    trades = []
    skipped_count = 0
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row["quantity"] = float(row["quantity"])
                row["value"] = float(row["value"])
            except (ValueError, TypeError):
                print(f"WARNING: skipping malformed row {row.get('trade_id', '?')} — "
                      f"quantity or value not numeric")
                skipped_count += 1
                continue
            trades.append(row)
    return trades, skipped_count


def check_large(trade: dict, threshold: float) -> bool:
    """Return True if trade value exceeds threshold."""
    return trade["value"] > threshold


def check_high_volume(trade: dict, threshold: float) -> bool:
    """Return True if this is an Equity BUY with quantity > threshold.

    Does not apply to Bond or Crypto trades — their quantities are on a different scale.
    """
    return (
        trade["asset_class"] == "Equity"
        and trade["side"] == "BUY"
        and trade["quantity"] > threshold
    )


def count_by_client(trades: list[dict]) -> dict[str, int]:
    """Return a dict of client_name -> trade count."""
    counts: dict[str, int] = {}
    for trade in trades:
        name = trade["client_name"]
        counts[name] = counts.get(name, 0) + 1
    return counts


def build_flags(
    trades: list[dict], large_threshold: float, high_volume_threshold: float
) -> dict[str, list[str]]:
    """Return a dict of trade_id -> list of flags for every trade that triggers at least one rule."""
    flags: dict[str, list[str]] = {}
    for trade in trades:
        tid = trade["trade_id"]
        trade_flags = []
        if check_large(trade, large_threshold):
            trade_flags.append("LARGE")
        if check_high_volume(trade, high_volume_threshold):
            trade_flags.append("HIGH_VOLUME")
        if trade_flags:
            flags[tid] = trade_flags
    return flags


def find_frequent_clients(
    trades: list[dict], frequency_threshold: int
) -> dict[str, int]:
    """Return a dict of client_name -> count for clients with count >= frequency_threshold."""
    counts = count_by_client(trades)
    return {name: count for name, count in counts.items() if count >= frequency_threshold}


def write_report(
    path: str,
    trades: list[dict],
    skipped_count: int,
    flags_by_trade: dict[str, list[str]],
    frequent_clients: dict[str, int],
) -> None:
    """Write the compliance report to path and also print to console."""
    lines = []
    lines.append(f"Trades processed: {len(trades)}")
    lines.append(f"Trades skipped (malformed): {skipped_count}")
    lines.append("")
    lines.append("--- Per-trade flags (LARGE / HIGH_VOLUME) ---")
    if flags_by_trade:
        for tid, flags in flags_by_trade.items():
            lines.append(f"  {tid}: {', '.join(flags)}")
    else:
        lines.append("  (none)")
    lines.append("")
    lines.append("--- HIGH_FREQUENCY clients ---")
    if frequent_clients:
        for name, count in sorted(frequent_clients.items()):
            lines.append(f"  {name}: {count} trades")
    else:
        lines.append("  (none)")

    report_text = "\n".join(lines)
    print(report_text)
    with open(path, "w", encoding="utf-8") as f:
        f.write(report_text + "\n")
    print(f"\nReport written to {path}")


def main() -> None:
    """Parse arguments and run the compliance check."""
    parser = argparse.ArgumentParser(description="Trade compliance checker")
    parser.add_argument("--input", default=r"C:\Users\zackt\Documents\leap-sprint4\shared\trades.csv")
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
