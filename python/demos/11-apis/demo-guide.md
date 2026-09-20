# Demo: Module 11 - Accessing Data Through APIs

**Duration:** 20 minutes
**Files:** `api_client_demo.py`, `shared/mock_api/trades_api.py`
**Prerequisite:** `pip install flask requests pandas`

This module uses a small, self-contained mock API (`shared/mock_api/trades_api.py`) serving the
mission dataset, rather than a real third-party API - so the lab never depends on internet
access, a real API's uptime, or someone else's rate limits. Everything it demonstrates (an API
key, pagination, a rate limit) is genuinely present in the mock server, not simulated.

## Setup for this demo

In one terminal: `python shared/mock_api/trades_api.py` (leave it running).
In a second terminal: run `api_client_demo.py`.

## Part 1: Endpoints and authentication (4 min)

Show a request with no API key first - `401`. Then the same request with
`headers={"X-API-Key": "leap-python-key"}` - `200`.

Narration: an endpoint is just a URL the server understands; almost every real API requires some
form of authentication on every request, most commonly an API key or a bearer token in a header.
Never hardcode a real API key into source code that gets committed - this demo's key is a
throwaway local secret for a mock server, not a real credential, which is precisely why it's safe
to have it in plain text here.

## Part 2: Pagination (6 min)

Show one request: `GET /trades?page=1&page_size=5`. Point out the response shape:
`page`, `page_size`, `total_pages`, `total_records`, and `data` (only this page's rows).

Narration: a real API essentially never returns every record in one response - pagination limits
each response to a manageable size. The client's job is to keep requesting the next page until
`page == total_pages`, accumulating `data` from each response.

## Part 3: Rate limits (5 min)

Show the demo hitting the API repeatedly in a tight loop with no delay - after a handful of
requests, `429` with a `Retry-After` header. Narration: a rate limit protects the server from
being overwhelmed; a well-behaved client reads `Retry-After` and waits that long before retrying,
rather than hammering the endpoint or giving up. Show the fixed version: on `429`, sleep for
`Retry-After` seconds, then retry the same page.

## Part 4: API vs. extract - when to use which (5 min)

Narration, a genuine judgement call, not a rule: an API is the right choice when you need
current, frequently-changing data, only a subset of records, or to trigger something (not just
read data). A batch extract (a file drop, a scheduled export) is often better when you need a
large, complete dataset infrequently, since it avoids pagination and rate-limit overhead
entirely, and doesn't depend on the source system being available at query time. Module 12's ETL
content picks this distinction up directly.

## Key message

A REST API's contract is usually: authenticate every request, expect paginated results, and
respect rate limits by backing off, not retrying blindly. All three are things a client must
handle explicitly - none of them are optional extras.
