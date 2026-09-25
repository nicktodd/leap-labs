# Module 6 Lab - Model Answer Notes

See `clean_transactions.py`. It writes the cleaned table to `output/clean_transactions.csv`.
Verified output against `shared/messy-transactions-raw.csv`:

- **Quantify:** 143 raw rows; nulls in `merchant_category` (3) and `amount` (1, the blank; `TBC`
  is text, so it is not a null yet); 9 distinct raw channel values (`'Online'`, `'Contactless'`,
  `'In-store'`, `'contactless'`, `'online'`, `' Contactless'`, `'Online '`, `'ONLINE'`,
  `'instore'`); 1 exact duplicate row. `amount` is read as `str` because of the symbols and `TBC`.
- **Amounts:** 2 rows cannot be parsed: P0057 (blank) and P0086 (`TBC`). Dropped.
- **Channel:** exactly `Contactless`, `In-store`, `Online` after the mapping.
- **Country:** `UK` replaced on 7 rows; countries are DE, ES, FR, GB, IE, NL, US.
- **Merchant:** 6 padded names stripped (5 distinct transactions plus the duplicate copy of
  P0102).
- **Category:** every merchant has exactly one category; filled P0015 (Pret A Manger -> Dining),
  P0107 (TfL -> Transport), P0132 (Amazon -> Retail).
- **Timestamps:** 131 rows in `YYYY-MM-DD HH:MM`, 9 in `DD-Mon-YYYY HH:MM`, 1 matching neither:
  P0131 `2026-02-29 09:35`. Rejected.
- **Duplicates:** 2 exact duplicates after normalisation (P0095, P0102), against 1 in the raw
  file. Deduplicated on `txn_id`.
- **Outlier:** the per-category IQR rule flags 15 rows, the contactless-limit rule flags 1, and
  only P0141 (Pret A Manger, Contactless, 1,850.00 GBP) breaks both. It stays in the data.
- **Final:** 138 rows. As a cross-check, the 137 rows other than P0141 match
  `shared/transactions.csv` in every column except the timestamp display format.

Key points to check in a delegate's solution:

- **The order of the steps.** Merchant whitespace must be stripped before the category lookup
  (otherwise `" Amazon"` is a separate key), and deduplication must run after normalisation. A
  delegate who calls `drop_duplicates()` first removes only P0095 and ends with 139 rows.
- **The reason for dropping P0057 and P0086.** The strong answer notes there is no other column
  to derive an amount from (unlike `quantity * price` in the demo), and that filling with 0 or the
  mean would silently change totals. Filling them is a fail.
- **An explicit channel mapping, with an assertion.** `.str.strip().str.title()` produces
  `In-Store` and leaves `instore` separate. A mapping that turns unknown variants into NaN, plus
  an `assert`, protects next month's run.
- **The category fill is verified, not assumed.** Look for a `nunique()` check (or equivalent)
  before the fill, and a comment that the fill would be unsafe if a merchant had more than one
  category (for example a supermarket selling fuel).
- **No guessed dates.** `format="mixed"` also parses the valid rows, but without
  `errors="coerce"` it raises `DateParseError` ("day is out of range for month") on P0131; with
  it, P0131 becomes NaT. A delegate
  who "fixes" it to 28 Feb or 1 Mar has invented data. Parsing both formats explicitly is
  preferred because it documents exactly which formats are accepted.
- **Outliers flagged, not removed, and in GBP.** An IQR rule on the raw `amount` column mixes EUR,
  USD and GBP. The investigation note should name a source of truth (the acquirer's settlement
  record or the merchant's till receipt), not only "check with someone".
- **The IQR rule is treated as a candidate list.** The per-category rule also flags Dishoom meals
  and Trainline fares; a good comment explains why those are not errors.

## Extension notes

**E1 before/after report** (`ext1_quality_report.py`, writes `output/quality_report.csv`). Rows
143 -> 138, `merchant_category` nulls 3 -> 0, `amount` nulls 1 -> 0, distinct channel values
9 -> 3, distinct country values 8 -> 7, exact duplicate rows 1 -> 0, duplicate `txn_id`s 2 -> 0.
Good answers explain each change by a step. Pitfall: the `amount` null count before cleaning is 1,
not 2, because `TBC` is text until it is coerced; a delegate who reports 2 has profiled after
step 2.

**E2 `.pipe()` pipeline** (`ext2_pipe_functions.py`). Ten small functions, each using `.assign()`
or a boolean filter so the input is never modified. `clean(raw)` returns 138 rows and flags only
P0141 as `needs_review`. Removing exact duplicates first, on raw data, leaves 139 rows with P0102
twice. Pitfall: functions that modify their argument in place (`df["x"] = ...; return df`) change the
caller's DataFrame too, so a step can no longer be rerun or tested on its own input.

**E3 quarantine** (`ext3_quarantine.py`, writes `output/rejected_rows.csv`). Five rejected rows:
P0057 blank amount, P0086 non-numeric amount (`TBC`), P0095 duplicate, P0102 duplicate, P0131
invalid date. The reconciliation `143 = 138 + 5` holds and the clean and rejected index sets are
disjoint. The rejected file keeps the raw values (P0102's second copy still shows `" Amazon"` and
`ONLINE`) so the source team can see what arrived. Pitfall: giving a row two reasons, which
breaks the reconciliation.

**E4 global versus per-category rules** (`ext4_global_vs_segment_outliers.py`). The global fence
is 206.44 GBP and flags 16 rows, including 4 legitimate Travel/Electronics purchases (P0034 Apple
Store 293.81, P0098 British Airways 418.67, P0100 British Airways 1,202.97, P0108 Currys 369.06);
none of these is flagged by the per-category rule (Electronics fence 1,978.31, Travel 2,759.85).
The per-category rule flags 15 rows, concentrated in Dining (6) and Transport (6), where cheap and
expensive merchants share a category. Both rules flag P0141. What good looks like: the delegate
concludes that thresholds should reflect what is normal for the segment, and notes that category
is still a coarse segment (merchant-level baselines or business rules such as the contactless
limit are the next refinement).
