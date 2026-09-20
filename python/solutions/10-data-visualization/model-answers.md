# Module 10 Lab - Model Answer Notes

See `visualize.py`. Verified: all four charts render correctly (checked visually), the bar
chart's y-axis starts at 0, the scatter plot contains only Equity trades, and the misleading
chart's truncated axis (bottom=13000, just below the smallest advisor total) makes R. Alvarez's
bar nearly disappear despite it being a real, meaningfully smaller number, not a rounding error.

Key points to check in a delegate's solution:

- **Chart type matches the question**: bar for a categorical comparison, line for a trend over
  time, scatter for a relationship between two numeric variables. A delegate who uses a line
  chart for the asset-class comparison (implying a trend that doesn't exist across categories)
  should be corrected.
- **The bar chart's y-axis genuinely starts at 0** - check `ax.set_ylim(bottom=0)` or equivalent
  is present, not just that the chart "looks fine" by chance.
- **The scatter plot is filtered to `asset_class == "Equity"` before plotting**, not filtered
  after by eye, and not left as the whole dataset with equity trades merely highlighted.
- **The misleading chart's comment names the specific mechanism** ("truncated y-axis, starting
  just below the smallest value") - a comment that only says "this chart is misleading" without
  saying how doesn't meet the bar.
- **`critique.md` must reference specifics from the partner's actual charts** (a title, an axis
  choice, a specific number) - a critique that could apply to any chart, unchanged, hasn't
  actually looked at the partner's work.
