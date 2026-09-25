# Module 4 Lab - Model Answer Notes

See `fraud_screen.py` for the core solution and `ext1_json_report.py` to
`ext4_threshold_sweep.py` for the extensions. The extensions import their shared functions from
`fraud_screen.py`; `payment_utils.py` is a copy of the Module 2 solution module, used by
Extension 2. Every script runs from any folder and writes into `output/` next to the script.

## Verified results

### `python fraud_screen.py` (shared/transactions.csv, defaults)

- 140 processed, 0 skipped, 33 flagged transactions, 5 velocity customer-days.
- Velocity (>= 3 per customer-day): K002 2026-02-04 (3), K004 2026-02-17 (3), K008 2026-03-01
  (3), K009 2026-02-12 (4), K011 2026-03-01 (3). With `--velocity 4` only K009 remains.
- Evaluation: 12 of 33 flagged transactions are fraud, 21 false alarms, 0 of 12 fraud
  transactions without a flag.

The 12 fraud transactions and the flags that caught them:

| txn_id | customer | GBP | flags |
|---|---|---:|---|
| P0016 | K002 | 1,259.74 | HIGH_VALUE, FOREIGN, NIGHT_ONLINE |
| P0029 | K005 | 701.27 | HIGH_VALUE, FOREIGN, NIGHT_ONLINE |
| P0043 | K009 | 1.50 | NIGHT_ONLINE |
| P0044 | K009 | 1.00 | NIGHT_ONLINE |
| P0045 | K009 | 1,012.76 | HIGH_VALUE, FOREIGN, NIGHT_ONLINE |
| P0054 | K011 | 412.54 | FOREIGN, NIGHT_ONLINE |
| P0076 | K001 | 1,326.74 | HIGH_VALUE, FOREIGN, NIGHT_ONLINE |
| P0088 | K010 | 857.47 | HIGH_VALUE, FOREIGN (23:04, so not NIGHT_ONLINE) |
| P0094 | K006 | 2,145.31 | HIGH_VALUE, FOREIGN, NIGHT_ONLINE |
| P0110 | K002 | 309.02 | FOREIGN, NIGHT_ONLINE |
| P0120 | K005 | 530.83 | HIGH_VALUE, FOREIGN, NIGHT_ONLINE |
| P0136 | K011 | 780.00 | HIGH_VALUE |

The two subtle cases are caught, but each by one rule only. K009's card-testing payments (P0043
GBP 1.50 and P0044 GBP 1.00, domestic, approved) are caught only because they happened at 01:33
and 01:55; the same test at midday would pass every rule. K011's cloned card (P0136, In-store,
14:19, GB) is caught only by HIGH_VALUE, and escapes once the threshold is above GBP 780 (see
Extension 4). The K009 card-testing day is also a VELOCITY customer-day (4 transactions on 12
Feb).

The 21 false alarms fall into three groups:

- **K012 Lena Fischer, UNKNOWN_CUSTOMER (10):** P0042, P0060, P0062, P0077, P0083, P0099, P0118,
  P0121, P0130, P0138. These are a reference-data gap, not a fraud signal.
- **K004 Daniel Price's holiday in Spain, FOREIGN (7):** P0057 (Airbnb, GBP 652.38, also
  HIGH_VALUE), P0061, P0064, P0068, P0075, P0079, P0082.
- **K007 George Mensah's US business trip, FOREIGN (4):** P0100 (British Airways, GBP 1,202.97,
  also HIGH_VALUE), P0103, P0109, P0111.

K003 (home FR) and K008 (home IE) spend in EUR in their home countries and are not flagged,
because FOREIGN compares with `home_country`.

### `python fraud_screen.py --input ../../shared/messy-transactions-raw.csv`

- 120 processed, 23 skipped, 31 flagged, 3 velocity customer-days (K004 17 Feb, K009 12 Feb with
  3, K011 1 Mar).
- Skipped for a bad amount (14): P0013 `£123.09`, P0016 `$1,594.61`, P0020, P0026, P0041,
  P0045, P0057 (blank), P0076, P0086 `TBC`, P0088, P0091, P0094, P0100, P0112.
- Skipped for a bad timestamp (9): P0011, P0047, P0068, P0087, P0106, P0115, P0124, P0135 (all
  `DD-Mon-YYYY HH:MM`) and P0131 `2026-02-29 09:35` (2026 is not a leap year, so `strptime`
  rejects it).
- Evaluation: 7 of 31 flagged are fraud, 24 false alarms, 0 of 7 fraud without a flag.

Three findings to draw out:

- **Skipping hides fraud.** Five of the 12 fraud transactions (P0016, P0045, P0076, P0088,
  P0094) are skipped because their amounts carry a currency symbol, so "0 fraud missed" is only
  true of the rows the tool read. The skipped-row list belongs in the report for this reason.
- **`UK` is not `GB`.** Five domestic transactions from known customers are flagged FOREIGN
  because the raw file uses `UK`: P0024, P0030, P0058, P0089, P0114 (the other two `UK` rows
  belong to K012, which already gets UNKNOWN_CUSTOMER).
- **P0141** (Pret A Manger, Contactless, GBP 1,850.00) is flagged HIGH_VALUE. It is not fraud
  (`is_fraud` 0); it is almost certainly a keying error for GBP 18.50. The duplicate rows
  (P0095 twice, P0102 twice) are processed twice; neither is flagged, and the brief does not ask
  for de-duplication. The channel spelling variants (`online`, `ONLINE`, ...) do not change any
  result here because none of them falls between 00:00 and 04:59, but `channel == "Online"` would
  miss them if one did.

## Key points to check in a delegate's solution

- **`float()` and `strptime` happen inside the `try`, before the row is kept.** Appending the raw
  row and converting later either crashes in a rule function or lets unconverted strings through.
- **Comparisons use `amount_gbp`, not `amount`.** Comparing the raw amount with 500 judges
  USD 1,594.61 and EUR 767.51 at face value, as if they were pounds. If the amount was never
  converted at all, `"1594.61" > 500` raises `TypeError`.
- **FOREIGN uses `customers.get(customer_id)`.** `customers[customer_id]` raises
  `KeyError: 'K012'` on P0042. A solution that compares `country != "GB"` flags all 4 of K003's
  French transactions and all 4 of K008's Irish ones: ask the delegate to explain K003.
- **The night window is `0 <= hour < 5`.** `hour <= 5` includes 05:00-05:59. P0088 at 23:04 is
  a good test of whether the delegate has checked the window rather than guessed.
- **VELOCITY is keyed by `(customer_id, date)`**, a tuple, and uses `ts.date()`, not the
  timestamp string. Keying by customer only counts the whole month (every customer passes 3).
  Keying by `txn_timestamp[:10]` works on the clean file but is fragile. VELOCITY is reported
  once per customer-day, not once per transaction.
- **One function writes and prints the report.** Two separate blocks of `print` and `f.write`
  calls drift apart as soon as one is edited.
- **`argparse` types.** Without `type=float`, `--high-value 750` arrives as the string `"750"`
  and the comparison raises `TypeError`. Default paths are built from `Path(__file__)`, so
  `python fraud_screen.py` works from any folder.
- **Warnings name the `txn_id` and the reason.** "Skipping bad row" with no identifier cannot be
  followed up.
- **The evaluation is built with sets.** `flagged & fraud`, `flagged - fraud` and
  `fraud - flagged` are the three quantities; a delegate who counts with nested loops should see
  the Module 3 set operations again.
- **Reading back the evaluation.** 21 of 33 flags are false alarms, and 10 of those come from one
  missing customer record. A delegate who reports "the rules catch all the fraud" without
  mentioning the false alarms, or the fraud hidden in skipped rows on the messy file, has not
  finished the analysis.

## Extension notes

**E1 - JSON report.** `python ext1_json_report.py --format json` writes
`output/fraud_report.json` (140 processed, 33 flagged, 5 velocity customer-days) and reads it
back. The first flagged entry is
`{'txn_id': 'P0016', 'customer_id': 'K002', 'timestamp': '2026-02-06T02:45', 'merchant':
'Apple Store', 'amount_gbp': 1259.74, 'flags': ['HIGH_VALUE', 'FOREIGN', 'NIGHT_ONLINE']}`.
The two traps are the ones the brief mentions: `json.dump` raises
`TypeError: Object of type datetime is not JSON serializable`, so timestamps must become ISO
(International Organization for Standardization) 8601 strings with `.isoformat()`; and a dict
with tuple keys raises `TypeError: keys must be str, int, float, bool or None, not tuple`, so the velocity
customer-days become a list of objects. Look for a solution that builds one report structure and
renders it as text or JSON, rather than two separate reporting paths that can disagree.

**E2 - Tolerant parsing.** On the messy file the core parser skips 23 rows and the tolerant one
skips 3 (20 fewer): P0057 (blank amount), P0086 (`TBC`) and P0131 (`2026-02-29`, which no
format can parse). With 140 rows processed, the evaluation becomes 12 of 38 flagged are fraud,
26 false alarms, 0 of 12 fraud missed, and all 5 velocity customer-days from the clean file
return. The 38 flags are the clean run's 33, minus P0057 (still skipped), plus the five `UK`
false alarms and P0141. Parsing more rows exposes the next data-quality problem (`UK` versus
`GB`) rather than solving everything; Module 6 cleans these systematically. `parse_amount`
raises `ValueError` for `TBC` and `InvalidAmountError` (a `PaymentError`, not a `ValueError`)
for zero or negative amounts, so the `except` must name both. The messy file has no negative
amounts, so a solution that catches only `ValueError` passes on this data and would crash on
the first negative amount in another file.

**E3 - Risk score.** With `--min-score 2`, 15 of 140 transactions are listed. P0045 scores 4
(the only transaction with every rule, VELOCITY included); P0094, P0076, P0016, P0029 and P0120
score 3. Score distribution: score 4: 1 transaction (1 fraud); 3: 5 (5 fraud); 2: 9 (6 fraud);
1: 29 (0 fraud); 0: 96 (0 fraud). A minimum score of 2 keeps all 12 fraud transactions and only
3 false alarms (P0100, P0057, P0075), against 21 for "any flag". Every UNKNOWN_CUSTOMER row
scores 1, which is why the score removes those alarms. The ranking uses a tuple key,
`key=lambda s: (-s[0], -s[1]["amount_gbp"])`; a delegate who sorts twice should know that
Python's sort is stable, so sorting by amount first and then by score also works.

**E4 - Threshold sweep.** HIGH_VALUE on its own:

| threshold | flagged | caught | false alarms | missed |
|---:|---:|---:|---:|---|
| 250 | 15 | 10 | 5 | 2 (P0043, P0044) |
| 500 | 10 | 8 | 2 | 4 (+ P0054, P0110) |
| 750 | 7 | 6 | 1 | 6 (+ P0029, P0120) |
| 1,000 | 5 | 4 | 1 | 8 (+ P0088, P0136) |

All transaction rules together: 250 gives 36 flagged, 12 caught, 24 false alarms, 0 missed; 500
and 750 give 33, 12, 21, 0; 1,000 gives 32, 11, 21, and misses P0136. Raising the threshold
trades false alarms for missed fraud, and the other rules make the combined result much less
sensitive to the threshold than HIGH_VALUE alone. P0136 (K011's cloned card) is the only fraud
that depends on HIGH_VALUE alone. The card-testing payments P0043 and P0044 can never be caught
by an amount threshold. In Module 13 terms, caught / flagged is precision and caught / (caught +
missed) is recall.
