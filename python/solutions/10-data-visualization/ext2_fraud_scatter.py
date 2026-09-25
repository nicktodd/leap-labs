from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SHARED = Path(__file__).resolve().parents[2] / "shared"
OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)

txns = pd.read_csv(SHARED / "transactions.csv")
fx = pd.read_csv(SHARED / "fx_rates.csv")
txns = txns.merge(fx, on="currency", how="left", validate="many_to_one")
txns["amount_gbp"] = (txns["amount"] * txns["rate_to_gbp"]).round(2)

zero_distance = txns[txns["distance_from_home_km"] == 0]
print(f"rows with distance 0 km: {len(zero_distance)} ({', '.join(zero_distance['txn_id'])}, "
      f"is_fraud = {zero_distance['is_fraud'].tolist()})")

fig, ax = plt.subplots(figsize=(9, 5.5))
# Fraud is shown by marker shape AND colour, so the chart still works in greyscale or for a
# reader with colour-vision deficiency. Legitimate points are drawn first so fraud sits on top.
groups = [
    (0, "Legitimate", "o", "#2a78d6", 30),
    (1, "Confirmed fraud", "X", "#eb6834", 90),
]
for flag, label, marker, colour, size in groups:
    subset = txns[txns["is_fraud"] == flag]
    ax.scatter(subset["distance_from_home_km"], subset["amount_gbp"], marker=marker, s=size,
               color=colour, edgecolor="white", linewidth=0.6, alpha=0.9,
               label=f"{label} ({len(subset)})")

# A plain log axis cannot show 0: log(0) is undefined, and matplotlib silently drops those
# points. Here the two dropped points would be K009's card-testing fraud. "symlog" is linear
# between 0 and linthresh and logarithmic above it, so the 0 km rows stay on the chart.
ax.set_xscale("symlog", linthresh=1)
ax.set_xlim(left=0)
ax.set_yscale("log")

# Label the two legitimate far-from-home clusters that a distance rule would flag.
# The text positions are in data coordinates, chosen to sit in empty areas of the chart.
for customer, text, text_xy, align in [("K004", "K004: holiday in Spain", (40, 12), "left"),
                                       ("K007", "K007: US business trip", (5000, 2.2), "right")]:
    rows = txns[(txns["customer_id"] == customer) & (txns["distance_from_home_km"] > 300)]
    x, y = rows["distance_from_home_km"].median(), rows["amount_gbp"].median()
    ax.annotate(f"{text} ({len(rows)} legitimate)", xy=(x, y), xytext=text_xy, ha=align,
                arrowprops={"arrowstyle": "->", "color": "0.3"})
    print(f"{customer}: {len(rows)} rows > 300 km, median distance {x:,.1f} km, "
          f"fraud rows {rows['is_fraud'].sum()}")

ax.set_title("Fraud clusters far from home, but so do two legitimate travellers")
ax.set_xlabel("Distance from home (km, symmetric log scale)")
ax.set_ylabel("Amount (GBP, log scale)")
ax.legend(loc="upper left")
fig.tight_layout()
fig.savefig(OUT / "distance_amount_scatter.png", dpi=120)
plt.close(fig)
print("saved output/distance_amount_scatter.png")
