# Sprint 4 - Project Friday Guidance

## Context

This week's teaching covers Python, pandas, data cleaning, exploratory data analysis,
statistical foundations, APIs, ETL validation and predictive analytics.

This week's deliverable is a Python "dashboard" surfacing three business insights, backed by a
tested extract-transform-load pipeline reading from whatever store(s) you designed in Sprint 3.
"Dashboard" here means what the week has actually taught: a plain Python script, run from the
command line, that prints a plain-text summary and saves its charts as image files with
matplotlib. Nothing this week teaches Jupyter, Streamlit, Dash or any other notebook or web UI
library, so don't let a team go looking for one, or burn Friday building one from scratch.
Notebooks are the more common tool for this kind of exploratory work in the real world, worth
a look in your own time, but not something to spend project time on this week.

## Suggested Friday session

- Agree as a team what the three business insights actually are before anyone writes a pipeline.
  Go back to the requirements spec and the customer meeting notes from Sprint 2, this is where a
  vague deliverable becomes a specific one.
- Sketch the ETL: what you're extracting from the Sprint 3 schema, what shape it needs to be in
  for analysis, and where the two disagree.
- Check you actually have enough data to say anything meaningful. A trend by period or client
  segment needs real volume and variety across time, not the handful of rows you seeded in
  Sprint 3 to test constraints. Generating a larger synthetic dataset is a good use of AI, just
  keep it consistent with your schema's constraints and realistic enough to support the insights
  you've chosen.
- Decide how the pipeline will be tested, and who owns writing those tests, before the pipeline
  itself is built.
- If you're not confident the three insights you've picked are actually the ones that matter,
  don't just guess from the Sprint 2 notes, ask your customer instructor directly. Ten minutes
  now is cheaper than a dashboard built around the wrong three.
- Refine the backlog: are the insights you've chosen actually what the customer asked for?

## What to present to the class

- The three business insights you've chosen, and why they're the right three.
- Your ETL design, and how you're testing it.
- An updated backlog, and anything from the Sprint 3 initial database designs that might need to be changed
