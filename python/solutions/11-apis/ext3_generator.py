"""Extension 3: fetch_all as a generator that yields one row at a time."""
import time

from payments_client import fetch_page, get_session


def iter_transactions(session, limit=20, **filters):
    """Yield transactions one by one, requesting the next page only when it is needed.

    Memory use is one page, not the whole result, and a caller that stops early (for
    example with next() or break) never triggers the requests for the remaining pages.
    """
    cursor = None
    while True:
        resp = fetch_page(session, cursor=cursor, limit=limit, **filters)
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 1))
            print(f"  429 rate limited, waiting {retry_after}s")
            time.sleep(retry_after)
            continue
        body = resp.json()
        yield from body["data"]
        cursor = body["next_cursor"]
        if cursor is None:
            return


if __name__ == "__main__":
    session = get_session()

    # Count without building a list: sum() consumes the generator one row at a time.
    total = sum(1 for _ in iter_transactions(session, limit=20))
    print(f"Counted {total} transactions without holding them in a list")

    fraud_total = sum(row["is_fraud"] for row in iter_transactions(session, limit=50))
    print(f"Confirmed fraud rows: {fraud_total}")

    # Stopping early: the first Online transaction over 1,000 is on the first page or two,
    # so only those pages are requested.
    first_big = next(
        row for row in iter_transactions(session, limit=20)
        if row["channel"] == "Online" and row["amount"] > 1000
    )
    print(f"First Online transaction over 1,000: {first_big['txn_id']} "
          f"{first_big['currency']} {first_big['amount']} at {first_big['merchant']}")
