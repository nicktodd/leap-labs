# Stakeholder Explanation — Sprint 4 Capstone Dashboard

## Why we read the data from a file, not an API

We loaded the trade data from a local CSV file (`trades.csv`) rather than fetching it through
the REST API we built in Module 11. The reason is straightforward: the dataset contains 20
daily trade records that are refreshed once per business day — there is no intraday update, no
real-time feed, and no need to call a server repeatedly. Pulling from a file is simpler, faster,
and has no risk of hitting a rate limit or network error. The API we explored in Module 11 is
the right tool when you need live data or when the source system only exposes an API — for a
small, static daily file, it just adds unnecessary complexity.

## Why we are confident the data is trustworthy

Before producing any numbers, we ran the raw data through a cleaning and validation process
(Modules 6 and 12). Specifically:

- We removed one trade record that was missing its quantity — it could not be reliably
  reconstructed, so keeping it would have produced a misleading value.
- We recomputed one trade's value from its quantity and price, confirming the arithmetic
  matched the pattern of all other trades in the dataset.
- We corrected one inconsistently formatted date (written as day/month/year instead of the
  standard year-month-day) by cross-checking it against the surrounding trade sequence — we
  did not guess.
- We removed one exact duplicate record, preventing any trade from being counted twice.
- We ran five automated checks (using pytest) that confirm: every trade has an ID, all
  quantities are positive, no values are negative, all asset types are recognised, and no
  trade ID is repeated.

In short, every number in this dashboard has passed through a documented cleaning step and
a specific automated test. If a future data extract introduced a new problem — a missing value,
a duplicate, an unrecognised asset type — the test suite would flag it before any results were
published.
