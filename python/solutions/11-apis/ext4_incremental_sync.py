"""Extension 4: incremental sync.

The first run downloads everything. Each later run asks only for transactions since the
last date seen. Run the script twice and compare the output.
"""
from pathlib import Path

import pandas as pd

from payments_client import fetch_all, get_session

OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)
STATE_FILE = OUT / "last_sync.txt"
SYNCED_CSV = OUT / "transactions_synced.csv"


def sync(session):
    if STATE_FILE.exists():
        last_ts = STATE_FILE.read_text().strip()
        # The API's since filter has date granularity, so this re-fetches every transaction
        # on the last synced date, including the ones already stored. The overlap is
        # deliberate: asking for "the day after" would miss transactions that arrived later
        # on that same day. De-duplicating on txn_id below removes the overlap.
        since = last_ts[:10]
        print(f"Last sync reached {last_ts}; fetching since={since}")
        new_rows = pd.DataFrame(fetch_all(session, limit=50, since=since))
    else:
        print("No previous sync found; fetching everything")
        new_rows = pd.DataFrame(fetch_all(session, limit=50))

    if SYNCED_CSV.exists():
        existing = pd.read_csv(SYNCED_CSV)
        combined = pd.concat([existing, new_rows[existing.columns]], ignore_index=True)
    else:
        existing = None
        combined = new_rows

    before = len(combined)
    # keep="last": if the source corrected a transaction, the newer copy wins.
    combined = combined.drop_duplicates(subset="txn_id", keep="last")
    combined = combined.sort_values("txn_id").reset_index(drop=True)
    combined.to_csv(SYNCED_CSV, index=False)
    STATE_FILE.write_text(combined["txn_timestamp"].max())

    print(f"Fetched {len(new_rows)} rows; stored before this run: "
          f"{0 if existing is None else len(existing)}; "
          f"duplicates removed: {before - len(combined)}; stored now: {len(combined)}")
    print(f"Wrote {SYNCED_CSV.name}; {STATE_FILE.name} = {STATE_FILE.read_text()}")


if __name__ == "__main__":
    sync(get_session())
