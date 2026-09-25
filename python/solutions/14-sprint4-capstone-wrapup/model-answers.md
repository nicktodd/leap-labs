# Module 14 Lab - Model Answer Notes

See `payments_dashboard.py` for the core solution, `stakeholder-explanation.md` for a model team
explanation, and `ext1_api_source.py`, `ext2_markdown_report.py`, `ext3_fraud_rules_panel.py`
and `ext4_customer_statements.py` for the extensions. The extension scripts import the core
functions from `payments_dashboard.py`. This is a capstone, so teams will choose different
insights and charts: the numbers below are for checking the parts every team must get right
(the cleaning and the definitions), not a required answer set.

## Verified results

Output of `python payments_dashboard.py`:

- Pipeline: 143 rows received, 5 rejected, 138 loaded. Rejected: P0095 and P0102 (duplicate
  row), P0057 and P0086 (amount missing or not a number), P0131 (impossible date). Held for
  review, not in spend figures: P0141.
- Repairs, counted on the rows received: merchant whitespace trimmed 6; channel spellings
  standardised 15; `UK` changed to `GB` 7; amount symbols/separators removed 12; timestamps in
  `DD-Mon-YYYY` format 9; missing categories filled from the merchant 3. (The whitespace and
  channel counts include the second copy of P0102, which is later removed as a duplicate.)
- `validate()` returns `[]` for the cleaned data. Removing `USD` from the FX rates stops the run
  with `8 rows with no amount_gbp` and `currency with no FX rate`; appending two copied rows and
  setting one country to `UK` returns `duplicate txn_id: ['P0001', 'P0002']` and
  `unexpected country values: ['UK']`.
- Customer spend (approved, not confirmed fraud, not held for review): GBP 7,295.33 across 119
  transactions.
- Insight 1: Travel is the largest category, GBP 1,906.71 (26.1% of customer spend), then Retail
  GBP 1,250.98. Subscriptions is the smallest at GBP 68.94.
- Insight 2: Online payments are declined 15.9% of the time (11 of 69), against 2.9% for
  in-store and contactless combined (2 of 69). By channel: Online 15.9%, In-store 4.3%,
  Contactless 2.2%.
- Insight 3: 12 confirmed fraud transactions worth GBP 9,338.18. Declines stopped 7 of them
  (GBP 5,997.83, 64% of the fraud value); 5 were approved, costing GBP 3,340.35. A further 6
  declines were genuine customers.
- Insight 4: from payday (Fri 27 Feb) there were 5.7 approved customer transactions a day,
  against 4.1 before it; spend per day was GBP 271.83 against GBP 259.19. The transaction count
  rises clearly; the spend per day barely moves, so a team should present the count, not the
  value, as the payday finding.
- Outputs in `output/`: `dashboard_data.csv`, `chart_spend_by_category.png` (horizontal bars,
  sorted, from zero, value labels), `chart_decline_rate_by_channel.png` (0-100% axis),
  `chart_daily_transactions.png` (payday period shaded).

## Key points to check in a delegate's solution

- **Normalisation before de-duplication.** A pipeline that drops exact duplicates first finds
  only P0095, loads 139 rows, and double-counts P0102 (EUR 83.77 at Amazon). De-duplicating on
  `txn_id` also works, but the delegate should be able to say why whole-row de-duplication
  needs the text cleaned first.
- **P0131 is rejected, not repaired.** `2026-02-29` must not be replaced with 28 Feb or 1 Mar:
  either would be a guess. Parsing each format explicitly with `errors="coerce"` leaves it as
  `NaT`, which is then rejected with a reason.
- **P0141 is kept but held for review.** Deleting it hides a data problem from the people who
  can fix it; including it adds GBP 1,850.00 to customer spend and nearly quadruples Dining
  (GBP 657.81 without it). A team that includes it should say so on the dashboard.
- **Amounts are added in GBP.** Adding `amount` across the 138 loaded rows gives 21,661.64,
  against GBP 19,099.01 after conversion: mixing currencies overstates the total by
  GBP 2,562.63.
- **The validation gate stops the run.** `validate()` returns a list and the script exits with
  every failure listed, before `load()`. Printing a warning and carrying on is not a gate. Ask
  the team to show you the gate failing (for example, with a currency removed from the rates).
- **"Customer spend" is defined and written down.** Declined payments and confirmed fraud are
  the usual exclusions. Different definitions are acceptable if they are stated on the
  dashboard; an undefined total is not.
- **Insights cite specific numbers**, not generalities: "Online payments are declined 15.9% of
  the time (11 of 69)" beats "Online payments are declined more often".
- **Charts follow Module 10's honest-axis rule** even under capstone time pressure: bars start at
  zero and a rate is plotted on a 0-100% axis. A truncated decline-rate axis would make 2.2% and
  15.9% look like a far larger gap.
- **The data-quality line is on the dashboard**, with rejected `txn_id`s and reasons. A reader
  who sees 138 loaded rows and no explanation cannot reconcile it with the 143 in the export.
- **The stakeholder explanation avoids jargon entirely**: no "ETL", no "DataFrame", no "NaT",
  no unexplained acronyms. If a team's explanation only makes sense to someone who took this
  course, it has not been written for the audience it claims.
- **Every team member can present at least one insight unprompted.** This is the single most
  important item on the list, the same emphasis as every earlier week's capstone module.

## Common gaps and quick fixes

| Gap | Likely cause | Quick fix |
|---|---|---|
| 139 rows loaded, P0102 counted twice | Duplicates removed before normalising text | Move the duplicate check after the text clean-up, or de-duplicate on `txn_id` |
| Totals far too high | Raw `amount` summed across currencies, or P0141 included | Sum `amount_gbp`; exclude rows held for review from spend |
| Insight has no specific number | Rushed, or copied a Module 7/9 observation without re-deriving it | Re-run the groupby and cite the figure from this data |
| Bar chart axis does not start at 0 | Module 10's rule forgotten under time pressure | `ax.set_ylim(bottom=0)` (or `set_xlim(left=0)` for horizontal bars) |
| `validate()` prints but the dashboard is still produced | Checks written as warnings, not as a gate | Return a list of failures and `raise SystemExit` if it is not empty |
| Stakeholder explanation uses "ETL" or "DataFrame" unexplained | Written by whoever built the pipeline, for an audience like themselves | Have a teammate who did not write the code read it back and flag anything unclear |
| Only one team member can present | Work was not shared; one person built the whole thing | Spend the remaining time walking every insight through as a team |

## Running the session

Fifteen to twenty minutes for the build, ten minutes to rehearse the stakeholder presentation in
pairs. Teams that split the functions should agree the definition of customer spend first,
otherwise the insights and the charts disagree. Circulate and specifically check: can this team
member explain a chart they did not personally build, and can they say why 5 rows were rejected?

## Extension notes

**Extension 1 (switchable source).** Verified with the lab API running on port 5051:
`--source api` fetches 140 rows in 3 pages (`limit=50`), with 0 rate-limit waits on a fresh
server, and reports 140 received, 0 rejected, 140 loaded, nothing held for review and no
repairs. Customer spend is GBP 8,131.20 across 122 transactions, and Travel is GBP 2,559.09
(31.5%). The dashboards differ because the API serves the clean dataset: it contains P0057,
P0086 and P0131 (which the raw export could not supply usable values for) and does not contain
P0141 (the keying error). `--source file` reproduces the core output. Good answers change only
the extract stage and convert the API rows to the raw file's shape (`[RAW_COLUMNS].astype(str)`),
because the JSON keys arrive in alphabetical order and numbers arrive as numbers. The
solution writes API-mode charts to `output/api/` so the two runs can be compared. Common
pitfalls: a second copy of `transform()` for API data, and reading `next_cursor` from a `429`
response body.

**Extension 2 (Markdown report).** Verified: `output/dashboard.md` is 38 lines, embeds the 3
charts with relative links (`![...](chart_spend_by_category.png)`), and includes the category
table (Travel 26.1% down to Subscriptions 0.9%) and the data-quality lines. The solution
reuses `dashboard_lines()` from the core script, so the console and Markdown wording cannot
drift apart. Common pitfalls: absolute image paths that break when the folder is shared, and
insight text written a second time by hand, which goes out of date on the next data change.

**Extension 3 (fraud-rules panel).** Verified on the 138 cleaned rows (12 confirmed fraud):

| Rule | Flagged | Fraud caught | False alarms |
|---|---:|---:|---:|
| HIGH_VALUE | 10 | 8 | 2 |
| FOREIGN | 19 | 9 | 10 |
| UNKNOWN_CUSTOMER | 10 | 0 | 10 |
| NIGHT_ONLINE | 10 | 10 | 0 |
| VELOCITY | 16 | 4 | 12 |
| Any rule | 44 | 12 | 32 |

Precision of "any rule" is 27.3% and recall 100.0%: no fraud escapes every rule on this data.
K009's card-testing payments (P0043, P0044) are caught by NIGHT_ONLINE and VELOCITY, and K011's
cloned-card payment (P0136, GBP 780.00) by HIGH_VALUE and VELOCITY. NIGHT_ONLINE is the
strongest single rule (10 of 12, no false alarms); it misses P0088 (Online at 23:04) and P0136
(In-store). The
FOREIGN false alarms are K004 in Spain (6) and K007 in the US (4), the holiday and business
trip; K003 and K008 are not flagged because their home countries (FR, IE) come from
`customers.csv`. The HIGH_VALUE false alarms are P0100 (K007's British Airways flight) and P0141
(the held keying error). All 10 of K012's transactions are flagged only by UNKNOWN_CUSTOMER,
which is a reference-data problem rather than a fraud signal; good answers point this out.
Common pitfalls: an inner merge with `customers.csv`, which silently drops K012's 10 rows, and
counting VELOCITY per transaction without saying so.

**Extension 4 (customer statements).** Verified: the top 3 customers by spend are George Mensah
(K007, Business) GBP 1,830.65 over 10 transactions, 25.1% of customer spend, 9.2% of a
GBP 20,000 limit; Daniel Price (K004, Premium) GBP 1,222.00 over 17 transactions, 16.8%, 12.2%
of GBP 10,000; Ibrahim Yusuf (K009, Standard) GBP 691.05 over 11 transactions, 9.5%, 46.1% of
GBP 1,500. Together they account for 51.3% of customer spend across 12 customers. K012 Lena
Fischer ranks 10th (GBP 267.02) and is reported as having no customer record. Check that the
join is a left join (`how="left"`) and that the share of limit is `NaN` for K012 rather than a
crash or a division by zero. Good answers notice that K009's 46.1% is the highest share of limit
among the top 3 despite the lowest spend, because of the small limit. Common pitfall: an inner
join, which drops K012 and so changes the 12-customer denominator.
