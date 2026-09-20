"""A small, self-contained mock REST API serving the mission dataset.

Runs entirely locally (no internet/third-party dependency), so labs are not at the
mercy of a real API's uptime, rate limits, or terms of use. It deliberately implements
the three things Module 11 is about: an API key check, pagination, and a rate limit.

Run with: python trades_api.py
Then in another terminal, run a client script against http://127.0.0.1:5050
"""
import time
from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, request

DATA_PATH = Path(__file__).resolve().parent.parent / "trades.csv"
API_KEY = "leap-python-key"
RATE_LIMIT_MAX_REQUESTS = 5
RATE_LIMIT_WINDOW_SECONDS = 10

app = Flask(__name__)
_trades = pd.read_csv(DATA_PATH).to_dict(orient="records")
_request_log = []  # timestamps of recent requests, for the rate limiter


def _check_rate_limit():
    now = time.time()
    while _request_log and _request_log[0] < now - RATE_LIMIT_WINDOW_SECONDS:
        _request_log.pop(0)
    if len(_request_log) >= RATE_LIMIT_MAX_REQUESTS:
        retry_after = int(RATE_LIMIT_WINDOW_SECONDS - (now - _request_log[0])) + 1
        return retry_after
    _request_log.append(now)
    return None


@app.route("/trades")
def get_trades():
    if request.headers.get("X-API-Key") != API_KEY:
        return jsonify({"error": "missing or invalid API key"}), 401

    retry_after = _check_rate_limit()
    if retry_after is not None:
        response = jsonify({"error": "rate limit exceeded", "retry_after": retry_after})
        response.status_code = 429
        response.headers["Retry-After"] = str(retry_after)
        return response

    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=5, type=int)
    if page < 1 or page_size < 1:
        return jsonify({"error": "page and page_size must be positive integers"}), 400

    start = (page - 1) * page_size
    end = start + page_size
    page_data = _trades[start:end]
    total_records = len(_trades)
    total_pages = (total_records + page_size - 1) // page_size

    return jsonify({
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "total_records": total_records,
        "data": page_data,
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050)
