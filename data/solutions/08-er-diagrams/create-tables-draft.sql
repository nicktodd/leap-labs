-- Module 08 Lab — First-Draft DDL for the Mission Model (Instructor Reference)
-- Deliberately minimal: PKs and FKs only. Module 09 adds indexes, CHECK
-- constraints, and anything beyond the obvious NOT NULLs.

CREATE TABLE clients (
    client_id   SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    advisor_id  INTEGER REFERENCES advisors(advisor_id)
);

CREATE TABLE model_portfolios (
    model_portfolio_id  SERIAL PRIMARY KEY,
    name                TEXT NOT NULL
);

CREATE TABLE instruments (
    instrument_id  SERIAL PRIMARY KEY,
    ticker         TEXT NOT NULL,
    name           TEXT NOT NULL
);

CREATE TABLE model_portfolio_holdings (
    model_portfolio_id  INTEGER REFERENCES model_portfolios(model_portfolio_id),
    instrument_id       INTEGER REFERENCES instruments(instrument_id),
    target_weight_pct   NUMERIC(5,2) NOT NULL,
    effective_from      DATE NOT NULL,
    effective_to        DATE,
    PRIMARY KEY (model_portfolio_id, instrument_id, effective_from)
);
-- Note: effective_from / effective_to are here because requirement 1 of the
-- mission brief asks for the HISTORY of each portfolio's target composition
-- ("what it looked like at any point in the past"). A rebalance closes the old
-- rows (effective_to) and inserts new ones; NULL effective_to = current.

CREATE TABLE client_subscriptions (
    client_id           INTEGER REFERENCES clients(client_id),
    model_portfolio_id  INTEGER REFERENCES model_portfolios(model_portfolio_id),
    subscribed_date     DATE NOT NULL,
    ended_date          DATE,
    PRIMARY KEY (client_id, model_portfolio_id, subscribed_date)
);
-- Note: subscribed_date is part of the key here because the mission brief
-- asks us to keep subscription HISTORY (a client can change portfolios over
-- time), not just their current one. A simpler (client_id, model_portfolio_id)
-- key would only allow one subscription ever per client/portfolio pair.
-- ended_date (NULL = current) records when a client left a portfolio.
