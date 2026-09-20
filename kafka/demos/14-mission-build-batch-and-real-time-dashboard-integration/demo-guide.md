# Module 14 Demo Guide - Mission Build: Batch + Real-Time Dashboard Integration

Everything this sprint built lands here. Module 6 designed the trade-events topic. Module 9
implemented a producer publishing to it. Module 7 built an idempotent batch loader into a
Postgres warehouse table. Today: one dashboard, reading from both, at once - exactly what the
mission brief promised in Week 1.

## Setup

Both data sources need to already exist:

```bash
# Postgres warehouse table (Module 7's loader)
docker start missionstream-postgres

# Kafka broker + topic (Module 5/9)
docker start kafka-missionstream
```

```bash
pip install -r requirements.txt
python dashboard.py
```

## Read the Code First

`dashboard.py` follows the Python week's exact ETL shape - `extract()` → `transform()` →
`compute_insights()` → `print_dashboard()` - with ONE change: there are now two extract
functions instead of one.

```python
def extract_batch() -> pd.DataFrame:
    """The batch side: query the warehouse table Module 7's ETL job loads."""
```

```python
def extract_stream() -> pd.DataFrame:
    """The real-time side: read whatever trade events are currently on the Kafka topic."""
```

**Point at this directly**: `transform()`, `compute_insights()`, and `print_dashboard()` are
UNCHANGED from what a single-source version would look like. Neither function knows or cares
whether a row came from Postgres or Kafka - only that every row has the same shape. This is the
same "only the extract layer changes" principle the Python week's own dashboard docstring predicted,
now proven true a full sprint later.

## Run It Once

```bash
python dashboard.py
```

Verified real output:

```
=== This Week's Mission Dashboard ===
-- Total quantity, by source --
source
batch (settled, end-of-day)        3650.0
stream (live, last few minutes)    5280.0

-- Row count, by source --
source
stream (live, last few minutes)    8
batch (settled, end-of-day)        5
```

## Produce More Live Trades, Then Run It Again

```bash
cd ../09-mission-build-implementing-kafka-topics-producers-and-consumers
java -cp "target/classes;$(cat cp.txt)" com.neueda.leap.mission.stream.OrderService
cd ../14-mission-build-batch-and-real-time-dashboard-integration
python dashboard.py
```

Verified real output, second run:

```
-- Total quantity, by source --
source
batch (settled, end-of-day)        3650.0
stream (live, last few minutes)    7920.0

-- Row count, by source --
source
stream (live, last few minutes)    12
batch (settled, end-of-day)         5
```

**This is the entire sprint's argument, made visible in two numbers**: the batch total is
IDENTICAL across both runs - `3650.0`, unchanged - because nothing new was loaded into the
warehouse. The stream total genuinely CHANGED - `5280.0` → `7920.0`, `8` → `12` events - because
new trades were actually produced between the two runs. Neither behavior is a bug. This is
exactly what "batch is a settled position, stream is happening right now" means, demonstrated,
not asserted.

## Why a Fresh `group.id` Every Run

```python
group_id=f"dashboard-{uuid4()}",
```

Module 5 taught `group.id` as "what has this consumer already committed." A persistent service
(like Module 9's `SettlementConsumer`) wants a STABLE `group.id`, so a restart resumes from where
it left off. This dashboard is different: it's a snapshot tool, not a persistent processor - every
run should show the full recent picture, not "only what arrived since the last time I checked."
A random `group_id` every run guarantees a fresh read from the beginning, every time.

**Worth naming as a real design trade-off**: reading from the beginning every run doesn't scale
- a topic with a year of history would make every dashboard run slower and slower. A production
version would read from a bounded time window (e.g., the last hour) instead. This is exactly the
kind of question the lab asks you to reason through.

## The Concept, Named

- **Only the extract layer changes**: the Python week's own dashboard predicted this in its docstring.
  A whole sprint of Kafka and batch-loading content later, the prediction held.
- **Batch = a settled position. Stream = what's happening right now.** Neither is more "correct"
  - they answer genuinely different questions, and a real dashboard often needs both, side by
  side, exactly as built today.
- **`group.id` is a design decision, not a default to accept**: a persistent processor and a
  snapshot tool have opposite needs, and the code should say which one it is.

## Transition to the Lab

Learners extend this dashboard with ONE more insight that specifically requires BOTH sources at
once (not something either source alone could answer) - and reason through the "read from the
beginning every time" scaling question directly.
