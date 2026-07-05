# Module 14 Lab — Capstone: Building the Analytics Dashboard & Sprint 4 Wrap-up

## Objectives

By the end of this lab you will have:

- Applied Modules 1-13 together to build a small analytics dashboard surfacing at least three
  business insights
- Structured data ingestion as a simple ETL pipeline
- Rehearsed explaining your data-access and analysis choices to a non-technical stakeholder
- Reviewed what Friday's Sprint 4 assessment will check

## Setup

- Everything installed across this sprint: `pandas`, `matplotlib`, `scipy`, `scikit-learn`,
  `flask`, `requests`, `pytest`
- `shared/trades.csv` (repo root)
- Work in your team

## Task

Starter file: `starter_dashboard.py`, in `labs/14-sprint4-capstone-wrapup/`.

1. Structure ingestion as `extract()` / `transform()` / `load()`, per Module 12's pattern.
2. Compute **at least three** business insights from the mission dataset, each backed by a
   specific number (not "some clients trade more than others" — "Alice Chen's total trade value,
   $38,092.40, is the highest of any client").
3. Build **at least two** charts (Module 10's principles: honest axes, specific titles, labelled
   axes) that support your insights.
4. Print a plain-text "dashboard" summary — the three (or more) insights, in a form a
   non-technical stakeholder could read without opening a chart.
5. As a team, write a short paragraph (in `stakeholder-explanation.md`) explaining, in plain
   language, why you accessed the data the way you did (a local file vs. Module 11's API), and
   why you're confident the underlying data is trustworthy (referencing Module 6's cleaning or
   Module 12's validation, if relevant).
6. Rehearse presenting your dashboard and explanation to a partner playing a non-technical
   stakeholder — no jargon, no acronyms without explanation, specific numbers over vague claims.

## What Friday's Sprint 4 assessment checks

Two things: a **data analytics submission** (your dashboard code and its output) and a
**presentation** on your solution and approach. Both are things your team will have already
produced by the end of this lab.

## Acceptance criteria

- `extract`, `transform`, and `load` are each a separate, named function.
- At least three insights are printed, each citing a specific number from the actual dataset.
- At least two charts are produced, each with a specific title, labelled axes, and an honest axis
  (no arbitrary truncation on a bar chart).
- `stakeholder-explanation.md` is written in plain language, with no unexplained acronyms or
  jargon, and gives a specific reason (not a generic one) for your data-access choice.
- Every team member can present at least one insight and explain the reasoning behind it,
  unprompted.
