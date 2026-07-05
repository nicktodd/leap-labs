# Module 14 Lab — Model Answer Notes

No solution in the usual sense, this is a capstone. Notes on what good looks like and common
gaps, in the same spirit as Sprints 1-3's equivalent wrap-up modules.

## What good looks like

- **Insights cite specific numbers**, not generalities: "Equity accounts for 57.0% of total
  trade value" beats "Equity is a big part of the book."
- **Charts follow Module 10's honest-axis rule** even under capstone time pressure — a bar chart
  with a truncated y-axis, done in a rush, is exactly the mistake this sprint spent a whole
  module teaching how to catch.
- **The stakeholder explanation avoids jargon entirely** — no "ETL," no "DataFrame," no
  unexplained acronyms. If a team's explanation only makes sense to someone who took this
  course, it hasn't actually been written for the audience it claims.
- **Every team member can present at least one insight unprompted** — this is the single most
  important item on the list, the same emphasis as every earlier sprint's capstone module.

## Common gaps and quick fixes

| Gap | Likely cause | Quick fix |
|---|---|---|
| Insight has no specific number | Rushed, or copied a Module 7/9 observation without re-deriving it | Re-run the actual groupby/pivot and cite the real figure |
| Bar chart y-axis doesn't start at 0 | Module 10's rule forgotten under time pressure | Add `ax.set_ylim(bottom=0)` |
| Stakeholder explanation uses "ETL" or "DataFrame" unexplained | Written by whoever built the pipeline, for an audience like themselves | Have a teammate who didn't write the code read it back and flag anything unclear |
| Only one team member can present | Work wasn't actually shared, one person built the whole thing | Spend remaining time walking every insight through as a team |

## Running the session

Fifteen to twenty minutes for the build, ten minutes to rehearse the stakeholder presentation in
pairs. Circulate and specifically check: can this team member explain a chart they didn't
personally build?
