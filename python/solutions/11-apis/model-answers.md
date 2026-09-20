# Module 11 Lab - Model Answer Notes

See `api_client.py`. Verified: with the mock API running, this loads all 20 rows into a
DataFrame regardless of `page_size`, and correctly retries the same page (without advancing)
when a manual test forces a `429`.

Key points to check in a delegate's solution:

- **On a `429`, the loop must `continue` without incrementing `page`** - a delegate who advances
  to the next page after a 429 will silently lose whatever page was rate-limited, producing a
  DataFrame with fewer than 20 rows without any error being raised.
- **`Retry-After` is read from the response header**, not hardcoded to a guessed sleep duration -
  the server's stated wait time should be respected exactly.
- **The stopping condition is `page >= total_pages`**, not a hardcoded page count - the loop
  must work correctly for any `page_size` a delegate chooses to test with.
- **The API-vs-extract answer must be specific to this dataset's actual characteristics**
  (twenty records, daily refresh) - "APIs are good for real-time data, extracts are good for
  batch" is the textbook answer, but the lab is testing whether a delegate can apply it to a
  specific case, not just recite it.
