-- Module 13 Lab — Verification Queries (Instructor Reference)

-- 8. Each portfolio's current target composition, readable end to end
SELECT mp.name AS portfolio, i.ticker, i.name AS instrument_name, mph.target_weight_pct
FROM model_portfolio_holdings mph
JOIN model_portfolios mp ON mph.model_portfolio_id = mp.model_portfolio_id
JOIN instruments i ON mph.instrument_id = i.instrument_id
WHERE mph.effective_to IS NULL
ORDER BY mp.name, mph.target_weight_pct DESC;

-- 8b. History: Balanced Growth's composition as it was on 2024-06-30
-- (before the 2025-01-01 rebalance), expected 50 / 30 / 20
SELECT mp.name AS portfolio, i.ticker, mph.target_weight_pct
FROM model_portfolio_holdings mph
JOIN model_portfolios mp ON mph.model_portfolio_id = mp.model_portfolio_id
JOIN instruments i ON mph.instrument_id = i.instrument_id
WHERE mp.name = 'Balanced Growth'
  AND mph.effective_from <= DATE '2024-06-30'
  AND (mph.effective_to IS NULL OR mph.effective_to > DATE '2024-06-30')
ORDER BY mph.target_weight_pct DESC;

-- 9. Which client is subscribed to which portfolio, including past
-- subscriptions (David Kim should show two rows, one ended)
SELECT c.name AS client_name, mp.name AS model_portfolio, cs.subscribed_date, cs.ended_date
FROM client_subscriptions cs
JOIN clients c ON cs.client_id = c.client_id
JOIN model_portfolios mp ON cs.model_portfolio_id = mp.model_portfolio_id
ORDER BY c.name, cs.subscribed_date;

-- 10. Deliberately violate a constraint
INSERT INTO model_portfolio_holdings (model_portfolio_id, instrument_id, target_weight_pct)
VALUES (1, 5, 150);
-- Expected: ERROR: new row for relation "model_portfolio_holdings" violates
-- check constraint "model_portfolio_holdings_target_weight_pct_check"

-- Finish-early extension: one client's actual holdings vs their target weights
SELECT c.name, i.ticker,
       ch.quantity AS actual_quantity,
       mph.target_weight_pct
FROM clients c
JOIN client_subscriptions cs ON c.client_id = cs.client_id AND cs.ended_date IS NULL
JOIN model_portfolio_holdings mph ON cs.model_portfolio_id = mph.model_portfolio_id
                                 AND mph.effective_to IS NULL
JOIN instruments i ON mph.instrument_id = i.instrument_id
LEFT JOIN client_holdings ch ON ch.client_id = c.client_id AND ch.instrument_id = mph.instrument_id
WHERE c.name = 'David Kim'
ORDER BY i.ticker;
-- Note: this shows quantity next to a target *percentage*, not a directly
-- comparable pair, exactly the gap Module 10 uncovered: without a price per
-- holding, quantity can't be turned into a percentage of portfolio value.
-- A good outcome here is a team noticing that limitation again, in practice.
