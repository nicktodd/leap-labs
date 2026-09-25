# Module 10 Lab - Data Visualization Principles & Practice

## Scenario

The PaySprint card-payments team presents a monthly review to people who will not read a table
of numbers. They have asked for a small set of charts from February's card transactions: where
the money goes, what a typical payment looks like, how spend moves day to day, and which
channels are declined. Each chart must be honest enough to be shown without a spoken
explanation. You will also build one chart that misleads on purpose, and critique a partner's
charts.

## Objectives

By the end of this lab you will have:

- Chosen the chart type for each question, including a horizontal bar for long category names
  and a histogram for a distribution
- Used a log scale to show a skewed distribution, and explained what it reveals
- Plotted a time series with a rolling mean and a legend
- Formatted axes for money and percentages, and labelled bars with values and counts
- Built a chart that misleads without a truncated axis, and named its flaw
- Peer-critiqued a partner's charts against a specific checklist

## Setup

- `pip install pandas numpy matplotlib`
- Data: `shared/transactions.csv` and `shared/fx_rates.csv` (in the repo's `shared/` folder)
- Starter file: `starter_visualise_payments.py`, in `labs/10-data-visualization/`. It loads the
  data, adds `amount_gbp` and provides a `save(fig, name)` helper that writes PNG files to an
  `output/` folder next to the script. Run it with `python starter_visualise_payments.py` from
  any folder.
- Pair up with a partner for the critique step.

## The data

`transactions.csv` has 140 card transactions from Mon 2 Feb to Sun 1 Mar 2026. The columns used
here: `txn_timestamp`, `merchant_category` (8 categories), `channel` (`Online`, `In-store`,
`Contactless`), `country` (a two-letter ISO, International Organization for Standardization,
country code), `currency` and `amount` (the amount is in this currency: GBP (pounds sterling),
EUR (euro) or USD (US dollar)), `status` (`APPROVED` / `DECLINED`), `distance_from_home_km`
and `is_fraud`.

The starter adds `amount_gbp` (the amount in GBP) using `fx_rates.csv` (FX, foreign
exchange): GBP 1.00, EUR 0.85, USD 0.79. Totals in this lab cover all 140
transactions, declined ones included; say so in a title or label where it matters.

## Task

Each chart goes in its own function in the starter and is saved to `output/` as a PNG (Portable
Network Graphics) file. Every chart needs a
title that states what the chart shows or finds (not "Chart 1"), and axis labels with units.

1. **Spend by category** (`category_spend.png`). A horizontal bar chart of total `amount_gbp` by
   `merchant_category`, sorted with the largest at the top. Put the value on each bar with
   `ax.bar_label`, format the axis as pounds, and start the x-axis at 0. The demo used vertical
   bars; horizontal bars suit long category names and ranked lists.
2. **Distribution of payment amounts** (`amount_distribution.png`). One figure with two panels
   (`plt.subplots(1, 2)`): a histogram of `amount_gbp` with a linear x-axis, and the same data
   with log-spaced bins (`np.geomspace(min, max, 25)`) on a log x-axis (`ax.set_xscale("log")`).
   Each panel's title says what that panel shows. Print how many of the 140 payments fall in
   the first bin of the linear histogram.
3. **Daily spend** (`daily_spend.png`). A line chart of daily `amount_gbp` (`resample("D")`)
   with a 7-day rolling mean (`.rolling(7).mean()`) on the same axes, a legend, a y-axis from 0
   and readable dates. Print the highest-spend day.
4. **Decline rate by channel** (`decline_rate_by_channel.png`). A bar chart of the decline rate
   per channel on a 0-100% axis (`ax.set_ylim(0, 1)` with `PercentFormatter(xmax=1)`). Each bar
   label shows the rate and the counts behind it, for example `15.5%` and `(11 of 71)`.
5. **A misleading chart** (`misleading.png`). Build one chart that misleads **without** a
   truncated axis (the demo covered that). Choose one:
   - a bar chart of the raw `amount` summed by `country` with a y-axis labelled "GBP", which
     silently adds euros and dollars as if they were pounds (print the true GBP totals next to
     what the chart shows)
   - a pie chart of spend across the 8 merchant categories
   - a chart with two unrelated y-axes (`ax.twinx()`), for example daily spend and daily
     decline rate, scaled so that the lines appear to move together

   Add a comment or docstring that names the specific flaw and how a reader would be misled.

## Peer critique

Swap charts with your partner (the PNG files, not the code) and, for each of their five charts,
answer against this checklist:

1. Does the chart type match the question being asked?
2. Does the axis represent magnitude truthfully (and, for the misleading chart, what is the
   dishonest part)?
3. Are the title and axis labels specific, with units, not generic?
4. Would someone unfamiliar with the dataset draw the correct conclusion from this chart alone?

Write your critique of your partner's charts as a short markdown file, `critique.md`, in your own
lab folder: one short paragraph per chart. Do not put it in `output/`.

## Acceptance criteria

- The script runs with `python starter_visualise_payments.py` from any folder with no errors or
  warnings, and writes five PNG files to `output/`. Open each one and check it.
- Chart 1: Electronics is the top bar with £6,681 (6,680.95), Subscriptions the bottom with
  £69; the x-axis starts at 0.
- Chart 2: the linear histogram (30 bins) puts 98 of 140 payments in its first bin; the log
  panel spreads them out and shows the range from £1 to about £2,145.
- Chart 3: 28 daily points; the highest day is Sun 22 Feb at £2,730.79; the rolling mean
  starts on the 7th day.
- Chart 4: Online 15.5% (11 of 71), In-store 4.2% (1 of 24), Contactless 2.2% (1 of 45), on an
  axis from 0% to 100%.
- Chart 5: the flaw is named in a comment. For the currency option, the chart shows US at
  9,162.52 against a true GBP total of 7,238.39.
- `critique.md` refers to specifics of the partner's charts (a title, an axis, a number) for all
  four checklist items, not a restatement of the checklist.

## Extension exercises

1. **Heatmap without seaborn.** Build a heatmap of transaction counts, weekday (rows, Monday
   first) by hour band (Night 00-05, Morning 06-11, Afternoon 12-17, Evening 18-23), with
   `pd.crosstab` and `ax.imshow`, a single-hue colour map, a colour bar, and the count written
   in every cell with `ax.text`. Done: `weekday_hour_heatmap.png` has all 28 cells annotated,
   text is readable on dark cells, and you have printed the busiest cell.
2. **Fraud scatter, accessible.** Scatter `distance_from_home_km` (x) against `amount_gbp` (y)
   on log axes, with fraud and non-fraud distinguished by marker shape as well as colour, a
   legend with group sizes, and annotations pointing at the legitimate far-from-home clusters of
   customers K004 and K007. Check what a log x-axis does to rows with a distance of 0 km, and
   deal with it. Done: `distance_amount_scatter.png` is readable in greyscale, no rows are lost,
   and a comment explains how you kept the 0 km rows.
3. **Reusable style and a dashboard.** Write a `style_axes(ax, title, xlabel, ylabel)` helper
   that applies one consistent style (title, labels, spines, grid). Rewrite four of your charts
   as functions that draw on an `ax` they are given, and combine them in one 2x2 figure with an
   overall title. Done: `dashboard.png` holds four consistent panels with no overlapping labels.
4. **Annotate the payday bump.** PaySprint's customers are paid on Fri 27 Feb. Find where the
   payday effect shows in the daily data (spend or transaction count: check both), then
   annotate it with `ax.annotate` and an arrow, and shade the payday period with `ax.axvspan`.
   Also annotate the single highest-spend day with the payment that caused it. Done:
   `daily_payday_annotated.png` carries both annotations with numbers taken from the data, and a
   comment says which measure shows the payday effect and why the other does not.
