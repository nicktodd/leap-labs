# Module 10 Lab - Data Visualization Principles & Practice

## Objectives

By the end of this lab you will have:

- Chosen the right chart type for a specific question
- Built a small set of clear, honest visualizations from the mission dataset
- Peer-critiqued a partner's charts against a specific checklist

## Setup

- `pip install pandas matplotlib`
- `shared/trades.csv` (repo root)
- Pair up with a partner for the critique step

## Task

Starter file: `starter_visualize.py`, in `labs/10-data-visualization/`.

1. Build a **bar chart** showing total `value` by `asset_class`, with a y-axis starting at 0, a
   specific title (not "Chart 1"), and labelled axes. Save it as `chart_asset_class.png`.
2. Build a **line chart** showing total `value` by week (reuse Module 9's `resample("W")`
   pattern), with a specific title and labelled axes. Save it as `chart_weekly_trend.png`.
3. Build a **scatter plot** of `quantity` vs. `value` for Equity trades only, with labelled axes.
   Save it as `chart_quantity_vs_value.png`.
4. Deliberately build one **misleading** version of one of your charts (e.g. a truncated y-axis
   on the bar chart), saved separately as `chart_misleading.png`, with a one-sentence comment
   explaining exactly what makes it misleading.

## Peer critique

Swap charts with your partner (not code, just the PNG files) and, for each of their four charts,
answer against this checklist:

1. Does the chart type match the question being asked?
2. Does the axis honestly represent magnitude?
3. Are the title and axis labels specific, not generic?
4. Would someone unfamiliar with the dataset draw the correct conclusion from this chart alone?

Write your critique of your partner's charts as a short markdown file, `critique.md`, in your own
lab folder - one short paragraph per chart.

## Acceptance criteria

- All four PNG files are produced, with no errors, and are visually correct (open them and check).
- Both "honest" charts (bar and line) have a specific title and labelled axes; the bar chart's
  y-axis starts at 0.
- The scatter plot only includes Equity trades, not the whole dataset.
- The misleading chart has an accompanying comment naming the specific flaw.
- `critique.md` contains a genuine critique of a partner's actual charts against all four
  checklist items, not a restatement of the checklist itself.
