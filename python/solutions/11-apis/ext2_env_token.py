"""Extension 2: read the API token from an environment variable, not from source code.

macOS/Linux:   export PAYSPRINT_API_TOKEN=paysprint-lab-token
Windows (PowerShell):   $env:PAYSPRINT_API_TOKEN = "paysprint-lab-token"
Then run:      python ext2_env_token.py
"""
import os
import sys

from payments_client import fetch_page, get_session

TOKEN_ENV_VAR = "PAYSPRINT_API_TOKEN"


def load_token():
    token = os.environ.get(TOKEN_ENV_VAR, "").strip()
    if not token:
        # Fail fast, before any request is made, with a message that says how to fix it.
        # A missing token discovered as a 401 halfway through a pipeline is harder to diagnose.
        sys.exit(
            f"Error: environment variable {TOKEN_ENV_VAR} is not set.\n"
            f"Set it before running, e.g.  export {TOKEN_ENV_VAR}=<your token>"
        )
    return token


if __name__ == "__main__":
    session = get_session(token=load_token())  # no token literal anywhere in this file
    body = fetch_page(session, limit=5).json()
    print(f"Authenticated with the token from {TOKEN_ENV_VAR}: first page has {body['count']} rows")
    print("First txn_ids:", [row["txn_id"] for row in body["data"]])
