from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SHARED = Path(__file__).resolve().parents[2] / "shared"
OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)

txns = pd.read_csv(SHARED / "transactions.csv", parse_dates=["txn_timestamp"])
txns["weekday"] = txns["txn_timestamp"].dt.day_name()
txns["hour_band"] = pd.cut(
    txns["txn_timestamp"].dt.hour,
    bins=[-1, 5, 11, 17, 23],
    labels=["Night 00-05", "Morning 06-11", "Afternoon 12-17", "Evening 18-23"],
)

# crosstab gives the grid; reindex fixes the weekday order (alphabetical otherwise) and keeps
# any weekday/band combination with no transactions as an explicit 0.
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
grid = pd.crosstab(txns["weekday"], txns["hour_band"]).reindex(days, fill_value=0)
print(grid.to_string())

fig, ax = plt.subplots(figsize=(8, 5))
# A single-hue sequential colour map: darker = more transactions. A rainbow map would suggest
# category boundaries that are not in the data.
image = ax.imshow(grid.values, cmap="Blues", aspect="auto", vmin=0)
ax.set_xticks(range(len(grid.columns)), labels=grid.columns)
ax.set_yticks(range(len(grid.index)), labels=grid.index)

# Annotate every cell with its count, switching text colour so it stays readable on dark cells.
threshold = grid.values.max() / 2
for row in range(grid.shape[0]):
    for col in range(grid.shape[1]):
        value = grid.iat[row, col]
        ax.text(col, row, str(value), ha="center", va="center",
                color="white" if value > threshold else "black")

fig.colorbar(image, ax=ax, label="Number of transactions")
ax.set_title("Card transactions by weekday and time of day (Feb 2026)")
ax.set_xlabel("Time of day")
ax.set_ylabel("Weekday")
fig.tight_layout()
fig.savefig(OUT / "weekday_hour_heatmap.png", dpi=120)
plt.close(fig)
print("saved output/weekday_hour_heatmap.png")
busiest = grid.stack().idxmax()
print(f"busiest cell: {busiest[0]} {busiest[1]} ({grid.stack().max()} transactions)")
