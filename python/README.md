# LEAP Program - Sprint 4 Lab Exercises

This repository contains the hands-on lab exercises accompanying **Sprint 4: Financial Services &
Data Analytics**, week 4 of the LEAP graduate programme.

## Prerequisites

- Python 3.11+ and `pip`
- `pandas`, `matplotlib`, `seaborn` (or `plotly`), `requests`, `flask`, `pytest`, `scikit-learn` - installed
  per-module as they're introduced
- GitHub Copilot Chat (continuing as a learning aid, and specifically used in Module 12 to help
  interpret an unfamiliar failing-test error)

## Two datasets: one for the demos, one for the labs

The demos and the labs use different datasets from the same fictional firm, PaySprint. Each lab
applies the techniques shown in the demo to a new problem, so it cannot be completed by copying
the demo code.

**Demos: wealth-platform trades.** See [`shared/mission-dataset.md`](shared/mission-dataset.md).

- **`shared/trades.csv`** - twenty clean trade records.
- **`shared/messy-trades-raw.csv`** - the same data, deliberately dirtied, for the Module 06 demo.
- **`shared/advisors.csv`** - a reference table (advisor, team, years of experience) for the
  Module 09 merge demo.
- **`shared/mock_api/trades_api.py`** - the mock API for the Module 11 demo.

**Labs: card payments.** See [`shared/lab-dataset.md`](shared/lab-dataset.md).

- **`shared/transactions.csv`** - 140 clean card transactions for February 2026, including
  confirmed fraud outcomes.
- **`shared/messy-transactions-raw.csv`** - 143 raw rows with a different set of data-quality
  problems, for Modules 06, 12 and 14.
- **`shared/customers.csv`** and **`shared/fx_rates.csv`** - reference data for customers and FX
  (foreign exchange) rates.
- **`shared/mock_api/payments_api.py`** - the mock API for the Module 11 lab.

## Extension exercises

Every lab ends with **Extension exercises**. They are optional and harder than the core task.
Attempt them once the core acceptance criteria are met. Reference solutions for the extensions
are in the matching `solutions/<module>/` folder, in files named `ext<N>_<topic>.py`, and are
discussed in that folder's `model-answers.md`.

## Output files

Lab scripts write their generated files (reports, CSV and JSON outputs, charts) into an
`output/` folder next to the script. These folders are ignored by git.

## Structure

Each module has its own folder under `demos/`, `labs/`, and `solutions/`:

- `demos/<module>/` - instructor-led demo assets and guides (trades dataset)
- `labs/<module>/` - your starter files and the task README for that module (card-payments dataset)
- `solutions/<module>/` - reference solutions for the core task and the extension exercises
  (attempt the lab first)

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
| 9 | pandas Deeper Dive - Groupby, Pivot, Merge & Time Series | [labs/09-pandas-deeper-dive/README.md](labs/09-pandas-deeper-dive/README.md) |
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
