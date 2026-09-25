# Sprint 4 Lab Dataset: PaySprint Card Payments

The instructor demos use the trades dataset described in [`mission-dataset.md`](mission-dataset.md).
The labs use a second, related dataset from the same fictional firm: one month of card
transactions from PaySprint's card-payments business (Monday 2 February 2026 to Sunday 1 March
2026). Using a different dataset in the labs means each lab applies the demo's techniques to a
new problem, rather than repeating the demo with different parameters.

## Files

- **`shared/transactions.csv`** - 140 clean card transactions. Columns: `txn_id`,
  `txn_timestamp` (`YYYY-MM-DD HH:MM`), `customer_id`, `customer_name`, `merchant`,
  `merchant_category`, `channel` (`Online`, `In-store`, `Contactless`), `country` (ISO 3166
  two-letter code), `currency` (`GBP`, `EUR`, `USD`), `amount` (in the transaction currency),
  `status` (`APPROVED` / `DECLINED`), `distance_from_home_km`, and `is_fraud` (0/1, the outcome
  confirmed by the fraud team after investigation).
- **`shared/messy-transactions-raw.csv`** - 143 raw rows derived from the clean file and
  deliberately dirtied for Modules 06, 12 and 14: amounts stored as text with currency symbols
  and thousands separators, two unrecoverable amounts, channel spelling variants, `UK` instead of
  the ISO code `GB`, whitespace around merchant names, missing merchant categories, a second
  timestamp format, an impossible date, an exact duplicate, a near-duplicate that only appears
  after normalisation, and an outlier.
- **`shared/customers.csv`** - reference data for 11 customers: segment, home country, credit
  limit, and joining date. One customer who appears in the transactions (K012) has no row here,
  which Modules 03, 04, 09 and 11 use to practise handling missing reference data.
- **`shared/fx_rates.csv`** - fixed FX (foreign exchange) rates to GBP (pound sterling) for the
  month: `amount_gbp = amount * rate_to_gbp`.
- **`shared/mock_api/payments_api.py`** - a local mock REST API serving the transactions for
  Module 11 (bearer-token authentication, cursor pagination, filtering, rate limiting, and an
  optional `--flaky` mode). The demo uses the separate `trades_api.py`.

## How it is used across the sprint

| Module | Lab use |
|---|---|
| 01-02 | Hard-coded transaction records: control flow, currency conversion, functions and exceptions |
| 03 | Read `transactions.csv`, `fx_rates.csv` and `customers.csv` with plain Python; write CSV and JSON |
| 04 | A command-line fraud-screening tool, run against the clean and the messy file |
| 05 | pandas selection, filtering and aggregation on `transactions.csv` |
| 06 | Clean `messy-transactions-raw.csv`, documenting each decision |
| 07-08 | Exploratory analysis and statistical tests (decline rates, fraud, skewed amounts) |
| 09 | Merges with `customers.csv` and `fx_rates.csv`, pivots, and daily time series |
| 10 | Charts from the transactions data, and a peer critique |
| 11 | Retrieve the transactions through `payments_api.py` |
| 12 | An ETL (extract, transform, load) pipeline and pytest suite for the messy file |
| 13 | A fraud classifier and a daily-spend forecast |
| 14 | The capstone dashboard, built from the messy file |
