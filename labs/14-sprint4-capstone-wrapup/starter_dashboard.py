from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[2] / "shared"
OUT = Path(__file__).resolve().parent


def extract():
    """TODO: read shared/trades.csv, with trade_date parsed as a real datetime."""
    raise NotImplementedError


def transform(df):
    """TODO: any cleaning/reshaping needed before analysis (this dataset is already
    clean, but keep this as its own stage)."""
    raise NotImplementedError


def load(df, out_path):
    """TODO: write df to out_path as a CSV, and return out_path."""
    raise NotImplementedError


def compute_insights(df):
    """TODO: compute at least three business insights, each backed by a specific
    number, and return them in a form print_dashboard() can use."""
    raise NotImplementedError


def build_charts(df, insights):
    """TODO: build at least two charts, following Module 10's principles (honest
    axes, specific titles, labelled axes), and save them as PNGs in this folder."""
    raise NotImplementedError


def print_dashboard(insights):
    """TODO: print the insights as a plain-text summary a non-technical stakeholder
    could read without opening a single chart."""
    raise NotImplementedError


if __name__ == "__main__":
    raw = extract()
    clean = transform(raw)
    load(clean, OUT / "dashboard_data_loaded.csv")
    insights = compute_insights(clean)
    build_charts(clean, insights)
    print_dashboard(insights)
