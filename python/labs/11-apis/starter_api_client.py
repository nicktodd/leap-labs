import time
import pandas as pd
import requests

BASE_URL = "http://127.0.0.1:5050/trades"
API_KEY = "leap-python-key"
HEADERS = {"X-API-Key": API_KEY}

# TODO:
# 1. fetch_page(page, page_size): one authenticated GET request, return parsed JSON.
# 2. fetch_all_trades(page_size): loop fetch_page from page 1, accumulate data,
#    stop once page >= total_pages.
# 3. In fetch_all_trades, on a 429: read Retry-After, time.sleep(), retry the SAME page.
# 4. Load accumulated rows into a DataFrame; print shape and df.head().
# 5. Comment: would you recommend an API over a nightly batch extract for this dataset? Why?
