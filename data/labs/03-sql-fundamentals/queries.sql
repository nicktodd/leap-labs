-- Module 03 Lab: Basic Queries Against the Enterprise Schema
-- NOTE: Schema uses joined_date (not joined_on), txn_type (not type), account_type (not type)

-- 1. List every client's name and risk profile.


-- 2. List the names of all clients with a "Cautious" risk profile.


-- 3. List all clients who joined before 2018-01-01, ordered by join date, oldest first.


-- 4. List all clients with a risk profile of either "Cautious" or "Adventurous".


-- 4b. Same query using OR instead of IN.


-- 5. List the name and date of birth of every client born in the 1980s.


-- 6. List every instrument's ticker and name, ordered alphabetically by name.


-- 7. List all transactions of type 'DIVIDEND', most recent first.


-- 8. Find every transaction that has no associated instrument (instrument_id IS NULL).


-- 9. List the distinct list of account types that actually exist in the accounts table.


-- 10. List every client along with their date of birth, only for clients whose DOB is not null.
