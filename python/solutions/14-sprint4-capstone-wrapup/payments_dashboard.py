"""PaySprint card payments: monthly dashboard (Module 14 capstone solution).

Pipeline: extract -> transform -> validate (a gate: stop if any check fails) -> load
-> compute_insights -> build_charts -> print_dashboard.

Unlike the demo dashboard, the source here is the MESSY raw export, so transform() does real
work: it contains its own copy of the Module 6 / Module 12 cleaning so this file is
self-contained. Nothing is analysed until validate() has passed.

Data-access note for a non-technical stakeholder: the dashboard reads a monthly export file.
The data covers one calendar month and is reported once, after the month closes, so a file
is simpler to audit than a live connection: the same file always gives the same numbers.
Extension 1 shows that only extract() changes if the source becomes the payments API.

Run from any folder:  python solutions/14-sprint4-capstone-wrapup/payments_dashboard.py
"""
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402  (the backend must be chosen first)

SHARED = Path(__file__).resolve().parents[2] / "shared"
OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)

PERIOD_START = pd.Timestamp("2026-02-02")
PERIOD_END = pd.Timestamp("2026-03-02")  # exclusive: the month runs to the end of Sun 1 Mar
PAYDAY = pd.Timestamp("2026-02-27")
CONTACTLESS_LIMIT_GBP = 100

CHANNELS = {"online": "Online", "instore": "In-store", "contactless": "Contactless"}
ALLOWED_COUNTRIES = {"GB", "FR", "IE", "ES", "NL", "DE", "US"}
REQUIRED = ["txn_id", "txn_timestamp", "customer_id", "merchant", "merchant_category",
            "channel", "country", "currency", "amount", "amount_gbp", "status", "is_fraud"]

# Chart styling: one hue for single-series charts, dark ink for text, recessive grid.
BAR_COLOUR = "#2a78d6"
TEXT_COLOUR = "#52514e"


# --------------------------------------------------------------------------- extract

def extract():
    """Read the raw export as text, so nothing is silently converted before cleaning."""
    raw = pd.read_csv(SHARED / "messy-transactions-raw.csv", dtype=str, keep_default_na=False)
    fx = pd.read_csv(SHARED / "fx_rates.csv")
    return raw, fx


# ------------------------------------------------------------------------- transform

def clean_amount(series):
    # "£1,249.00" -> 1249.00. Blank and "TBC" become NaN and are rejected later.
    return pd.to_numeric(series.str.replace(r"[£$€,]", "", regex=True), errors="coerce")


def parse_timestamp(series):
    # Two formats are present and both are unambiguous, so parse each explicitly and combine.
    # 2026-02-29 fails both formats (2026 is not a leap year) and stays NaT: rejected, not guessed.
    iso = pd.to_datetime(series, format="%Y-%m-%d %H:%M", errors="coerce")
    alt = pd.to_datetime(series, format="%d-%b-%Y %H:%M", errors="coerce")
    return iso.fillna(alt)


def transform(raw, fx):
    """Clean the raw rows. Returns (clean DataFrame, data-quality dict)."""
    df = raw.astype(str).copy()
    quality = {"raw_rows": len(df), "rejected": [], "repairs": {}, "held_for_review": []}

    def reject(mask, reason):
        for txn_id in df.loc[mask, "txn_id"]:
            quality["rejected"].append((txn_id, reason))

    # Repair counts are measured on the rows as received, before anything is changed, so
    # they describe the source file (they include the second copy of any duplicate).
    # 1. Normalise text BEFORE removing duplicates. P0102's second copy differs only by
    #    " Amazon" and "ONLINE"; it is only an exact duplicate after normalisation.
    padded = df["merchant"] != df["merchant"].str.strip()
    quality["repairs"]["merchant whitespace trimmed"] = int(padded.sum())
    channel_key = df["channel"].str.lower().str.replace(r"[^a-z]", "", regex=True)
    quality["repairs"]["channel spellings standardised"] = int(
        (channel_key.map(CHANNELS) != df["channel"]).sum())
    for col in df.columns:
        df[col] = df[col].str.strip()
    df["channel"] = channel_key.map(CHANNELS)

    quality["repairs"]["country UK changed to GB"] = int((df["country"] == "UK").sum())
    df["country"] = df["country"].str.upper().replace({"UK": "GB"})

    # 2. Exact duplicates, now that formatting differences are gone.
    dupes = df.duplicated()
    reject(dupes, "duplicate row")
    df = df[~dupes].copy()

    # 3. Types. Record which values needed repair before converting.
    has_symbol = df["amount"].str.contains(r"[£$€,]", regex=True)
    quality["repairs"]["amount symbols/separators removed"] = int(has_symbol.sum())
    df["amount"] = clean_amount(df["amount"])

    alt_format = df["txn_timestamp"].str.match(r"^\d{2}-[A-Za-z]{3}-\d{4}")
    quality["repairs"]["timestamps in DD-Mon-YYYY format"] = int(alt_format.sum())
    df["txn_timestamp"] = parse_timestamp(df["txn_timestamp"])

    df["distance_from_home_km"] = pd.to_numeric(df["distance_from_home_km"], errors="coerce")
    df["is_fraud"] = pd.to_numeric(df["is_fraud"], errors="coerce").astype("Int64")

    # 4. Reject what cannot be recovered.
    bad_amount = df["amount"].isna()
    reject(bad_amount, "amount missing or not a number")
    bad_date = df["txn_timestamp"].isna() & ~bad_amount
    reject(bad_date, "impossible or unreadable date")
    df = df[~bad_amount & ~bad_date].copy()

    # 5. Missing category: recover from the category the same merchant has on other rows.
    df["merchant_category"] = df["merchant_category"].replace("", pd.NA)
    known = (df.dropna(subset=["merchant_category"])
             .groupby("merchant")["merchant_category"].agg(lambda s: s.mode().iloc[0]))
    quality["repairs"]["missing categories filled from merchant"] = int(df["merchant_category"].isna().sum())
    df["merchant_category"] = df["merchant_category"].fillna(df["merchant"].map(known))

    # 6. Convert to GBP (FX, foreign exchange). validate="many_to_one" fails loudly if the
    #    rates file ever gains a duplicate currency.
    df = df.merge(fx, on="currency", how="left", validate="many_to_one")
    df["amount_gbp"] = (df["amount"] * df["rate_to_gbp"]).round(2)

    # 7. Flag, do not delete: a contactless payment above the GBP 100 limit is almost certainly
    #    a keying error (P0141: Pret A Manger GBP 1,850.00, probably 18.50). It stays in the
    #    loaded data but is excluded from spend figures until someone confirms it.
    df["held_for_review"] = (df["channel"] == "Contactless") & (df["amount_gbp"] > CONTACTLESS_LIMIT_GBP)
    quality["held_for_review"] = df.loc[df["held_for_review"], "txn_id"].tolist()

    df = df.sort_values("txn_timestamp").reset_index(drop=True)
    return df, quality


# -------------------------------------------------------------------------- validate

def validate(df):
    """Return a list of failed checks (empty list = safe to analyse)."""
    failures = []
    if df.empty:
        return ["no rows loaded"]
    missing_cols = [c for c in REQUIRED if c not in df.columns]
    if missing_cols:
        return [f"missing columns: {missing_cols}"]

    nulls = df[REQUIRED].isna().sum()
    for col, n in nulls[nulls > 0].items():
        failures.append(f"{n} rows with no {col}")
    if df["txn_id"].duplicated().any():
        failures.append(f"duplicate txn_id: {sorted(df.loc[df['txn_id'].duplicated(), 'txn_id'])}")
    if not df["txn_id"].str.fullmatch(r"P\d{4}").all():
        failures.append("txn_id not in the form P0000")
    if not df["customer_id"].str.fullmatch(r"K\d{3}").all():
        failures.append("customer_id not in the form K000")
    checks = [
        ("channel", set(CHANNELS.values())),
        ("country", ALLOWED_COUNTRIES),
        ("status", {"APPROVED", "DECLINED"}),
    ]
    for col, allowed in checks:
        bad = set(df[col].dropna()) - allowed
        if bad:
            failures.append(f"unexpected {col} values: {sorted(bad)}")
    if df["rate_to_gbp"].isna().any():
        failures.append("currency with no FX rate")
    if (df["amount_gbp"] <= 0).any():
        failures.append(f"{int((df['amount_gbp'] <= 0).sum())} rows with amount <= 0")
    outside = (df["txn_timestamp"] < PERIOD_START) | (df["txn_timestamp"] >= PERIOD_END)
    if outside.any():
        failures.append(f"{int(outside.sum())} rows outside the reporting month")
    if not df["is_fraud"].isin([0, 1]).all():
        failures.append("is_fraud not 0/1")
    if (df["merchant"] != df["merchant"].str.strip()).any():
        failures.append("merchant names with leading/trailing spaces")
    over_limit = (df["channel"] == "Contactless") & (df["amount_gbp"] > CONTACTLESS_LIMIT_GBP)
    if "held_for_review" not in df.columns or (over_limit & ~df["held_for_review"]).any():
        failures.append("contactless payment over the limit that is not held for review")
    return failures


# ------------------------------------------------------------------------------ load

def load(df, out_path):
    df.to_csv(out_path, index=False)
    return out_path


# ------------------------------------------------------------------------- insights

def compute_insights(df, quality):
    # "Customer spend" = approved, not confirmed fraud, not held for review.
    spend = df[(df["status"] == "APPROVED") & (df["is_fraud"] == 0) & ~df["held_for_review"]]
    total_spend = spend["amount_gbp"].sum()

    by_category = spend.groupby("merchant_category")["amount_gbp"].sum().sort_values(ascending=False)
    top_category = by_category.index[0]

    df = df.assign(declined=df["status"] == "DECLINED",
                   channel_group=df["channel"].where(df["channel"] == "Online", "Card present"))
    decline = df.groupby("channel_group")["declined"].agg(declines="sum", transactions="count", rate="mean")
    decline_by_channel = df.groupby("channel")["declined"].mean()

    fraud = df[df["is_fraud"] == 1]
    fraud_declined = fraud[fraud["status"] == "DECLINED"]
    fraud_approved = fraud[fraud["status"] == "APPROVED"]
    non_fraud_declines = int((df["declined"] & (df["is_fraud"] == 0)).sum())

    spend = spend.assign(day=spend["txn_timestamp"].dt.normalize())
    daily = spend.groupby("day").agg(transactions=("txn_id", "size"), value=("amount_gbp", "sum"))
    daily = daily.reindex(pd.date_range(PERIOD_START, PERIOD_END - pd.Timedelta(days=1)), fill_value=0)
    is_payday = daily.index >= PAYDAY

    return {
        "rows": len(df),
        "quality": quality,
        "total_spend": total_spend,
        "spend_transactions": len(spend),
        "by_category": by_category,
        "top_category": top_category,
        "top_share": by_category.iloc[0] / total_spend * 100,
        "decline": decline,
        "decline_by_channel": decline_by_channel,
        "fraud_count": len(fraud),
        "fraud_value": fraud["amount_gbp"].sum(),
        "fraud_declined_count": len(fraud_declined),
        "fraud_declined_value": fraud_declined["amount_gbp"].sum(),
        "fraud_approved_count": len(fraud_approved),
        "fraud_approved_value": fraud_approved["amount_gbp"].sum(),
        "non_fraud_declines": non_fraud_declines,
        "daily": daily,
        "payday_txn_per_day": daily.loc[is_payday, "transactions"].mean(),
        "other_txn_per_day": daily.loc[~is_payday, "transactions"].mean(),
        "payday_value_per_day": daily.loc[is_payday, "value"].mean(),
        "other_value_per_day": daily.loc[~is_payday, "value"].mean(),
    }


# --------------------------------------------------------------------------- charts

def _style(ax, grid_axis):
    # Light gridlines along the value axis only; no top/right frame.
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(colors=TEXT_COLOUR)
    ax.grid(axis=grid_axis, color="#e5e4e0", linewidth=0.8)
    ax.set_axisbelow(True)


def build_charts(df, insights, out_dir=OUT):
    paths = []

    # Chart 1: where the money goes. Horizontal bars (long category names), sorted, from 0.
    cats = insights["by_category"].sort_values()
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(cats.index, cats.values, color=BAR_COLOUR, height=0.6)
    for y, value in enumerate(cats.values):
        ax.text(value, y, f" £{value:,.0f}", va="center", fontsize=8, color=TEXT_COLOUR)
    ax.set_xlim(left=0, right=cats.max() * 1.15)
    ax.set_title(f"{insights['top_category']} is {insights['top_share']:.0f}% of customer spend, Feb 2026",
                 loc="left")
    ax.set_xlabel("Approved spend, excluding confirmed fraud (GBP)")
    _style(ax, "x")
    fig.tight_layout()
    paths.append(out_dir / "chart_spend_by_category.png")
    fig.savefig(paths[-1], dpi=120)
    plt.close(fig)

    # Chart 2: decline rate by channel. Rates, so the axis is 0-100%.
    rates = insights["decline_by_channel"].sort_values(ascending=False) * 100
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(rates.index, rates.values, color=BAR_COLOUR, width=0.6)
    for x, value in enumerate(rates.values):
        ax.text(x, value, f"{value:.1f}%", ha="center", va="bottom", fontsize=9, color=TEXT_COLOUR)
    ax.set_ylim(0, 100)
    ax.set_title("Online payments are declined far more often", loc="left")
    ax.set_ylabel("Share of transactions declined (%)")
    _style(ax, "y")
    fig.tight_layout()
    paths.append(out_dir / "chart_decline_rate_by_channel.png")
    fig.savefig(paths[-1], dpi=120)
    plt.close(fig)

    # Chart 3: transactions per day, with the payday period marked.
    daily = insights["daily"]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(daily.index, daily["transactions"], color=BAR_COLOUR, width=0.7)
    ax.axvspan(PAYDAY - pd.Timedelta(hours=12), daily.index.max() + pd.Timedelta(hours=12),
               color="#e5e4e0", zorder=0)
    ax.text(PAYDAY, daily["transactions"].max() + 0.3, " payday onwards", fontsize=9, color=TEXT_COLOUR)
    ax.set_ylim(0, daily["transactions"].max() + 1.5)
    ax.set_title("Approved customer transactions per day", loc="left")
    ax.set_ylabel("Transactions")
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d %b"))
    _style(ax, "y")
    fig.tight_layout()
    paths.append(out_dir / "chart_daily_transactions.png")
    fig.savefig(paths[-1], dpi=120)
    plt.close(fig)
    return paths


# ------------------------------------------------------------------------ dashboard

def dashboard_lines(insights):
    """The dashboard as a list of lines, so Extension 2 can reuse the same wording."""
    i = insights
    q = i["quality"]
    online = i["decline"].loc["Online"]
    present = i["decline"].loc["Card present"]
    reasons = pd.Series([reason for _, reason in q["rejected"]]).value_counts()
    rejected_text = ", ".join(f"{n} {reason}" for reason, n in reasons.items())
    ids = ", ".join(txn for txn, _ in q["rejected"])
    rejected_detail = f" ({rejected_text}: {ids})" if q["rejected"] else ""
    held = ", ".join(q["held_for_review"]) or "none"

    return [
        "=== PaySprint card payments: February 2026 dashboard ===",
        "Period: Mon 2 Feb to Sun 1 Mar 2026. All amounts in GBP.",
        "",
        f"Customer spend: GBP {i['total_spend']:,.2f} across {i['spend_transactions']} approved "
        "transactions (excluding confirmed fraud and items held for review).",
        "",
        f"1. {i['top_category']} is the largest category: GBP {i['by_category'].iloc[0]:,.2f}, "
        f"{i['top_share']:.1f}% of customer spend. Next: {i['by_category'].index[1]} "
        f"(GBP {i['by_category'].iloc[1]:,.2f}).",
        f"2. Online payments are declined {online['rate']:.1%} of the time ({int(online['declines'])} of "
        f"{int(online['transactions'])}), against {present['rate']:.1%} for in-store and contactless "
        f"({int(present['declines'])} of {int(present['transactions'])}).",
        f"3. {i['fraud_count']} transactions (GBP {i['fraud_value']:,.2f}) were confirmed as fraud. "
        f"Declines stopped {i['fraud_declined_count']} of them, GBP {i['fraud_declined_value']:,.2f} "
        f"({i['fraud_declined_value'] / i['fraud_value']:.0%} of the fraud value); "
        f"{i['fraud_approved_count']} went through, costing GBP {i['fraud_approved_value']:,.2f}. "
        f"A further {i['non_fraud_declines']} declines were genuine customers.",
        f"4. From payday (Fri 27 Feb) customers made {i['payday_txn_per_day']:.1f} approved transactions "
        f"a day, against {i['other_txn_per_day']:.1f} before it; spend per day was GBP "
        f"{i['payday_value_per_day']:,.2f} against GBP {i['other_value_per_day']:,.2f}.",
        "",
        f"Data quality: {q['raw_rows']} rows received, {len(q['rejected'])} rejected"
        f"{rejected_detail}, {i['rows']} loaded. Held for review, not in spend figures: {held}.",
        "Repairs applied (counted on the rows received): "
        + ("; ".join(f"{k} {v}" for k, v in q["repairs"].items() if v) or "none") + ".",
    ]


def print_dashboard(insights):
    print("\n".join(dashboard_lines(insights)))


# ----------------------------------------------------------------------------- main

def run(raw, fx, data_file="dashboard_data.csv"):
    clean, quality = transform(raw, fx)
    failures = validate(clean)
    if failures:
        # The gate: no dashboard is better than a dashboard built on bad data.
        raise SystemExit("Validation failed, dashboard not produced:\n  - " + "\n  - ".join(failures))
    load(clean, OUT / data_file)
    insights = compute_insights(clean, quality)
    return clean, insights


if __name__ == "__main__":
    raw_rows, rates = extract()
    clean_df, results = run(raw_rows, rates)
    charts = build_charts(clean_df, results)
    print_dashboard(results)
    print("\nOutputs: " + ", ".join(p.name for p in [OUT / "dashboard_data.csv", *charts]))
