"""Extension 1: retry transient 5xx errors with exponential backoff.

Start the API in flaky mode first:   python shared/mock_api/payments_api.py --flaky
(every fourth request that passes auth and the rate limit returns 503).
"""
import time

import pandas as pd
import requests

from payments_client import BASE_URL, REQUEST_TIMEOUT, ApiAuthError, get_session

MAX_ATTEMPTS = 4  # waits between attempts: 1 s, 2 s, 4 s


def get_with_retry(session, url, params=None):
    """GET with two separate retry policies.

    - 429: the server has told us exactly how long to wait (Retry-After), so wait that long.
      This does not use up an attempt: the server is healthy, we are going too fast.
    - 5xx: a transient server fault. Retry with exponential backoff (1, 2, 4 s), at most
      MAX_ATTEMPTS attempts in total, then give up and raise.
    - Any other 4xx is never retried: 400 (bad parameter), 401 (bad token) and 404 (no such
      customer) are problems with our request, and sending the same request again produces
      the same answer while adding load to the server.
    """
    attempt = 1
    while True:
        resp = session.get(url, params=params, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 1))
            print(f"    429 rate limited, waiting {retry_after}s (not counted as a failed attempt)")
            time.sleep(retry_after)
            continue
        if 500 <= resp.status_code < 600:
            if attempt == MAX_ATTEMPTS:
                print(f"    {resp.status_code} on attempt {attempt}/{MAX_ATTEMPTS}, giving up")
                resp.raise_for_status()
            delay = 2 ** (attempt - 1)  # 1, 2, 4
            print(f"    {resp.status_code} on attempt {attempt}/{MAX_ATTEMPTS}, retrying in {delay}s")
            time.sleep(delay)
            attempt += 1
            continue
        if resp.status_code == 401:
            raise ApiAuthError(f"401 from {resp.url}: the API rejected the bearer token.")
        resp.raise_for_status()  # other 4xx: raise immediately, no retry
        return resp


def fetch_all_with_retry(session, limit=20, **filters):
    rows, cursor = [], None
    while True:
        params = {"limit": limit, **filters}
        if cursor is not None:
            params["cursor"] = cursor
        body = get_with_retry(session, f"{BASE_URL}/transactions", params).json()
        rows.extend(body["data"])
        cursor = body["next_cursor"]
        if cursor is None:
            return rows


if __name__ == "__main__":
    session = get_session()

    print("Fetching all transactions from the flaky API...")
    df = pd.DataFrame(fetch_all_with_retry(session, limit=20))
    print(f"Loaded {len(df)} rows, {df['txn_id'].nunique()} unique txn_ids")

    # A 4xx must fail on the first attempt: limit=100 is outside the allowed 1..50.
    print("\nRequesting limit=100 (invalid) to show a 4xx is not retried...")
    try:
        get_with_retry(session, f"{BASE_URL}/transactions", {"limit": 100})
    except requests.HTTPError as exc:
        print(f"  Raised immediately, no retry: {exc}")
