import argparse
import csv


def read_trades(path):
    """Read a trades CSV, returning (trades, skipped_count).

    TODO: skip any row where quantity or value can't be converted to a
    number, printing a warning naming the trade_id, and continue with the
    rest of the file rather than crashing.
    """
    raise NotImplementedError


def check_large(trade, threshold):
    """TODO: return True if trade['value'] > threshold."""
    raise NotImplementedError


def check_high_volume(trade, threshold):
    """TODO: return True if this is an Equity BUY with quantity > threshold.
    Do not apply this rule to Bond or Crypto trades."""
    raise NotImplementedError


def count_by_client(trades):
    """TODO: return a dict of client_name -> trade count."""
    raise NotImplementedError


def build_flags(trades, large_threshold, high_volume_threshold):
    """TODO: return a dict of trade_id -> list of flags (e.g. ["LARGE"])
    for every trade that triggers at least one rule."""
    raise NotImplementedError


def find_frequent_clients(trades, frequency_threshold):
    """TODO: return a dict of client_name -> count, for clients whose trade
    count is >= frequency_threshold."""
    raise NotImplementedError


def write_report(path, trades, skipped_count, flags_by_trade, frequent_clients):
    """TODO: write the report described in the lab README to `path`, and
    print the same content to the console."""
    raise NotImplementedError


def main():
    parser = argparse.ArgumentParser(description="Trade compliance checker")
    parser.add_argument("--input", default="shared/trades.csv")
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
