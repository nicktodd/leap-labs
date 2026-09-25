"""Module 11 lab starter: a client for the PaySprint payments API.

Start the API first, in its own terminal:   python shared/mock_api/payments_api.py
Then run:                                   python starter_payments_client.py
"""
from pathlib import Path
import time

import pandas as pd
import requests

SHARED = Path(__file__).resolve().parents[2] / "shared"
BASE_URL = "http://127.0.0.1:5051"
API_TOKEN = "paysprint-lab-token"  # throwaway token for a local mock server (see Extension 2)
REQUEST_TIMEOUT = 10  # seconds


class ApiAuthError(Exception):
    """Raised when the API rejects our credentials (HTTP 401)."""


def get_session(token=API_TOKEN):
    """TODO (step 1): create a requests.Session, set the header
    Authorization: Bearer <token> on it once, and return it.
    Add a comment explaining why a Session is used instead of requests.get()."""
    raise NotImplementedError


def fetch_page(session, cursor=None, limit=20, **filters):
    """TODO (step 2): make ONE GET request to BASE_URL + "/transactions" with params
    limit, cursor (only when not None) and any filters (status, customer_id, since).
    - 401: raise ApiAuthError with a clear message
    - 429: return the response unchanged (the caller decides how to wait)
    - anything else: call resp.raise_for_status(), then return the response"""
    raise NotImplementedError


def fetch_all(session, limit=20, **filters):
    """TODO (step 3): call fetch_page in a loop, following body["next_cursor"] until it
    is None, and return all rows as a list of dicts. On a 429, sleep for the
    Retry-After header's number of seconds, then retry the SAME cursor."""
    raise NotImplementedError


def fetch_customer(session, customer_id):
    """TODO (step 6): GET BASE_URL + "/customers/<customer_id>". Return the customer
    dict, or None on a 404. Handle 429 the same way as fetch_all."""
    raise NotImplementedError


if __name__ == "__main__":
    session = get_session()

    # TODO (step 2): show that a session with a wrong token raises ApiAuthError, and
    #   print the exception message instead of crashing.

    # TODO (step 4): df = pd.DataFrame(fetch_all(session)); compare with
    #   pd.read_csv(SHARED / "transactions.csv"): print the shape and whether the
    #   txn_id sets are identical.

    # TODO (step 5): fetch status="DECLINED", since="2026-02-15" with server-side filters,
    #   filter the full download the same way in pandas, and print whether the rows match.
    #   Comment: which approach is preferable, and when?

    # TODO (step 6): for each distinct customer_id in the declined set, call
    #   fetch_customer and print the segment, or a clear message when there is no record.

    # TODO (step 7): comment - for this dataset, API or nightly extract? Why?
