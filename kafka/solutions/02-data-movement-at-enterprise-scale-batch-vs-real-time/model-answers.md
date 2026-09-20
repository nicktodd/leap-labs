# Module 2 - Model Answers

## Scenario A - End-of-Day Settlement: Batch

The dataset is genuinely bounded - "every trade executed today" is a fixed, countable set the
moment the market closes. It also has a hard deadline (the overnight window), which is exactly
the failure mode batch jobs make visible: if it doesn't finish, you know immediately, with a clear
error, not a silent gap. There's no reason to process trade #4,000 the instant it happens when
trade #1 through #3,999 aren't reconciled until the same overnight run anyway.

## Scenario B - A Live Price Feed: Real-Time

Prices are unbounded and continuous by nature - there's no "how many price changes will happen
today" to wait for. More importantly, the whole point of a risk calculation is that it reflects
the *current* state, not a stale snapshot from the last batch run. A batch job that runs every 15
minutes would mean risk calculations are, on average, 7.5 minutes out of date - for a live trading
platform, that's not a performance detail, it's a correctness problem.

## Scenario C - Monthly Client Statements: Batch

Bounded (every client's activity for a fixed calendar month), scheduled (a fixed date), and
nothing about a statement needs to reflect activity that happened one second ago - "as of the
month-end close" is the actual requirement, not "as of right now." Building this as a real-time
stream would mean maintaining always-on infrastructure for something that only needs to run once
a month.

## Discussion Question 1 - What Changes at 100x Volume?

**Scenario A is the one most likely to break first.** End-of-day settlement already has a fixed
window; 100x the trade volume doesn't grow that window. A batch job that comfortably finishes in
4 minutes today might not finish in a 30-minute window at 100x volume - this is exactly the kind
of consequence Module 2's demo flagged, and it's a genuine argument for either scaling the batch
infrastructure significantly or reconsidering whether "one giant end-of-day batch" is still the
right shape at that volume (a common real answer: shrink it via more frequent, smaller batches
throughout the day - not necessarily full real-time). Scenario C (monthly statements) is far less
sensitive to volume growth, since the processing window (a month) scales independently of trade
count in any single day.

## Discussion Question 2 - What Breaks If the Pattern Were Swapped?

- **A price feed built as an hourly batch** would mean risk calculations are silently using
  prices up to 59 minutes stale, with no obvious error - a risk desk could be making decisions on
  wrong numbers with no indication anything is wrong. This is a correctness failure that looks
  exactly like success.
- **End-of-day settlement built as a live stream** would mean there's no natural "we're done"
  signal - a stream has no end, so "has settlement finished for today?" becomes a much harder
  question to answer reliably than "did the batch job exit 0." A downstream system waiting for
  "settlement is complete" would need an entirely separate signalling mechanism that a batch job's
  own completion gives you for free.

## Framing for Discussion

Neither pattern is "more advanced" or "better engineering" than the other - Scenario B genuinely
needs real-time; Scenarios A and C genuinely don't, and building them as real-time anyway would be
pure added cost and complexity for no benefit. The skill this module is teaching is picking the
right one for the actual shape of the data and the actual requirement, not defaulting to whichever
sounds more sophisticated.
