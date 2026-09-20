# Module 11 Lab - Accessing Data Through APIs

## Objectives

By the end of this lab you will have:

- Authenticated against a REST API using an API key header
- Handled pagination to retrieve a complete dataset across multiple requests
- Handled a `429` rate-limit response by waiting and retrying, not failing or hammering the API
- Loaded the retrieved data into a pandas DataFrame

## Setup

- `pip install flask requests pandas`
- Start the mock API in its own terminal, and leave it running for this whole lab:
  ```bash
  python shared/mock_api/trades_api.py
  ```
- The API key is `leap-python-key`, sent as the `X-API-Key` header.

## The API

`GET http://127.0.0.1:5050/trades?page=<n>&page_size=<n>`

- Requires the `X-API-Key` header - a missing or wrong key returns `401`.
- Returns `{"page", "page_size", "total_pages", "total_records", "data"}` - `data` is only the
  current page's rows.
- Enforces a rate limit: more than 5 requests in a 10-second window returns `429`, with a
  `Retry-After` header (seconds to wait).

## Task

Starter file: `starter_api_client.py`, in `labs/11-apis/`.

1. Write a function `fetch_page(page, page_size)` that makes one authenticated GET request and
   returns the parsed JSON response.
2. Write a function `fetch_all_trades(page_size)` that calls `fetch_page` in a loop, starting at
   page 1, accumulating each page's `data`, and stopping once `page >= total_pages`.
3. In `fetch_all_trades`, handle a `429` response: read the `Retry-After` header, `time.sleep()`
   for that many seconds, then retry the **same** page (don't skip it, and don't advance to the
   next page).
4. Load the accumulated rows into a pandas DataFrame, and print its shape and the first 5 rows.
5. In a comment, answer: for this specific dataset (twenty trade records, refreshed at the start
   of each business day), would you actually recommend an API over a nightly batch extract? Why?

## Acceptance criteria

- The script runs with `python starter_api_client.py` (with the mock API running) and produces
  no errors.
- The final DataFrame has all 20 trade records, regardless of the `page_size` you choose.
- A `429` response is handled by waiting `Retry-After` seconds and retrying the same page - not
  by crashing, silently dropping the page, or retrying without waiting.
- The API-vs-extract comment gives a specific, justified answer for this dataset, not a generic
  restatement of "it depends."
