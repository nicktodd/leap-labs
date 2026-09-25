"""A small, self-contained mock REST API serving the PaySprint card-payments lab dataset.

This is the API used by the Module 11 lab (the demo uses trades_api.py instead). It
differs from the demo API on purpose, so the lab exercises techniques the demo does not:

- Authentication is a bearer token in the Authorization header, not an X-API-Key header.
- Pagination is cursor-based (follow next_cursor until it is null), not page-numbered.
- The server can filter (status, customer_id, since) before paginating.
- GET /customers/<customer_id> returns 404 for a customer with no reference record.
- An optional --flaky mode makes every fourth request fail with 503, for the retry extension.

Run with:   python payments_api.py            (normal mode)
            python payments_api.py --flaky    (transient 503 errors, for Extension 1)
Then run a client script against http://127.0.0.1:5051
"""
import argparse
import base64
import time
from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, request

SHARED = Path(__file__).resolve().parent.parent
API_TOKEN = "paysprint-lab-token"
MAX_LIMIT = 50
RATE_LIMIT_MAX_REQUESTS = 5
RATE_LIMIT_WINDOW_SECONDS = 10

app = Flask(__name__)
_transactions = pd.read_csv(SHARED / "transactions.csv").to_dict(orient="records")
_customers = {c["customer_id"]: c for c in pd.read_csv(SHARED / "customers.csv").to_dict(orient="records")}
_request_log = []  # timestamps of recent requests, for the rate limiter
_state = {"flaky": False, "request_count": 0}


def _encode_cursor(offset):
    return base64.urlsafe_b64encode(f"offset:{offset}".encode()).decode()


def _decode_cursor(cursor):
    try:
        prefix, offset = base64.urlsafe_b64decode(cursor.encode()).decode().split(":")
        if prefix != "offset":
            raise ValueError
        return int(offset)
    except (ValueError, UnicodeDecodeError):
        return None


def _check_auth():
    header = request.headers.get("Authorization", "")
    if header != f"Bearer {API_TOKEN}":
        return jsonify({"error": "missing or invalid bearer token"}), 401
    return None


def _check_rate_limit():
    now = time.time()
    while _request_log and _request_log[0] < now - RATE_LIMIT_WINDOW_SECONDS:
        _request_log.pop(0)
    if len(_request_log) >= RATE_LIMIT_MAX_REQUESTS:
        retry_after = int(RATE_LIMIT_WINDOW_SECONDS - (now - _request_log[0])) + 1
        response = jsonify({"error": "rate limit exceeded", "retry_after": retry_after})
        response.status_code = 429
        response.headers["Retry-After"] = str(retry_after)
        return response
    _request_log.append(now)
    return None


def _check_flaky():
    _state["request_count"] += 1
    if _state["flaky"] and _state["request_count"] % 4 == 0:
        return jsonify({"error": "service temporarily unavailable"}), 503
    return None


@app.before_request
def _guards():
    for check in (_check_auth, _check_rate_limit, _check_flaky):
        failure = check()
        if failure is not None:
            return failure
    return None


@app.route("/transactions")
def get_transactions():
    limit = request.args.get("limit", default=20, type=int)
    if limit < 1 or limit > MAX_LIMIT:
        return jsonify({"error": f"limit must be between 1 and {MAX_LIMIT}"}), 400

    offset = 0
    cursor = request.args.get("cursor")
    if cursor:
        offset = _decode_cursor(cursor)
        if offset is None:
            return jsonify({"error": "invalid cursor"}), 400

    rows = _transactions
    status = request.args.get("status")
    if status:
        rows = [r for r in rows if r["status"] == status.upper()]
    customer_id = request.args.get("customer_id")
    if customer_id:
        rows = [r for r in rows if r["customer_id"] == customer_id]
    since = request.args.get("since")  # YYYY-MM-DD, inclusive
    if since:
        rows = [r for r in rows if r["txn_timestamp"][:10] >= since]

    page = rows[offset:offset + limit]
    next_offset = offset + limit
    next_cursor = _encode_cursor(next_offset) if next_offset < len(rows) else None
    return jsonify({"data": page, "count": len(page), "next_cursor": next_cursor})


@app.route("/customers/<customer_id>")
def get_customer(customer_id):
    customer = _customers.get(customer_id)
    if customer is None:
        return jsonify({"error": f"customer {customer_id} not found"}), 404
    return jsonify(customer)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PaySprint mock payments API")
    parser.add_argument("--flaky", action="store_true", help="fail every fourth request with 503")
    args = parser.parse_args()
    _state["flaky"] = args.flaky
    app.run(host="127.0.0.1", port=5051)
