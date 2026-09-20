# Demo: Module 10 - Data Visualization Principles & Practice

**Duration:** 20 minutes
**Files:** `visualize_demo.py`
**Output:** PNG files written to this folder (not committed - see `.gitignore`)

## Part 1: Chart choice - matching the chart to the question (5 min)

Narration, before writing any code: the first decision in any visualization isn't colour or
style, it's **which chart type actually answers the question**.

- Comparing totals across a small number of categories -> a **bar chart**
- Showing a trend over time -> a **line chart**
- Showing the relationship between two numeric variables -> a **scatter plot**
- A pie chart, in almost every real case, is a worse bar chart in disguise - the eye is bad at
  comparing angles, good at comparing bar lengths. Avoid pie charts with more than 2-3 slices.

## Part 2: Building two honest charts (6 min)

Show `plot_asset_class_totals()` (a bar chart of total value by asset class) and
`plot_weekly_trend()` (a line chart of Module 9's weekly totals). Narrate the choices behind each:
axis labels, a title that states the actual finding (not just "Chart 1"), and a y-axis that
starts at zero for the bar chart, since a bar chart's whole visual language is "length represents
magnitude" - starting anywhere else breaks that promise to the reader.

## Part 3: Building - then catching - a misleading chart (6 min)

Show `plot_advisor_totals_misleading()`: a bar chart of total value by advisor, with the y-axis
**truncated to start at 150,000** instead of 0. Run it, and look at the result together: J.
Okafor's bar looks roughly *ten times* taller than R. Alvarez's, even though the real numbers
(115,569 vs. 13,822) are roughly 8x apart before truncation makes it look far more extreme, and
would look wildly different again at a different truncation point.

Ask the room: what's actually wrong here? The chart isn't lying about the numbers printed on the
axis, but it *is* lying about the visual impression, since a bar chart's implicit promise is
"length is proportional to value." Fix it in `plot_advisor_totals_honest()` - same data, y-axis
starting at 0 - and compare the two side by side.

## Part 4: Critiquing a chart, as a checklist (3 min)

Give the room a short checklist to critique any chart, their own or a partner's:

1. Does the chart type match the question being asked?
2. Does the axis honestly represent magnitude (no arbitrary truncation for a bar chart)?
3. Are the title and axis labels specific, not generic ("Total Trade Value by Asset Class ($)",
   not "Chart 1")?
4. Would someone unfamiliar with the dataset draw the *correct* conclusion from this chart alone?

## Key message

Chart choice and axis honesty aren't styling details, they're the difference between a chart
that informs and one that misleads, even when every number on it is technically correct.
