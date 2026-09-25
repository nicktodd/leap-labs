"""Module 14 Extension 1: choose the data source with --source file|api.

Only the extract stage changes. The API rows are converted to the same shape as the raw
export (every value as text, same column order), then go through the same transform,
validate and load stages as the file.

API mode needs the lab API running in its own terminal:
    python shared/mock_api/payments_api.py
Then:
    python ext1_api_source.py --source api
    python ext1_api_source.py --source file     (same as payments_dashboard.py)
"""
import argparse
import time

import pandas as pd
import requests

from payments_dashboard import OUT, build_charts, extract, print_dashboard, run

BASE_URL = "http://127.0.0.1:5051"
API_TOKEN = "paysprint-lab-token"  # throwaway token for a local mock server
REQUEST_TIMEOUT = 10  # seconds
RAW_COLUMNS = ["txn_id", "txn_timestamp", "customer_id", "customer_name", "merchant",
               "merchant_category", "channel", "country", "currency", "amount", "status",
               "distance_from_home_km", "is_fraud"]


def fetch_all_transactions(limit=50):
    """Module 11's client pattern: bearer token set once on a Session, follow next_cursor
    until it is null, and on a 429 wait Retry-After seconds and retry the same cursor."""
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {API_TOKEN}"})
    rows, cursor, pages, waits = [], None, 0, 0
    while True:
        params = {"limit": limit}
        if cursor is not None:
            params["cursor"] = cursor
        resp = session.get(f"{BASE_URL}/transactions", params=params, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 429:
            waits += 1
            time.sleep(int(resp.headers.get("Retry-After", 1)))
            continue
        if resp.status_code == 401:
            raise SystemExit("The API rejected the bearer token (401): check API_TOKEN.")
        resp.raise_for_status()
        pages += 1
        body = resp.json()
        rows.extend(body["data"])
        cursor = body["next_cursor"]
        if cursor is None:
            break
    print(f"API: fetched {len(rows)} rows in {pages} page(s), {waits} rate-limit wait(s)")
    return rows


def extract_api():
    """Return (raw, fx) in exactly the shape extract() returns for the file."""
    try:
        rows = fetch_all_transactions()
    except requests.ConnectionError:
        raise SystemExit(f"Cannot reach the API at {BASE_URL}. Start it with: "
                         "python shared/mock_api/payments_api.py") from None
    # The API returns JSON numbers and alphabetically ordered keys. transform() expects the
    # raw export's layout, with every value as text, so match that here and nowhere else.
    raw = pd.DataFrame(rows)[RAW_COLUMNS].astype(str)
    _, fx = extract()  # FX rates are reference data and still come from the shared file
    return raw, fx


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PaySprint monthly payments dashboard")
    parser.add_argument("--source", choices=["file", "api"], default="file",
                        help="read the monthly export file (default) or the payments API")
    args = parser.parse_args()

    if args.source == "api":
        raw_rows, rates = extract_api()
        out_dir = OUT / "api"  # keep the two runs' outputs apart so they can be compared
    else:
        raw_rows, rates = extract()
        out_dir = OUT
    out_dir.mkdir(exist_ok=True)

    clean_df, results = run(raw_rows, rates, data_file=f"dashboard_data_{args.source}.csv")
    charts = build_charts(clean_df, results, out_dir=out_dir)
    print(f"Source: {args.source}\n")
    print_dashboard(results)
    print("\nCharts: " + ", ".join(str(p.relative_to(OUT)) for p in charts))
