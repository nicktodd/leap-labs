# Demo: Module 7 — Exploratory Data Analysis (EDA)

**Duration:** 18 minutes
**Files:** `eda_demo.py`
**Data:** `shared/trades.csv` (already clean, from Module 6)

## Part 1: What EDA actually is (3 min)

Narration: EDA isn't a fixed checklist of functions to run, it's a mindset — look at the data
*before* you assume you know what's in it, and let what you find shape your next question. The
process this demo follows: shape and summary statistics first, then break the data down by
category, then look for something surprising, then write down a hypothesis worth testing later.

## Part 2: Shape and summary statistics (4 min)

Run `df.describe()` and `df.shape`. Narration: `describe()` only summarises numeric columns —
point out that `quantity` and `value`'s ranges look sensible now (Module 6 cleaned this same
dataset's messy twin), but the range alone doesn't tell you *why* they vary, that needs the next
step: segmenting.

## Part 3: Segmenting with value_counts and groupby (6 min)

Show `df["asset_class"].value_counts()` — Equity dominates (11 of 20 trades). Then
`df["advisor"].value_counts()` — J. Okafor has almost double R. Alvarez's trade count.

Narration: neither of these is "the answer" to anything yet, they're **patterns worth
questioning**. Is Equity dominance because Equity is genuinely the desk's focus, or because this
particular week happened to have more Equity activity? Is J. Okafor's higher count because they
manage more clients, or because they trade more per client? EDA surfaces the question; it
doesn't answer it by itself.

## Part 4: A segment-level comparison, and a hypothesis (5 min)

Show `df.groupby("side")["value"].agg(["count", "mean", "sum"])`. Narration: BUY trades
outnumber SELL trades 14 to 6 in this dataset. Form a testable hypothesis out loud: *"BUY trades
are, on average, larger in value than SELL trades in this book."* Check the `mean` column against
that hypothesis, then flag it explicitly as something Module 8's statistical tools (correlation,
not just eyeballing an average) would actually test properly, not something this module claims
to prove.

## Key message

EDA's job is to surface patterns, anomalies, and segments, and to turn what you notice into a
specific, checkable hypothesis. It is deliberately *not* the step where you prove anything —
that's what Module 8's statistical foundations are for.
