# Fidelity LEAP Program — Sprint 4 Lab Exercises

This repository contains the hands-on lab exercises accompanying **Sprint 4: Financial Services &
Data Analytics**, week 4 of the Fidelity LEAP graduate programme.

## Prerequisites

- Python 3.11+ and `pip`
- `pandas`, `matplotlib`, `seaborn` (or `plotly`), `requests`, `flask`, `pytest`, `scikit-learn` — installed
  per-module as they're introduced
- GitHub Copilot Chat (continuing as a learning aid, and specifically used in Module 12 to help
  interpret an unfamiliar failing-test error)

## One dataset runs through this whole week

See **[`shared/mission-dataset.md`](shared/mission-dataset.md)**. In short:

- **`shared/trades.csv`** — twenty clean trade records for a fictional wealth platform. Read with
  plain Python from Module 03, then with pandas from Module 05 onward.
- **`shared/messy-trades-raw.csv`** — the same data, deliberately dirtied (bad dates, missing
  values, a duplicate row, inconsistent casing, an outlier) for Module 06's cleaning exercise.
- **`shared/advisors.csv`** — a small reference table (advisor, team, years of experience), used
  from Module 09 onward to demonstrate merging `trades.csv` with a second table.

## Structure

Each module has its own folder under `demos/`, `labs/`, and `solutions/`:

- `demos/<module>/` — instructor-led demo assets and guides
- `labs/<module>/` — your starter files and the task README for that module
- `solutions/<module>/` — reference solutions (try the lab first!)

## Modules

| # | Module | Lab |
|---|---|---|
| 1 | Python Fundamentals: Syntax, Data Types & Control Flow | [labs/01-python-syntax-control-flow/README.md](labs/01-python-syntax-control-flow/README.md) |
| 2 | Python Fundamentals: Functions, Modules & Error Handling | [labs/02-functions-modules-errors/README.md](labs/02-functions-modules-errors/README.md) |
| 3 | Python Data Structures & File I/O | [labs/03-data-structures-file-io/README.md](labs/03-data-structures-file-io/README.md) |
| 4 | Python Fundamentals Consolidation Lab | [labs/04-fundamentals-consolidation/README.md](labs/04-fundamentals-consolidation/README.md) |
| 5 | Pandas Fundamentals: DataFrames & Series | [labs/05-pandas-fundamentals/README.md](labs/05-pandas-fundamentals/README.md) |
| 6 | Data Cleaning & Preparation | [labs/06-data-cleaning/README.md](labs/06-data-cleaning/README.md) |
| 7 | Exploratory Data Analysis (EDA) | [labs/07-eda/README.md](labs/07-eda/README.md) |
| 8 | Statistical Foundations | [labs/08-statistical-foundations/README.md](labs/08-statistical-foundations/README.md) |
| 9 | pandas Deeper Dive — Groupby, Pivot, Merge & Time Series | [labs/09-pandas-deeper-dive/README.md](labs/09-pandas-deeper-dive/README.md) |
| 10 | Data Visualization Principles & Practice | [labs/10-data-visualization/README.md](labs/10-data-visualization/README.md) |
| 11 | Accessing Data Through APIs | [labs/11-apis/README.md](labs/11-apis/README.md) |
| 12 | ETL Concepts & Data Validation | [labs/12-etl-validation/README.md](labs/12-etl-validation/README.md) |
| 13 | Predictive Analytics, Forecasting & Model Evaluation | [labs/13-predictive-analytics/README.md](labs/13-predictive-analytics/README.md) |
| 14 | Capstone: Building the Analytics Dashboard & Sprint 4 Wrap-up | [labs/14-sprint4-capstone-wrapup/README.md](labs/14-sprint4-capstone-wrapup/README.md) |

## Getting started

1. Clone this repository.
2. Create a virtual environment and install dependencies as each module introduces them.
3. Work through the modules in order, starting with `labs/01-python-syntax-control-flow/README.md`.

## Support

Raise questions with your trainer or in the cohort's usual support channel.
