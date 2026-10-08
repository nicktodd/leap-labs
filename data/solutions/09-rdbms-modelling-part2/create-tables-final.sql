-- Module 09 Lab — Hardened Mission Model DDL (Instructor Reference)
-- Assumes `advisors` already exists (reused from the enterprise schema).

CREATE TABLE clients (
    client_id   SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    advisor_id  INTEGER NOT NULL REFERENCES advisors(advisor_id)
);
CREATE INDEX idx_clients_advisor_id ON clients(advisor_id);

CREATE TABLE model_portfolios (
    model_portfolio_id  SERIAL PRIMARY KEY,
    name                TEXT NOT NULL UNIQUE
);

CREATE TABLE instruments (
    instrument_id  SERIAL PRIMARY KEY,
    ticker         TEXT NOT NULL UNIQUE,
    name           TEXT NOT NULL,
    asset_class    TEXT NOT NULL,
    currency       CHAR(3) NOT NULL
);

-- Part A.2: keeping history, as the mission brief requires.
-- Requirement 1: a model portfolio's target composition can change (e.g. a
-- rebalance), and we must know what it looked like at any point in the past.
-- So a target weight is never updated in place: the old row is closed by
-- setting effective_to, and a new row is inserted with a new effective_from.
-- The current composition is the rows where effective_to IS NULL.
-- effective_from is part of the key, so the same instrument can appear in the
-- same portfolio more than once over time.
CREATE TABLE model_portfolio_holdings (
    model_portfolio_id  INTEGER NOT NULL REFERENCES model_portfolios(model_portfolio_id),
    instrument_id       INTEGER NOT NULL REFERENCES instruments(instrument_id),
    target_weight_pct   NUMERIC(5,2) NOT NULL CHECK (target_weight_pct BETWEEN 0 AND 100),
    effective_from      DATE NOT NULL DEFAULT CURRENT_DATE,
    effective_to        DATE,  -- NULL = still the current target
    PRIMARY KEY (model_portfolio_id, instrument_id, effective_from),
    CHECK (effective_to IS NULL OR effective_to > effective_from)
);
CREATE INDEX idx_mph_instrument_id ON model_portfolio_holdings(instrument_id);

-- Requirement 2: a client can change model portfolio over time, and we keep
-- that history. A switch closes the old subscription (ended_date) and inserts
-- a new one. The current subscription is the row where ended_date IS NULL.
CREATE TABLE client_subscriptions (
    client_id           INTEGER NOT NULL REFERENCES clients(client_id),
    model_portfolio_id  INTEGER NOT NULL REFERENCES model_portfolios(model_portfolio_id),
    subscribed_date     DATE NOT NULL,
    ended_date          DATE,  -- NULL = current subscription
    PRIMARY KEY (client_id, model_portfolio_id, subscribed_date),
    CHECK (ended_date IS NULL OR ended_date > subscribed_date)
);
CREATE INDEX idx_cs_model_portfolio_id ON client_subscriptions(model_portfolio_id);
-- At most one current subscription per client (a partial unique index):
CREATE UNIQUE INDEX uq_cs_one_current_per_client
    ON client_subscriptions(client_id) WHERE ended_date IS NULL;

-- Part A: closing Module 08's gap
CREATE TABLE client_holdings (
    client_id      INTEGER NOT NULL REFERENCES clients(client_id),
    instrument_id  INTEGER NOT NULL REFERENCES instruments(instrument_id),
    quantity       NUMERIC(14,4) NOT NULL CHECK (quantity >= 0),
    as_of_date     DATE NOT NULL,
    PRIMARY KEY (client_id, instrument_id, as_of_date)
);
-- Primary key rationale: a client can hold the same instrument as of different
-- dates over time (this is a snapshot, not a running total), so client_id +
-- instrument_id alone isn't unique enough, as_of_date must be part of the key.
CREATE INDEX idx_ch_instrument_id ON client_holdings(instrument_id);

-- Part C.9: an additional index worth adding
-- Reporting on a client's current holdings vs their model portfolio's target
-- (the mission brief's core report) will filter client_holdings by client_id
-- and the most recent as_of_date constantly. client_id is already indexed as
-- part of the primary key, but a report frequently querying "most recent
-- as_of_date per client" benefits from:
CREATE INDEX idx_ch_client_asof ON client_holdings(client_id, as_of_date DESC);

-- Part C.10: a column deliberately NOT indexed
-- model_portfolios.name is UNIQUE (so it already has an index from that
-- constraint), but a column like clients.name would NOT be worth a
-- dedicated index here: this schema is small, name is rarely the sole
-- filter in a query (usually joined via client_id instead), and free-text
-- name search would need a different kind of index entirely (e.g. a trigram
-- index), not a plain B-tree.

-- Part E.13: EXPLAIN ANALYZE before and after an index
-- Run the same query with and without an index on the column it filters on.
-- (With only a handful of rows Postgres may still prefer a Seq Scan; the
-- point is to read the plan. SET enable_seqscan = off; shows the index plan
-- on a tiny table, remember to SET it back on afterwards.)
DROP INDEX IF EXISTS idx_ch_instrument_id;
EXPLAIN ANALYZE SELECT * FROM client_holdings WHERE instrument_id = 7;
-- Expected: Seq Scan on client_holdings ... Filter: (instrument_id = 7)
--           Rows Removed by Filter: n
CREATE INDEX idx_ch_instrument_id ON client_holdings(instrument_id);
EXPLAIN ANALYZE SELECT * FROM client_holdings WHERE instrument_id = 7;
-- Expected (on enough rows, or with enable_seqscan off):
--   Index Scan / Bitmap Index Scan using idx_ch_instrument_id
--   Index Cond: (instrument_id = 7), and no "Rows Removed by Filter"

-- Part E.14: rewrite a function-wrapped column so it can use an index
-- Before: UPPER() runs on every row, so the UNIQUE index on ticker can't be used
EXPLAIN ANALYZE SELECT instrument_id, ticker FROM instruments WHERE UPPER(ticker) = 'GLBEQ1';
-- After: filter on the raw column (tickers are stored upper case already)
EXPLAIN ANALYZE SELECT instrument_id, ticker FROM instruments WHERE ticker = 'GLBEQ1';
-- If case-insensitive search were genuinely needed, the alternative is an
-- expression index: CREATE INDEX ON instruments (UPPER(ticker));

-- History queries the brief now supports (requirement 1 and 2)
-- Current target composition of every portfolio:
--   SELECT * FROM model_portfolio_holdings WHERE effective_to IS NULL;
-- Composition as it was on a past date, e.g. 2024-01-01:
--   SELECT * FROM model_portfolio_holdings
--   WHERE effective_from <= DATE '2024-01-01'
--     AND (effective_to IS NULL OR effective_to > DATE '2024-01-01');
-- A client's full subscription history:
--   SELECT * FROM client_subscriptions WHERE client_id = 1 ORDER BY subscribed_date;
