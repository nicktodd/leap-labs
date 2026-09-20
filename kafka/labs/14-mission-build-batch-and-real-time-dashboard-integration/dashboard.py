"""
This Week's Mission Build - the Python week's dashboard, extended.

Same extract_batch()/extract_stream()/transform()/compute_insights() as the
demo. KATA: add ONE more insight - compute_pending_settlement() - that
specifically requires BOTH sources merged. Neither source alone can answer
this question.
"""

import sys
import warnings
from datetime import datetime, timezone
from uuid import uuid4

import pandas as pd
import psycopg2
from kafka import KafkaConsumer

warnings.filterwarnings("ignore", category=DeprecationWarning, module="kafka")

POSTGRES_DSN = "dbname=missionstream user=postgres password=leappass host=localhost port=5434"
KAFKA_BOOTSTRAP = "localhost:9092"
KAFKA_TOPIC = "trade-events"
STREAM_POLL_SECONDS = 5


def extract_batch() -> pd.DataFrame:
    with psycopg2.connect(POSTGRES_DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT settlement_id, account_id, ticker, quantity FROM settled_trades")
            rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=["settlement_id", "account_id", "ticker", "quantity"])
    df["source"] = "batch (settled, end-of-day)"
    return df


def extract_stream() -> pd.DataFrame:
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id=f"dashboard-{uuid4()}",
        auto_offset_reset="earliest",
        consumer_timeout_ms=STREAM_POLL_SECONDS * 1000,
        key_deserializer=lambda k: k.decode("utf-8") if k else None,
        value_deserializer=lambda v: v.decode("utf-8"),
    )

    rows = []
    for record in consumer:
        ticker, side, quantity = record.value.split(",")
        rows.append({
            "settlement_id": None,
            "account_id": record.key,
            "ticker": ticker,
            "quantity": float(quantity),
        })
    consumer.close()

    df = pd.DataFrame(rows, columns=["settlement_id", "account_id", "ticker", "quantity"])
    df["source"] = "stream (live, last few minutes)"
    return df


def transform(batch_df: pd.DataFrame, stream_df: pd.DataFrame) -> pd.DataFrame:
    combined = pd.concat([batch_df, stream_df], ignore_index=True)
    combined["quantity"] = combined["quantity"].astype(float)
    return combined


def compute_insights(df: pd.DataFrame) -> dict:
    by_ticker_source = (
        df.groupby(["ticker", "source"])["quantity"].sum().unstack(fill_value=0)
    )
    total_by_source = df.groupby("source")["quantity"].sum()
    return {
        "by_ticker_source": by_ticker_source,
        "total_by_source": total_by_source,
        "row_count_by_source": df["source"].value_counts(),
    }


# KATA: implement this function.
#
# For each account_id, compute:
#   stream_quantity  = total quantity for that account with source starting "stream"
#   batch_quantity    = total quantity for that account with source starting "batch"
#   pending           = stream_quantity - batch_quantity
#
# "pending" is a rough proxy for "trade volume that has happened (per the
# live stream) but hasn't shown up in the settled batch position yet" - a
# genuinely useful reconciliation signal, and something NEITHER extract
# function alone could tell you.
#
# Return a pandas Series indexed by account_id, sorted descending by pending
# quantity (largest pending amount first).
#
# Hint: df.groupby(["account_id", "source"])["quantity"].sum().unstack(...)
# gives you a table with accounts as rows and sources as columns - similar
# to what compute_insights() already does for tickers.
def compute_pending_settlement(df: pd.DataFrame) -> pd.Series:
    raise NotImplementedError("TODO: implement compute_pending_settlement")


def print_dashboard(insights: dict, pending: pd.Series) -> None:
    print("=== This Week's Mission Dashboard ===")
    print(f"Generated: {datetime.now(timezone.utc).isoformat()}")
    print()
    print("-- Quantity traded, by ticker, by source --")
    print(insights["by_ticker_source"].to_string())
    print()
    print("-- Total quantity, by source --")
    print(insights["total_by_source"].to_string())
    print()
    print("-- Row count, by source --")
    print(insights["row_count_by_source"].to_string())
    print()
    print("-- Pending settlement (stream quantity minus batch quantity), by account --")
    print(pending.to_string())
    print()
    print("Batch total is a settled, complete position as of the last load.")
    print("Stream total is whatever has happened recently - it will keep changing")
    print("on every rerun as new trades are produced. Neither number is 'wrong' -")
    print("they answer different questions.")


def main():
    print("Extracting batch data from Postgres...", file=sys.stderr)
    batch_df = extract_batch()
    print(f"  {len(batch_df)} settled trades.", file=sys.stderr)

    print(f"Extracting stream data from Kafka (polling {STREAM_POLL_SECONDS}s)...", file=sys.stderr)
    stream_df = extract_stream()
    print(f"  {len(stream_df)} live trade events.", file=sys.stderr)

    combined = transform(batch_df, stream_df)
    insights = compute_insights(combined)
    pending = compute_pending_settlement(combined)
    print_dashboard(insights, pending)


if __name__ == "__main__":
    main()
