-- PaySprint Wealth Platform — Raw Client Intake
-- Client applications exactly as they'd arrive from an intake form: unchecked,
-- unvalidated, and not yet trusted enough to load into a real clients table.
-- Used for Module 06's data quality lab.
--
-- Prerequisite: shared/enterprise-schema.sql must already be loaded in the same
-- database. The referential check in this module's lab joins against the
-- `advisors` table it creates.

CREATE TABLE raw_client_intake (
    intake_id       SERIAL PRIMARY KEY,
    full_name       TEXT,
    date_of_birth   DATE,
    email           TEXT,
    risk_profile    TEXT,
    advisor_name    TEXT,
    submitted_date  DATE NOT NULL
);

INSERT INTO raw_client_intake
    (full_name, date_of_birth, email, risk_profile, advisor_name, submitted_date) VALUES
    ('Tomasz Nowak',        '1990-11-02', 'tomasz.nowak@example.com',        'Adventurous',  'Priya Shah',      '2026-01-06'),
    ('Tomasz Nowak',        '1990-11-02', 'tomasz.nowak@example.com',        'Adventurous',  'Priya Shah',      '2026-01-09'),
    -- same person, same details, submitted twice a few days apart
    ('Renata Kowalski',     '1982-05-14', 'renata.kowalski@example.com',     'Balanced',     'Daniel Osei',     '2026-01-07'),
    (NULL,                  '1979-03-08', 'm.santos@example.com',            'Cautious',     'Wei Zhang',       '2026-01-07'),
    -- missing full_name
    ('Aisha Bello',         NULL,         'aisha.bello@example.com',         'Balanced',     'Fatima Al-Rashid','2026-01-08'),
    -- missing date_of_birth
    ('Liam O''Connor',      '1994-08-21', 'liam.oconnor@example.com',        'ADVENTUROUS',  'Daniel Osei',     '2026-01-08'),
    ('Sophie Dubois',       '1987-12-02', 'sophie.dubois@example.com',       'adventurous',  'Priya Shah',      '2026-01-09'),
    ('Kwame Mensah',        '1991-02-27', 'kwame.mensah@example.com',        'balanced',     'Wei Zhang',       '2026-01-09'),
    ('Ingrid Larsen',       '1975-09-17', 'ingrid.larsen@example.com',       'Cautious',     'Fatima Al-Rashid','2026-01-10'),
    ('Rosa Alves',          '1996-01-11', 'rosa.alves@example.com',          'cautious',     'Daniel Osei',     '2026-01-10'),
    ('  Dmitri Volkov',     '1989-07-04', 'dmitri.volkov@example.com',       'Balanced',     'Priya Shah',      '2026-01-10'),
    -- leading whitespace in full_name
    ('Chloe Bennett',       '1993-10-30', 'chloe.bennett@example.com',       'Moderate',     'Wei Zhang',       '2026-01-11'),
    -- 'Moderate' is not a casing variant of a real risk_profile value
    ('Arjun Nair',          '1986-04-19', 'arjun.nair@example.com',          'Balanced',     'Priya Shaw',      '2026-01-11'),
    -- 'Priya Shaw' is a likely typo for the real advisor, 'Priya Shah'
    ('Fiona Sutherland',    '1990-06-25', 'fiona.sutherland@example.com',    'Adventurous',  'Sam Whitmore',    '2026-01-12'),
    -- 'Sam Whitmore' does not match any advisor at all, not just a typo
    ('Hassan Ali',          '1984-11-13', 'hassan.ali@example.com',          'Cautious',     'Daniel Osei',     '2026-01-12'),
    ('Yuki Tanaka',         '1997-03-05', 'yuki.tanaka@example.com',         'Adventurous',  'Fatima Al-Rashid','2026-01-13'),
    ('Emeka Chukwu ',       '1981-08-09', 'emeka.chukwu@example.com',        'Balanced',     'Wei Zhang',       '2026-01-13');
    -- trailing whitespace in full_name
