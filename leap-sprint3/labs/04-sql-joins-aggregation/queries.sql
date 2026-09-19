-- Module 04 Lab: Joins and Aggregation Against the Enterprise Schema
-- NOTE: Nadia Farouk (client 11) is already in the schema with no accounts.

-- 1. INNER JOIN: list every client's name alongside their advisor's name.


-- 2a. LEFT JOIN: list every client's name alongside any account they have.
-- Confirm Nadia Farouk appears with NULL account columns.


-- 2b. Rewrite 2a as an INNER JOIN and confirm Nadia Farouk disappears. Why?


-- 3. Three-table join: account ID and type, client name, advisor name.


-- 4. GROUP BY: for each advisor, count how many clients they manage.


-- 5. HAVING: advisors managing three or more clients.


-- 6. Total value of all BUY transactions per account, highest first.


-- 7. Window function: client name and join date, with RANK() by join date.
