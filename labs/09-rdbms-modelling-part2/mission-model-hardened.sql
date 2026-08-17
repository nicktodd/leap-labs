-- Module 09 Lab — Hardened DDL for the Mission Model
-- Start from Module 08's first-draft DDL and add NOT NULL, UNIQUE, CHECK constraints,
-- and indexes on FK columns. This DDL is run in the `mission` schema in Module 13.

-- Part A: close the gap — add a client_holdings table


-- Part B: constraints
-- Add NOT NULL where appropriate, a UNIQUE constraint on instruments.ticker, a CHECK on
-- model_portfolio_holdings.target_weight_pct (0-100), and a CHECK on client_holdings.quantity
-- (>= 0).


-- Part C: indexes
-- Add an index on every foreign key column. Then identify one additional column worth
-- indexing, and one you would deliberately leave unindexed — with reasoning for both.


-- Part D: prove it works
-- Run this against a real Postgres database, then try to insert a row that violates one of
-- your constraints and note the actual error message.
