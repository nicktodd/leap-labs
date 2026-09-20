# Demo: Module 14 - Capstone: Building the Analytics Dashboard & Wrap-up

**Duration:** 15 minutes
**Files:** `dashboard_demo.py`

## Part 1: One script, everything this week taught (5 min)

Walk through `dashboard_demo.py` top to bottom without running it yet. Point out that every
function is something delegates have already built, module by module:

- `extract()` / `transform()` / `load()` - Module 12's ETL structure, reusing Module 6's cleaning
- `compute_insights()` - Module 7's EDA and Module 9's groupby/pivot patterns
- `build_charts()` - Module 10's chart-choice and honest-axis principles
- `print_dashboard()` - a plain-text summary a non-technical stakeholder could read without
  opening a single chart

Narration: a capstone isn't new content, it's proof the pieces actually fit together into
something a real stakeholder could use.

## Part 2: Running it and reading the insights (5 min)

Run the script. Look at the three insights together:

1. Equity accounts for 57% of total trade value
2. J. Okafor's average trade (~$12,841) is roughly 4.6x R. Alvarez's (~$2,764)
3. Week 1 trading value (~$122,205) outpaced week 2 (~$79,855)

Narration: each of these is a genuine finding from the actual mission dataset, not a scripted
example - the same numbers a delegate would find doing this analysis themselves.

## Part 3: Structuring ingestion, and the stakeholder explanation (5 min)

Point out `extract()` reads from a local file, structured exactly like Module 12's pipeline -
narrate that in a real system, `extract()` is where you'd swap in Module 11's API client instead,
without touching `transform()` or `load()` at all, if the data source changed from a file to a
live feed.

Read the stakeholder-facing explanation at the bottom of the script's docstring out loud, as a
model for the lab's own requirement: plain language, no jargon, a specific reason tied to this
dataset's actual characteristics (small, daily-refreshed), not a generic textbook answer.

## Key message

This module has almost no new content on purpose - it exists to prove this week's pieces
(Python fundamentals, pandas, cleaning, EDA, statistics, visualization, APIs, ETL, and modelling)
combine into one coherent, explainable deliverable, and that you can explain your choices to
someone who doesn't code.
