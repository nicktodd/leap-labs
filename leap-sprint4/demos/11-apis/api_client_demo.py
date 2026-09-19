import time
import pandas as pd
import requests

BASE_URL = "http://127.0.0.1:5050/trades"
API_KEY = "leap-sprint4-key"
HEADERS = {"X-API-Key": API_KEY}

# --- Part 1: authentication ---
resp_no_key = requests.get(BASE_URL)
print(f"No API key: HTTP {resp_no_key.status_code} -- {resp_no_key.json()}")

resp_with_key = requests.get(BASE_URL, headers=HEADERS)
print(f"With API key: HTTP {resp_with_key.status_code}")

# --- Part 2: pagination ---
first_page = requests.get(BASE_URL, headers=HEADERS, params={"page": 1, "page_size": 5}).json()
print(f"\nPage 1 of {first_page['total_pages']}, {first_page['total_records']} total records")
print(f"Rows on this page: {len(first_page['data'])}")


def fetch_all_pages(page_size=5):
    all_rows = []
    page = 1
    while True:
        resp = requests.get(BASE_URL, headers=HEADERS, params={"page": page, "page_size": page_size})
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 1))
            print(f"  Rate limited, waiting {retry_after}s before retrying page {page}...")
            time.sleep(retry_after)
            continue
        body = resp.json()
        all_rows.extend(body["data"])
        if page >= body["total_pages"]:
            break
        page += 1
    return all_rows


print("\nFetching all pages...")
all_rows = fetch_all_pages(page_size=5)
df = pd.DataFrame(all_rows)
print(f"Loaded {len(df)} rows into a DataFrame")
print(df[["trade_id", "client_name", "value"]].head())

# --- Part 3: rate limits, demonstrated deliberately ---
print("\nHitting the API in a tight loop to trigger the rate limit...")
for i in range(8):
    resp = requests.get(BASE_URL, headers=HEADERS, params={"page": 1, "page_size": 1})
    print(f"  request {i + 1}: HTTP {resp.status_code}")
    if resp.status_code == 429:
        print(f"  Retry-After: {resp.headers.get('Retry-After')}s -- a well-behaved client waits this long")
        break
