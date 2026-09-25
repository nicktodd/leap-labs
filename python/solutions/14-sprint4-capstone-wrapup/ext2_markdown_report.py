"""Module 14 Extension 2: write the dashboard as output/dashboard.md, with the charts embedded.

The insight wording comes from dashboard_lines() in the core solution, so the console
dashboard and the Markdown report cannot drift apart. Image links are relative to the
Markdown file (both live in output/), so the report renders wherever the folder is copied.
"""
from payments_dashboard import OUT, build_charts, dashboard_lines, extract, run

CHART_CAPTIONS = {
    "chart_spend_by_category.png": "Customer spend by merchant category",
    "chart_decline_rate_by_channel.png": "Decline rate by channel",
    "chart_daily_transactions.png": "Approved customer transactions per day",
}


def category_table(by_category, total):
    rows = ["| Category | Spend (GBP) | Share |", "| --- | ---: | ---: |"]
    for category, value in by_category.items():
        rows.append(f"| {category} | {value:,.2f} | {value / total:.1%} |")
    return rows


def build_markdown(insights, chart_paths):
    lines = dashboard_lines(insights)
    title = lines[0].strip("= ")
    period = lines[1]
    numbered = [line for line in lines if line[:2] in {"1.", "2.", "3.", "4."}]
    quality = [line for line in lines if line.startswith(("Data quality", "Repairs applied"))]
    headline = next(line for line in lines if line.startswith("Customer spend"))

    md = [f"# {title}", "", period, "", f"**{headline}**", "", "## Key findings", ""]
    md += numbered
    md += ["", "## Charts", ""]
    for path in chart_paths:
        md += [f"![{CHART_CAPTIONS.get(path.name, path.stem)}]({path.name})", ""]
    md += ["## Spend by category", ""]
    md += category_table(insights["by_category"], insights["total_spend"])
    md += ["", "## Data quality", ""]
    md += [f"- {line}" for line in quality]
    return "\n".join(md) + "\n"


if __name__ == "__main__":
    raw_rows, rates = extract()
    clean_df, results = run(raw_rows, rates)
    charts = build_charts(clean_df, results)
    report = OUT / "dashboard.md"
    report.write_text(build_markdown(results, charts), encoding="utf-8")
    print(f"Wrote {report.name} ({len(report.read_text(encoding='utf-8').splitlines())} lines), "
          f"embedding {len(charts)} charts")
    for path in charts:
        print(f"  {path.name} exists: {path.exists()}")
