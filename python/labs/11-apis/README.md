# Module 11 Lab - Accessing Data Through APIs

## Scenario

PaySprint's fraud team wants card-transaction data straight from the payments platform rather
than waiting for the nightly file. The platform exposes a REST (Representational State Transfer)
API (Application Programming Interface) that uses bearer-token authentication, cursor-based
pagination, server-side filters and a rate limit. You will build a small, well-behaved client
for it, check that what it returns matches the nightly extract, and enrich recent declines with
customer reference data.

## Objectives

By the end of this lab you will have:

- Authenticated with a bearer token set once on a `requests.Session`
- Raised a clear, custom exception for authentication failures and surfaced other HTTP errors
  with `raise_for_status()`
- Followed cursor-based pagination to retrieve a complete dataset
- Handled a `429` rate-limit response by waiting `Retry-After` seconds and retrying the same
  request
- Compared server-side filtering with local filtering in pandas, and reasoned about which to use
- Handled a `404` for a missing reference record without crashing
- Judged whether an API or a nightly extract suits this specific dataset

## Setup

- `pip install flask requests pandas`
- Start the lab API in its own terminal, and leave it running for the whole lab:
  ```bash
  python shared/mock_api/payments_api.py
  ```
  It listens on `http://127.0.0.1:5051`. This is a different API from the demo's
  (`trades_api.py` on port 5050): read its docstring before you start.
- Starter file: `labs/11-apis/starter_payments_client.py`. Run it from any folder with
  `python labs/11-apis/starter_payments_client.py`.
- The rate limit means a full run of your script includes waits of up to 10 seconds. That is
  expected behaviour, not a hang.

## The data

The API serves the 140 rows of `shared/transactions.csv` (one month of card transactions,
2 Feb to 1 Mar 2026) and the customer reference data in `shared/customers.csv`.

| Endpoint | Notes |
| --- | --- |
| `GET /transactions` | Query parameters: `limit` (1 to 50, default 20), `cursor`, and optional filters `status` (`APPROVED`/`DECLINED`), `customer_id`, `since` (`YYYY-MM-DD`, inclusive). Returns `{"data": [...], "count": n, "next_cursor": "..."}`; `next_cursor` is `null` on the last page. |
| `GET /customers/<customer_id>` | Returns one customer (`customer_id`, `customer_name`, `segment`, `home_country`, ...), or `404` if there is no reference record. |

- Every request needs the header `Authorization: Bearer paysprint-lab-token`; otherwise `401`.
- Rate limit: more than 5 requests in 10 seconds returns `429` with a `Retry-After` header
  (seconds to wait). Requests rejected with `401` do not count towards the limit.
- The cursor is opaque: do not decode it or build it yourself, pass back the value you received.

## Task

1. **Session.** Complete `get_session()` so it returns a `requests.Session` with the
   `Authorization` header set once. In a comment, explain why a `Session` is a better choice than
   calling `requests.get()` with the header each time (think about connection reuse and shared
   headers).
2. **One page, with error handling.** Complete `fetch_page(session, cursor=None, limit=20,
   **filters)`. It makes one request and returns the `Response`. On `401` it raises the custom
   `ApiAuthError` with a message that tells the reader what to check. On `429` it returns the
   response to the caller. For any other error status it calls `resp.raise_for_status()`. In the
   main block, create a session with a wrong token, call `fetch_page`, catch `ApiAuthError` and
   print its message.
3. **All pages.** Complete `fetch_all(session, limit=20, **filters)`. Follow `next_cursor` until
   it is `null`, accumulating `data`. On a `429`, sleep for `Retry-After` seconds, then retry with
   the **same** cursor. Print how many pages were fetched and how many rate-limit waits occurred.
4. **Check against the extract.** Load the rows into a DataFrame and compare it with
   `shared/transactions.csv`: print the shape, and whether the two `txn_id` sets are identical.
   Note that the JSON keys arrive in a different order from the CSV columns.
5. **Server-side vs local filtering.** Call `fetch_all(session, status="DECLINED",
   since="2026-02-15")`. Then filter your full download in pandas for the same condition. Print
   both row counts and whether the rows are the same. In a comment, say which approach is
   preferable here, and in what situations the other one would be the better choice.
6. **Enrich the declines.** For each distinct `customer_id` in the declined set, call
   `GET /customers/<id>` (complete `fetch_customer`) and print the customer's segment. One of the
   customers has no reference record: your code must report this clearly and carry on, not crash.
   These lookups count against the rate limit too.
7. **API or extract?** In a comment, answer: for this dataset (one closed month of 140 card
   transactions), would you recommend the API or a nightly batch extract, and for which uses? Base
   your answer on this dataset's characteristics, not a general rule.

## Acceptance criteria

- The script runs from any working directory with the lab API running, and produces no errors.
- A wrong token produces your `ApiAuthError` message, not a traceback or a `KeyError` on the
  JSON body.
- The full download has 140 rows and exactly the same `txn_id` set as `transactions.csv`,
  whatever `limit` you choose.
- A `429` is handled by waiting `Retry-After` seconds and retrying the same cursor, not by
  skipping a page, crashing, or retrying without waiting.
- The server-side filter and the local pandas filter both return the same 9 rows.
- The declined set covers 6 distinct customers; 5 segments are printed and the sixth (`K012`)
  is reported as having no customer record.
- The comments for steps 1, 5 and 7 give specific, justified answers.

## Extension exercises

1. **Retry with exponential backoff.** Restart the API with `python
   shared/mock_api/payments_api.py --flaky`, which returns `503` on every fourth request. Your core
   client now fails. Write a request helper that retries `5xx` responses with exponential backoff
   (waits of 1, 2 and 4 seconds, at most 4 attempts in total), still honours `Retry-After` on
   `429`, and never retries any other `4xx`. Show that a request with `limit=100` fails
   immediately with `400`. Done: the full download completes with 140 rows against the flaky
   server, and a comment explains why `4xx` errors must not be retried.
2. **Token from the environment.** Remove the token literal from your code. Read it from the
   environment variable `PAYSPRINT_API_TOKEN`, and if it is unset, exit before making any request
   with a message saying which variable to set and how. Done: the script works with the variable
   set, prints your helpful message with it unset, and the token string appears nowhere in your
   source file.
3. **A generator client.** Turn `fetch_all` into a generator, `iter_transactions(session,
   limit=20, **filters)`, that yields one row at a time and requests the next page only when the
   caller needs it. Count the rows without building a list, and use `next()` to find the first
   Online transaction over 1,000 without downloading every page. Done: the count is 140, and a
   comment explains the memory and request savings.
4. **Incremental sync.** Write a sync script that, on its first run, downloads everything to
   `output/transactions_synced.csv` and stores the latest `txn_timestamp` in
   `output/last_sync.txt`. On later runs it fetches with `since=<date of the last sync>`, appends
   the new rows and de-duplicates on `txn_id`. Because `since` works at date granularity, the
   second run re-fetches the last day. Done: the second run fetches only the last day's rows,
   reports how many duplicates it removed, and the stored file still has 140 unique rows.
