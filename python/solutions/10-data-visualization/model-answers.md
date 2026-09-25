# Module 10 Lab - Model Answer Notes

See `visualise_payments.py` for the core solution and `ext1_heatmap.py` to
`ext4_annotate_payday.py` for the extensions. All PNG files are written to `output/` next to the
script; each one was opened and checked visually.

## Verified results

Output of `python visualise_payments.py` (five PNG files):

- `category_spend.png`: horizontal bars, Electronics at the top with £6,681 (6,680.95), then
  Travel £4,704, Retail £2,942, Groceries £1,337, Transport £1,316, Dining £658, Fuel £378,
  Subscriptions £69. The x-axis starts at £0.
- `amount_distribution.png`: with 30 linear bins, 98 of 140 payments fall in the first bin and
  the rest of the axis is almost empty. The log panel (25 bins from `np.geomspace`) shows the
  spread from £1 to about £2,145: 120 of the 140 payments lie between £3 and £200, with a thin
  tail of large payments.
- `daily_spend.png`: 28 daily points; the highest day is Sun 22 Feb at £2,730.79. The 7-day
  rolling mean starts on 8 Feb (the first 6 values are NaN) and smooths the spikes.
- `decline_rate_by_channel.png`: Online 15.5% (11 of 71), In-store 4.2% (1 of 24), Contactless
  2.2% (1 of 45), on a 0-100% axis.
- `misleading.png`: raw `amount` by country, labelled "Total spend (GBP)". What the chart shows
  against the true GBP totals: US 9,162.52 vs 7,238.39 (overstated by 1,924.13); GB 6,575.97
  both (0.00); FR 1,276.51 vs 1,085.03; NL 1,188.57 vs 1,010.29; DE 1,109.85 vs 943.37; ES
  1,046.60 vs 889.61; IE 402.62 vs 342.22. The ranking does not change, but the US lead over
  GB appears as 2,586.55 when it is 662.42, so the chart makes US spend look like a much larger
  share of the business than it is.

## Key points to check in a delegate's solution

- **Chart type matches the question.** Horizontal bars for a ranked comparison of named
  categories, a histogram for a distribution, a line for a daily time series, bars for rates by
  group. A line chart across categories, or a bar per transaction, should be corrected.
- **Bars start at zero.** For the horizontal bar the x-axis starts at 0 (`set_xlim(0, ...)`);
  for the decline rate the axis runs from 0% to 100%. Check the code, not only whether the
  chart happens to look right.
- **The decline-rate labels include the counts.** "4.2%" alone invites the reader to compare it
  with Contactless's 2.2%; "(1 of 24)" against "(1 of 45)" shows that each rate rests on a
  single decline.
- **The log histogram uses log-spaced bins.** Setting `set_xscale("log")` on a histogram with
  linear bins gives bars of very different widths, crammed at the right. `np.geomspace` gives
  bins of equal width on the log axis. The titles should say which panel is which scale.
- **The rolling mean is on the same axes as the daily line, with a legend**, and the delegate
  can explain why the first 6 days have no rolling value.
- **Titles state a finding**, for example "Online payments are declined far more often than
  card-present ones", not "Decline rate chart".
- **`plt.close(fig)` after saving.** Without it, figures accumulate in memory; matplotlib warns
  when more than 20 are open, which happens quickly in loops.
- **The misleading chart's comment names the mechanism**, for example "sums `amount` across
  GBP, EUR and USD and labels the result GBP; US is overstated by about 27% (1 / 0.79) and
  euro countries by about 18% (1 / 0.85)". "This chart is misleading" alone does not meet the
  bar. For the pie option, the flaw is that 8 slices with several small, similar shares
  (Fuel 2.1%, Subscriptions 0.4%, Dining 3.6%) cannot be compared by angle. For the dual-axis
  option, the flaw is that the two scales are chosen independently, so any apparent link
  between the lines is an artefact of the scaling.
- **Totals include declined transactions.** The core charts sum all 140 rows, so category
  "spend" includes declined attempts (Electronics includes 5 declined payments at Apple Store and
  Currys). A delegate who filters to APPROVED gets different, also valid, totals; the
  title or label should say which was used. This is a good critique point.
- **`critique.md` refers to the partner's actual charts** (a title, an axis, a number). A
  critique that would apply unchanged to any chart has not looked at the partner's work.

## Extension notes

**E1 - Heatmap.** Counts by weekday x hour band: Monday 1/6/5/8, Tuesday 0/4/7/9, Wednesday
2/4/7/5, Thursday 3/3/5/8, Friday 2/3/8/6, Saturday 1/12/4/4, Sunday 1/6/8/8 (Night / Morning
/ Afternoon / Evening). The busiest cell is Saturday Morning with 12. Pitfalls: weekdays in
alphabetical order (use `reindex` with an explicit list), a rainbow colour map such as `jet`
(use one hue, light to dark, with `vmin=0`), and black text that disappears on the darkest
cells (switch the text colour above a threshold). `ax.set_xticks(positions, labels=...)` is
needed because `imshow` has no idea of category names.

**E2 - Fraud scatter.** Legitimate (128) as circles, confirmed fraud (12) as larger X markers in
a second colour, so the groups are distinguishable without colour. The trap: two rows have a
distance of 0 km, P0043 and P0044, and both are K009's card-testing fraud. On a plain log
x-axis matplotlib drops them without any warning, so the chart would hide exactly the fraud
that distance rules miss. The solution uses `ax.set_xscale("symlog", linthresh=1)`, which is
linear from 0 to 1 km and logarithmic above; plotting `distance + 1` with a note on the label
is also acceptable. The annotations point at K004 (7 legitimate rows beyond 300 km, median
1,758.3 km, Spain) and K007 (4 rows, median 5,581.4 km, US): legitimate clusters sitting next to
the far-from-home fraud, which is the false-positive problem for a distance rule.

**E3 - Dashboard.** `style_axes` sets the title (left-aligned), axis labels, removes the top and
right spines, and draws a light grid on the value axis only, behind the data
(`set_axisbelow(True)`). The key design change is that each panel function takes an `ax`
argument instead of calling `plt.subplots` itself; that is what makes it reusable in a grid.
The solution's panels: category spend, daily spend with rolling mean, decline rate by channel,
and transactions by hour (with integer y ticks via `MaxNLocator(integer=True)`). The overall
title states that all amounts are in GBP. Check for overlapping tick labels (dates need
rotation) and that `fig.tight_layout()` is called after `suptitle`.

**E4 - Payday annotation.** The payday effect is in the number of transactions, not in spend:
4.76 transactions a day on average before Fri 27 Feb (25 days) against 7.00 from 27 Feb (3
days: 7, 6 and 8). Daily spend does not show it because it is dominated by single large
payments: the highest-spend day, Sun 22 Feb (£2,730.79), is mostly one fraudulent payment,
P0094 at £2,145.31. The solution uses two panels sharing the date axis (`sharex=True`) rather
than a second y-axis, annotates P0094 on the spend panel and the payday bump on the count
panel, and shades 27 Feb onwards with `axvspan`. Good answers take the annotation numbers from
the data (f-strings) rather than typing them in, and note that 3 days is a short window for a
firm conclusion.
