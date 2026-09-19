-- Module 06 Lab — Reference Answers (Instructor Reference)

-- 1. Missing data
SELECT * FROM raw_client_intake
WHERE full_name IS NULL
   OR date_of_birth IS NULL;
-- Two rows: one with a NULL full_name (submitted 2026-01-07), one with a
-- NULL date_of_birth (Aisha Bello, submitted 2026-01-08).

-- 2. Exact duplicates
SELECT full_name, date_of_birth, email, COUNT(*)
FROM raw_client_intake
GROUP BY full_name, date_of_birth, email
HAVING COUNT(*) > 1;
-- Tomasz Nowak, submitted twice (2026-01-06 and 2026-01-09).

-- 3. Distinct risk_profile values
SELECT DISTINCT risk_profile
FROM raw_client_intake
ORDER BY risk_profile;
-- Returns: ADVENTUROUS, Adventurous, adventurous, Balanced, balanced,
-- Cautious, cautious, Moderate. Seven rows represent three real values
-- (Adventurous, Balanced, Cautious) in mixed casing; 'Moderate' is not a
-- casing variant of any of them, it's an eighth, invalid value.

-- 4. Invalid risk_profile values
SELECT * FROM raw_client_intake
WHERE LOWER(risk_profile) NOT IN ('cautious', 'balanced', 'adventurous');
-- Only Chloe Bennett's 'Moderate' row. Normalising case would not fix this,
-- it is not one of the three real risk profiles at all.

-- 5. Whitespace-padded names
SELECT full_name, LENGTH(full_name), LENGTH(TRIM(full_name))
FROM raw_client_intake
WHERE full_name != TRIM(full_name);
-- Two rows: '  Dmitri Volkov' (leading space) and 'Emeka Chukwu ' (trailing
-- space). Both are safe to fix automatically with TRIM().

-- 6. Referential consistency: advisor_name against the real advisors table
SELECT r.full_name, r.advisor_name
FROM raw_client_intake r
LEFT JOIN advisors a
  ON LOWER(TRIM(r.advisor_name)) = LOWER(a.name)
WHERE a.advisor_id IS NULL;
-- Two rows: Arjun Nair's advisor 'Priya Shaw' is a likely typo for the real
-- advisor 'Priya Shah'. Fiona Sutherland's advisor 'Sam Whitmore' does not
-- match any advisor at all, a fabricated name rather than a typo.

-- 7. Classifying the fix
-- Missing full_name/date_of_birth: needs a human, the applicant must be
--   contacted, there is no safe default to fill in.
-- Exact duplicate: safe to auto-fix, drop the later submission and keep one.
-- Inconsistent casing: safe to auto-fix, normalise with UPPER()/LOWER() or
--   an explicit mapping to the three canonical values.
-- Invalid value ('Moderate'): needs a human, it is not a data-entry slip,
--   someone must decide how to classify or reject the application.
-- Whitespace: safe to auto-fix with TRIM().
-- Referential typo/mismatch: needs a human for a genuine mismatch like
--   'Sam Whitmore', but a close match like 'Priya Shaw' could reasonably be
--   auto-corrected once a fuzzy-match threshold is agreed with the business.

-- Finish-early extension: flag every application with at least one issue
WITH flagged AS (
    SELECT r.intake_id, r.full_name, r.advisor_name,
           CONCAT_WS(', ',
               CASE WHEN r.full_name IS NULL OR r.date_of_birth IS NULL
                    THEN 'missing data' END,
               CASE WHEN EXISTS (
                        SELECT 1 FROM raw_client_intake d
                        WHERE d.full_name = r.full_name
                          AND d.date_of_birth = r.date_of_birth
                          AND d.email = r.email
                          AND d.intake_id != r.intake_id)
                    THEN 'duplicate' END,
               CASE WHEN r.risk_profile IS NOT NULL
                         AND LOWER(r.risk_profile) NOT IN ('cautious', 'balanced', 'adventurous')
                    THEN 'invalid risk_profile' END,
               CASE WHEN r.full_name IS NOT NULL AND r.full_name != TRIM(r.full_name)
                    THEN 'whitespace' END,
               CASE WHEN r.advisor_name IS NOT NULL AND NOT EXISTS (
                        SELECT 1 FROM advisors a
                        WHERE LOWER(TRIM(r.advisor_name)) = LOWER(a.name))
                    THEN 'unknown advisor' END
           ) AS issues
    FROM raw_client_intake r
)
SELECT * FROM flagged WHERE issues != '';
