# Sprint 4 Mission Dataset

One dataset runs through this whole week: a small book of trade records for a fictional wealth
platform, "PaySprint" (the same fictional firm behind Sprint 3's enterprise schema, now viewed
from an analytics angle rather than a relational-schema angle).

## Files

- **`shared/trades.csv`** — twenty clean trade records: trade id, date, client, advisor,
  instrument, asset class, side (BUY/SELL), quantity, price, currency, and value. Used from
  Module 03 (plain-Python file I/O) onward as "the mission dataset."
- **`shared/messy-trades-raw.csv`** — the same data, deliberately dirtied: an inconsistent date
  format (`05/01/2026` vs `2026-01-05`), missing values (blank quantity, blank value, blank
  client name), a duplicated row, inconsistent casing (`equity` vs `Equity`), and a single
  extreme outlier (a 99,999-unit trade). Used specifically in Module 06's cleaning exercise —
  every issue seeded here has a matching, nameable pandas cleaning technique.
- **`shared/advisors.csv`** — a small reference table (advisor, team, years of experience).
  Introduced in Module 09 to demonstrate `merge`, combining `trades.csv` with a second table.

## How it's used across the sprint

| Module | Use |
|---|---|
| 03 | Read `trades.csv` with plain Python, no libraries, to compute a simple summary |
| 05 | Load the same file into pandas and compare the two approaches |
| 06 | Clean `messy-trades-raw.csv`, documenting each decision |
| 07 | Exploratory Data Analysis on the (clean) mission dataset |
| 08 | Statistical foundations: correlation between two variables in the dataset |
| 09 | groupby / pivot / merge / time series on the mission dataset |
| 10 | Visualizations built from the mission dataset |
| 12 | Validated as part of a small ETL/validation pipeline |
| 13 | A simple predictive model built on the mission dataset |
| 14 | Folded into the capstone analytics dashboard |

Keeping one dataset across the whole sprint means later modules never have to explain a new
domain, delegates already know what a "trade," a "client," and an "instrument" are from Module 03
onward.
