"""
Sprint 7 Mission Build - the Sprint 4 dashboard, extended.

Sprint 4's dashboard.py had one extract() reading a local CSV. This version
has TWO extract functions - one per data-movement pattern this sprint spent
14 modules teaching - merged into one combined view, exactly as the mission
brief promised: "two different data-movement patterns, feeding one
dashboard, each used where it's actually the right tool."

  extract_batch()  - settled_trades, the Postgres warehouse table Module 7's
                      idempotent loader populated. End-of-day, complete,
                      slow-moving. This is TODAY's settlement position.

  extract_stream()  - trade-events, the Kafka topic Module 9's OrderService
                      publishes to. Whatever has happened in roughly the
                      last few minutes. Fast-moving, may be incomplete.

Only the extract layer changed. transform(), compute_insights(), and
print_dashboard() don't care where a row came from - only that every row
has the same shape (ticker, account_id, quantity, source).
"""

import sys
import warnings
from datetime import datetime, timezone
from uuid import uuid4

warnings.filterwarnings("ignore", category=DeprecationWarning, module="kafka")

import pandas as pd
import psycopg2
from kafka import KafkaConsumer

POSTGRES_DSN = "dbname=sprint7 user=postgres password=leappass host=localhost port=5434"
KAFKA_BOOTSTRAP = "localhost:9092"
KAFKA_TOPIC = "trade-events"
STREAM_POLL_SECONDS = 5


def extract_batch() -> pd.DataFrame:
    """The batch side: query the warehouse table Module 7's ETL job loads."""
    with psycopg2.connect(POSTGRES_DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT settlement_id, account_id, ticker, quantity FROM settled_trades")
            rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=["settlement_id", "account_id", "ticker", "quantity"])
    df["source"] = "batch (settled, end-of-day)"
    return df


def extract_stream() -> pd.DataFrame:
    """
    The real-time side: read whatever trade events are currently on the
    Kafka topic.

    A fresh, random group.id every run is DELIBERATE, not an oversight -
    Module 5 taught group.id as "what has this consumer already seen."
    A dashboard snapshot tool isn't a persistent processor tracking its own
    progress; every run wants the FULL recent picture, not "only what's
    arrived since I last checked." A real production version of this would
    likely read from a bounded time window instead of from the beginning -
    left as a design question for the lab.
    """
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
    """Combine both sources into one shape. Neither knows the other exists."""
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


def print_dashboard(insights: dict) -> None:
    print("=== Sprint 7 Mission Dashboard ===")
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
    print_dashboard(insights)


if __name__ == "__main__":
    main()
