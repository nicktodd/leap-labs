# Module 11 Lab - Model Answer Notes

See `payments_client.py` (core), and `ext1_retry_backoff.py`, `ext2_env_token.py`,
`ext3_generator.py`, `ext4_incremental_sync.py` for the extensions. The extension scripts
import the core functions from `payments_client.py`.

Verified results (lab API running on port 5051):

- A session with a wrong token raises `ApiAuthError`; the script prints the message and
  continues.
- The full download with `limit=20` takes 7 pages and hits the rate limit once (a 10 s wait on a
  fresh server), giving a `(140, 13)` DataFrame. The `txn_id` set is identical to
  `transactions.csv`, and after reordering the columns `pd.testing.assert_frame_equal` passes
  (every value matches).
- `status=DECLINED, since=2026-02-15` returns 9 rows in 1 request; the local pandas filter
  returns the same 9 rows (`DataFrame.equals` is `True`).
- The 9 declines cover 6 customers: K001 Amara Okoye (Premium), K002 Ben Carter (Standard), K005
  Eilidh Murray (Standard), K009 Ibrahim Yusuf (Standard), K010 Julia Novak (Premium), and K012,
  which returns `404` (no customer record). The 6 lookups plus the earlier requests trigger one
  further rate-limit wait.
- A full run takes about 20 seconds, almost all of it rate-limit waiting.

Key points to check in a delegate's solution:

- **The header is set once on the `Session`**, not passed to every call. The comment should
  mention both connection reuse (one TCP/TLS connection kept alive across pages) and shared
  configuration (headers set in one place, so a new call cannot forget them).
- **`fetch_page` separates the three outcomes**: `401` raises the custom exception with an
  actionable message, `429` is returned to the caller, everything else goes through
  `raise_for_status()`. A delegate who calls `resp.json()["data"]` without checking the status
  gets a `KeyError` on the error body, which hides the real cause.
- **On a `429` the cursor must not change.** A loop that reads `next_cursor` from the 429 body
  (which has none) either crashes or ends early with fewer than 140 rows.
- **The loop stops on `next_cursor is None`**, not on `count < limit` or a hardcoded page count.
  With `limit=20` the last page is full (140 = 7 x 20), so a `count < limit` test would request
  an eighth page.
- **The comparison with the CSV accounts for column order** (the API returns keys alphabetically).
  Comparing `txn_id` sets is the minimum; `assert_frame_equal` after `api_df[csv_df.columns]` is
  a stronger check.
- **Filtering preference is argued, not asserted.** Good answer: server-side filtering is better
  when only the subset is needed (1 request for 9 rows instead of 7 for 140, less data, less
  rate-limit budget); local filtering is fine when the full data is already downloaded, and
  necessary when the API does not offer the filter (for example `amount > 500`).
- **The 404 is handled as data.** K012 is reported and the loop continues; a bare
  `raise_for_status()` on the customer endpoint crashes on the sixth customer.
- **The API vs extract answer uses this dataset's facts**: one closed month, 140 rows, the full
  download costs 7 requests plus rate-limit waits and the month does not change, so a nightly
  extract suits the month-end analysis; the API suits operational, current, subset questions
  (today's declines, one customer's record).

## Extension notes

**Extension 1 (retry with backoff).** Verified against `--flaky`: the download completes with
140 rows and 140 unique `txn_id`s, printing `503 on attempt 1/4, retrying in 1s` twice and one
`429` wait. Because the server fails only every fourth request, one retry always succeeds, so the
2 s and 4 s waits are not exercised; a delegate can test the give-up path by pointing the helper
at a URL that always returns `5xx`. The `limit=100` request raises `400 Client Error` on the
first attempt. Good answers explain that a `4xx` means the request itself is wrong, so repeating
it cannot succeed and only adds load; `429` is the exception because the server says when to
retry. Common pitfalls: counting `429` waits as failed attempts (the download can then give up
while the server is healthy), retrying every non-200 status, and backoff that does not grow.

**Extension 2 (token from the environment).** Verified: with `PAYSPRINT_API_TOKEN` unset the
script exits with status 1 and prints which variable to set and how, before any request is made;
with it set, the first page returns 5 rows. Check that the token literal has been removed from
the source (the extension imports `get_session` but passes the token explicitly). Common
pitfall: `os.environ["PAYSPRINT_API_TOKEN"]`, which fails with a bare `KeyError` that does not
tell the user what to do.

**Extension 3 (generator).** Verified: `sum(1 for _ in iter_transactions(...))` counts 140
rows, summing `is_fraud` gives 12, and `next(...)` finds P0016 (USD 1594.61 at Apple Store) as
the first Online transaction over 1,000 without fetching the remaining pages. The 429 handling
must live inside the generator. Good answers note that memory holds one page at a time and that
early termination saves requests, which matters under a rate limit. Common pitfall: collecting
rows into a list inside the generator and yielding it at the end, which gives no benefit.

**Extension 4 (incremental sync).** Verified over two runs: the first run fetches 140 rows and
writes `output/last_sync.txt` = `2026-03-01 21:30`; the second fetches with `since=2026-03-01`,
receives 8 rows, removes 8 duplicates and stores 140 rows. The overlap is deliberate: using the
next day as `since` would miss transactions posted later on the last synced date. Good answers
de-duplicate on `txn_id` (not whole rows, so a corrected transaction replaces the old copy with
`keep="last"`) and write the state file only after the data file is saved. Common pitfalls:
appending without de-duplication (280 rows after two runs), and storing the time of the run
instead of the latest transaction timestamp.
