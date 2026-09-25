"""Module 11 lab solution: a client for the PaySprint payments API.

Start the API first, in its own terminal:   python shared/mock_api/payments_api.py
Then run:                                   python payments_client.py
"""
from pathlib import Path
import time

import pandas as pd
import requests

SHARED = Path(__file__).resolve().parents[2] / "shared"
BASE_URL = "http://127.0.0.1:5051"
API_TOKEN = "paysprint-lab-token"  # throwaway token for a local mock server (see Extension 2)
REQUEST_TIMEOUT = 10  # seconds; without a timeout a hung server would hang the client forever


class ApiAuthError(Exception):
    """Raised when the API rejects our credentials (HTTP 401)."""


def get_session(token=API_TOKEN):
    # A Session reuses the underlying TCP connection across requests (no new handshake per
    # page) and carries shared headers, so the Authorization header is set once here rather
    # than being repeated, and possibly forgotten, on every call.
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session


def fetch_page(session, cursor=None, limit=20, **filters):
    """Make one GET /transactions request and return the Response.

    401 raises ApiAuthError, other 4xx/5xx raise requests.HTTPError via raise_for_status().
    429 is returned unchanged: waiting and retrying is the caller's decision.
    """
    params = {"limit": limit, **filters}
    if cursor is not None:
        params["cursor"] = cursor
    resp = session.get(f"{BASE_URL}/transactions", params=params, timeout=REQUEST_TIMEOUT)
    if resp.status_code == 401:
        raise ApiAuthError(
            f"401 from {resp.url}: the API rejected the bearer token. "
            "Check the Authorization header is 'Bearer <token>' and the token is correct."
        )
    if resp.status_code == 429:
        return resp
    resp.raise_for_status()
    return resp


def fetch_all(session, limit=20, **filters):
    """Follow next_cursor until it is null, and return every row as a list of dicts."""
    rows = []
    cursor = None
    pages = waits = 0
    while True:
        resp = fetch_page(session, cursor=cursor, limit=limit, **filters)
        if resp.status_code == 429:
            waits += 1
            retry_after = int(resp.headers.get("Retry-After", 1))
            print(f"  429 rate limited, waiting {retry_after}s then retrying the same cursor")
            time.sleep(retry_after)
            continue  # cursor unchanged, so the same page is requested again
        pages += 1
        body = resp.json()
        rows.extend(body["data"])
        cursor = body["next_cursor"]
        if cursor is None:
            break
    print(f"  fetched {len(rows)} rows: {pages} page(s), {waits} rate-limit wait(s), filters={filters}")
    return rows


def fetch_customer(session, customer_id):
    """GET /customers/<id>. Returns the customer dict, or None when the API returns 404."""
    while True:
        resp = session.get(f"{BASE_URL}/customers/{customer_id}", timeout=REQUEST_TIMEOUT)
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 1))
            print(f"  429 rate limited, waiting {retry_after}s before looking up {customer_id}")
            time.sleep(retry_after)
            continue
        if resp.status_code == 404:
            return None  # a missing reference record is data to report, not a crash
        if resp.status_code == 401:
            raise ApiAuthError("401 from /customers: the API rejected the bearer token.")
        resp.raise_for_status()
        return resp.json()


if __name__ == "__main__":
    # --- Step 1-2: a bad token fails loudly with our own exception ---
    try:
        fetch_page(get_session(token="wrong-token"))
    except ApiAuthError as exc:
        print(f"Bad token handled: {exc}")

    session = get_session()

    # --- Step 3-4: full download via cursor pagination, checked against the extract ---
    print("\nFetching all transactions...")
    api_df = pd.DataFrame(fetch_all(session, limit=20))
    csv_df = pd.read_csv(SHARED / "transactions.csv")
    # The API returns JSON keys in alphabetical order, so reorder columns before comparing.
    api_df = api_df[csv_df.columns]
    print(f"API DataFrame shape: {api_df.shape}")
    print(f"Same txn_id set as transactions.csv: {set(api_df['txn_id']) == set(csv_df['txn_id'])}")
    pd.testing.assert_frame_equal(api_df, csv_df)  # stronger check: every value matches
    print("assert_frame_equal: API data is identical to transactions.csv")

    # --- Step 5: server-side filter vs local filter ---
    print("\nFetching DECLINED since 2026-02-15 with server-side filters...")
    server_df = pd.DataFrame(fetch_all(session, status="DECLINED", since="2026-02-15"))[csv_df.columns]
    local_df = api_df[
        (api_df["status"] == "DECLINED") & (api_df["txn_timestamp"].str[:10] >= "2026-02-15")
    ].reset_index(drop=True)
    print(f"Server-side filter: {len(server_df)} rows; local pandas filter: {len(local_df)} rows")
    print(f"Same rows: {server_df.equals(local_df)}")
    # Which is preferable: here the full download already exists, so filtering locally costs
    # nothing extra. When you only need the subset, filter on the server: one request for 9
    # rows instead of 7 requests for 140, less data transferred, and fewer requests counted
    # against a 5-per-10-seconds rate limit. Filter locally when you need the full data anyway,
    # or when the API does not support the filter you need (e.g. amount > 500).

    # --- Step 6: enrich each declined customer from /customers/<id> ---
    print("\nLooking up the segment of each customer with a recent decline...")
    for customer_id in sorted(server_df["customer_id"].unique()):
        customer = fetch_customer(session, customer_id)
        if customer is None:
            print(f"  {customer_id}: no customer record (404) - segment unknown")
        else:
            print(f"  {customer_id} {customer['customer_name']}: {customer['segment']}")

    # --- Step 7: API vs nightly extract, for this dataset ---
    # This is one closed month (2-28 Feb plus 1 Mar) of 140 card transactions. For the
    # month-end analysis in the rest of the course a nightly extract is the better fit: the
    # month does not change once closed, one file replaces 7 paginated requests and the
    # rate-limit waits, and the analysis does not depend on the API being up. The API is the
    # right tool for operational questions during the month: the fraud team checking today's
    # declines, or looking up one customer, where a subset of current data is needed now and
    # a nightly file would be up to a day old.
