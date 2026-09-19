from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[2] / "shared"
OUT = Path(__file__).resolve().parent
trades = pd.read_csv(BASE / "trades.csv", parse_dates=["trade_date"])

# TODO:
# 1. Bar chart: total value by asset_class, y-axis starting at 0, specific title,
#    labelled axes -> chart_asset_class.png
# 2. Line chart: total value by week (reuse Module 9's resample("W") pattern),
#    specific title, labelled axes -> chart_weekly_trend.png
# 3. Scatter plot: quantity vs value, Equity trades only, labelled axes
#    -> chart_quantity_vs_value.png
# 4. One deliberately misleading chart, with a comment explaining the specific flaw
#    -> chart_misleading.png
