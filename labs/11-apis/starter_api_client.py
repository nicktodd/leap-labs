"""Lab 11: API client — authenticated, paginated, rate-limit-aware."""

import time
import pandas as pd
import requests

BASE_URL = "http://127.0.0.1:5050/trades"
API_KEY = "leap-sprint4-key"
HEADERS = {"X-API-Key": API_KEY}


def fetch_page(page: int, page_size: int) -> dict:
    """Make one authenticated GET request and return the parsed JSON response."""
    response = requests.get(
        BASE_URL,
        headers=HEADERS,
        params={"page": page, "page_size": page_size},
    )
    return response


def fetch_all_trades(page_size: int = 5) -> list[dict]:
    """Fetch every page from the API, handling 429 rate-limit responses.

    On a 429 response, reads the Retry-After header, sleeps that many seconds,
    then retries the *same* page — never skipping it.
    """
    all_rows = []
    page = 1

    while True:
        response = fetch_page(page, page_size)

        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 10))
            print(f"Rate limited on page {page}. Waiting {retry_after}s before retry…")
            time.sleep(retry_after)
            continue  # retry the same page — do NOT increment page

        response.raise_for_status()
        data = response.json()
        all_rows.extend(data["data"])
        total_pages = data["total_pages"]
        print(f"Fetched page {page}/{total_pages} ({len(data['data'])} records)")

        if page >= total_pages:
            break
        page += 1

    return all_rows


if __name__ == "__main__":
    rows = fetch_all_trades(page_size=5)
    df = pd.DataFrame(rows)
    print(f"\nDataFrame shape: {df.shape}")
    print(df.head())

# Comment: for this specific dataset — 20 trade records, refreshed once per business day —
# I would NOT recommend an API over a nightly batch extract. An API makes sense when you
# need real-time or near-real-time data, or when the dataset is too large to batch. Here,
# with only 20 static daily records and no intraday updates, a simple nightly CSV pull (or
# even a daily file drop) is simpler, more reliable, has zero rate-limit concerns, and
# requires no running server. The API adds operational overhead (uptime, auth, pagination)
# with no benefit for a daily-refreshed 20-row dataset.
