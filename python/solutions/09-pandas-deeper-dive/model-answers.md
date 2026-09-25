# Module 9 Lab - Model Answer Notes

See `payments_deep_dive.py` for the core solution and `ext1_cumulative_vs_limit.py` to
`ext4_time_between_txns.py` for the extensions.

## Verified results

Output of `python payments_deep_dive.py`:

- Inputs: 140 transactions, 11 customers, 3 FX rates.
- Step 1: 140 rows after the FX merge; total `amount_gbp` (all statuses) 18,084.88.
- Step 2: `_merge` counts `both` 130, `left_only` 10, `right_only` 0. All 10 orphans are K012
  (Lena Fischer), 479.02 GBP. Inner join 130 rows, left join 140 rows.
- Step 3 (all transactions, sorted by `total_gbp`):

  | segment | txn_count | customers | total_gbp | avg_gbp | decline_rate | fraud_count |
  |---|---|---|---|---|---|---|
  | Standard | 66 | 6 | 8,225.31 | 124.63 | 0.152 | 9 |
  | Premium | 43 | 3 | 4,917.86 | 114.37 | 0.047 | 2 |
  | Business | 21 | 2 | 4,462.69 | 212.51 | 0.000 | 1 |
  | Unknown | 10 | 1 | 479.02 | 47.90 | 0.100 | 0 |

- Approved transactions: 127, approved spend 11,471.55 GBP.
- Step 4: channel totals Contactless 774.49, In-store 2,363.26, Online 8,333.80; margin total
  11,471.55, and the check prints `True`. Travel (4,704.40) is entirely Online; Retail
  (1,794.52) and Subscriptions (68.94) are also Online only.
- Step 5: 28 daily rows, 0 days with zero spend. The largest day is 22 Feb (2,730.79). The
  7-day rolling mean on 1 Mar is 568.41. Weekly spend (week ending Sunday): 8 Feb 1,448.98
  (27 approved transactions), 15 Feb 2,323.37 (34), 22 Feb 3,720.33 (30), 1 Mar 3,978.87 (36).
  Highest week ends Sun 01 Mar 2026. Before payday: 4.76 transactions/day (4.32 approved,
  392.84 GBP/day); from payday: 7.00 transactions/day (6.33 approved, 550.16 GBP/day).

## Key points to check in a delegate pair's solution

- **`validate=` is on both merges.** The comment should say that `many_to_one` raises a
  `MergeError` if the right-hand key is duplicated, which would otherwise multiply rows and
  inflate every total without any error.
- **The orphan rows are found with `indicator=True`, not by eye.** A pair that notices K012 only
  because an inner join "lost 10 rows" has the right answer by a weaker route; ask them how they
  would know which rows were lost.
- **The join choice is argued.** Either join can be defended, but the comment must say what is
  gained or lost. The model answer keeps the left join: an inner join silently drops 479.02 GBP of
  genuine transactions and hides a reference-data problem.
- **`customer_name` is dropped from `customers.csv` before the merge.** Otherwise the result
  has `customer_name_x` and `customer_name_y`, and K012's `_y` is NaN.
- **Step 3 is one `.agg` call with named outputs** (`txn_count=("txn_id", "count")` and so on),
  not several `groupby` calls glued together. The decline rate is the mean of a boolean column,
  not a count divided by a count computed separately.
- **Steps 4 and 5 use approved transactions only.** Using all 140 rows gives a margin total of
  18,084.88 instead of 11,471.55, because declined attempts (including the large declined fraud
  attempts) are counted as spend.
- **The margin check is done in code**, with a tolerance (`abs(a - b) < 0.005`) or rounding, not
  `==` on floats.
- **`resample` needs a `DatetimeIndex`.** Delegates who forget `parse_dates` or `set_index` get a
  `TypeError`; this is a useful error to read aloud.
- **Every takeaway cites a number that appears in the pair's output.** "Online dominates" is not
  a takeaway; "Online is 8,333.80 of the 11,471.55 GBP approved spend (72.6%)" is.
- **Pair-work check.** Ask each partner to explain a section the other one typed. If either
  cannot, the driver swaps were not used for their purpose.

## Extension notes

**E1 - Cumulative spend against credit limit.** Month-end usage ranges from K011 at 0.622 of its
3,000 GBP limit down to K001 at 0.037. With a 25% threshold three customers cross: K009 at P0034
(9 Feb, Apple Store, 293.81, cumulative 581.95, 0.388), K011 at P0098 (22 Feb, British Airways,
418.67, cumulative 997.70, 0.333) and K002 at P0119 (26 Feb, Tesco, 70.71, cumulative 650.11,
0.260). K011 carries 1,192.54 GBP of approved fraud; without it K011 would end the month at
22.4%, below the threshold. The common bug is running `cumsum()` without sorting by
`customer_id` and `txn_timestamp` first, which gives a running total in file order. Accept an
inner join here if the comment explains that K012 has no limit to compare against.

**E2 - Melt the pivot back.** Without margins the long form has 24 rows (8 categories x 3
channels), of which 14 are non-zero; the per-channel totals and the overall 11,471.55 match the
source. Melting the version with margins gives 45,886.20, four times the true total, because
the `Total` row and `Total` column are melted as if they were data. Delegates should also notice
that `fill_value=0` created 10 rows for combinations that never happened.

**E3 - Weekly spend per category.** `pd.Grouper(key="txn_timestamp", freq="W-SUN")` inside the
`groupby` gives 28 (week, category) pairs with spend; `unstack(fill_value=0)` turns them into a
4 x 8 table whose row totals match step 5 (1,448.98, 2,323.37, 3,720.33, 3,978.87). Travel is the
largest category in three of the four weeks (Transport leads the week ending 8 Feb) and drives
the large weeks: 2,563.98 in the week ending 22 Feb, which includes the 2,145.31 fraudulent
British Airways booking (P0094), and 1,202.97 in the final week (K007's flight, P0100).
Electronics rises to 1,149.06 in the final week, which includes K011's 780.00 cloned-card
payment (P0136). A delegate who forgets `fill_value=0` in `unstack` gets NaN cells and a row
total that is still correct (`sum` skips NaN), so ask them to check for NaN explicitly.

**E4 - Time between transactions.** After sorting by customer and time, `diff()` leaves 12 NaT
values (one per customer). The six shortest gaps are 15 min (K002 P0011, ASOS, legitimate),
15 min (K009 P0045, Apple Store USD 1,281.98, declined, fraud), 22 min (K009 P0044, Amazon GBP
1.00, fraud), 31 min (K010 P0129), 33 min (K004 P0072) and 43 min (K007 P0109). The K009 burst on
12 Feb is 1.50 at 01:33, 1.00 at 01:55 and the declined 1,281.98 USD attempt at 02:10, all
Online. The point to look for in the comment is that the gap alone does not separate fraud from
normal behaviour (K002's 15-minute gap is legitimate); the combination of a short gap, tiny
amounts, the hour and the channel does. `transactions.csv` is already in timestamp order, so a
delegate who skips the sort gets the same gaps here; ask them what would happen with a file that
is not sorted (`diff` works on row order, so gaps could be negative).
