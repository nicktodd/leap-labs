import time
import pandas as pd
import requests

BASE_URL = "http://127.0.0.1:5050/trades"
API_KEY = "leap-sprint4-key"
HEADERS = {"X-API-Key": API_KEY}


def fetch_page(page, page_size):
    resp = requests.get(BASE_URL, headers=HEADERS, params={"page": page, "page_size": page_size})
    return resp


def fetch_all_trades(page_size=5):
    all_rows = []
    page = 1
    while True:
        resp = fetch_page(page, page_size)
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 1))
            print(f"Rate limited on page {page}, waiting {retry_after}s...")
            time.sleep(retry_after)
            continue  # retry the same page, don't advance
        body = resp.json()
        all_rows.extend(body["data"])
        if page >= body["total_pages"]:
            break
        page += 1
    return all_rows


if __name__ == "__main__":
    rows = fetch_all_trades(page_size=5)
    df = pd.DataFrame(rows)
    print(f"Shape: {df.shape}")
    print(df.head())

    # For this dataset: a nightly batch extract, not an API, is the better fit. It's
    # only 20 records, refreshed once a day — pagination and rate-limit handling here
    # are pure overhead for a dataset this small and this infrequently updated. An API
    # would make more sense if the data changed intraday, or if only a small filtered
    # subset (not the whole book) were needed on each access.
